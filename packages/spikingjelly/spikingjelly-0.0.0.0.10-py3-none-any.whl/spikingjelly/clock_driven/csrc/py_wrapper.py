import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.cpp_extension

# torch_cpp_wrapper = torch.utils.cpp_extension.load(name="torch_cpp_wrapper", sources=["./spikingjelly/clock_driven/csrc/torch_cpp_wrapper.cpp"])
from torch.utils.cpp_extension import load_inline
torch_cpp_wrapper = load_inline(
        name='at_ops',
        cpp_sources=["""
        using namespace at;
        """],
        functions=[
            "cudnn_convolution_backward",
            "cudnn_convolution_backward_input",
            "cudnn_convolution_backward_weight",
        ],
        with_cuda=True,
        verbose=True
)

class spike_convolution(torch.autograd.Function):
    # Pytorch only provides cudnn_convolution without bias.
    # Refer to https://github.com/pytorch/pytorch/issues/3823 for more details.
    @staticmethod
    def forward(ctx, spike, weight, bias, padding, stride, dilation, groups):
        if ctx.needs_input_grad[0] or ctx.needs_input_grad[1] or ctx.needs_input_grad[2]:
            ctx.save_for_backward(
                spike.bool() if ctx.needs_input_grad[1] else None,
                weight if ctx.needs_input_grad[0] else None
            )
            if ctx.needs_input_grad[1]:
                ctx.spike_dtype = spike.dtype
            ctx.padding = padding
            ctx.stride = stride
            ctx.dilation = dilation
            ctx.groups = groups

        if spike.dim() == 3:
            return F.conv1d(input=spike, weight=weight, bias=bias, stride=stride, padding=padding, dilation=dilation, groups=groups)
        elif spike.dim() == 4:
            return F.conv2d(input=spike, weight=weight, bias=bias, stride=stride, padding=padding, dilation=dilation, groups=groups)
        elif spike.dim() == 5:
            return F.conv3d(input=spike, weight=weight, bias=bias, stride=stride, padding=padding, dilation=dilation, groups=groups)



    @staticmethod
    def backward(ctx, grad_output):
        grad_spike = None
        grad_weight = None
        grad_bias = None
        if ctx.needs_input_grad[0] and ctx.needs_input_grad[1]:
            spike, weight = ctx.saved_tensors
            spike = spike.to(ctx.spike_dtype)
            grad_spike, grad_weight = torch_cpp_wrapper.cudnn_convolution_backward(spike, grad_output, weight, ctx.padding,
                                                                               ctx.stride, ctx.dilation, ctx.groups,
                                                                               torch.backends.cudnn.benchmark,
                                                                               torch.backends.cudnn.deterministic,
                                                                               torch.backends.cudnn.allow_tf32, (
                                                                               True,
                                                                               True))

        elif not ctx.needs_input_grad[0] and ctx.needs_input_grad[1]:
            spike, _ = ctx.saved_tensors[0]
            spike = spike.to(ctx.spike_dtype)
            grad_weight = torch_cpp_wrapper.cudnn_convolution_backward_weight(ctx.weight_shape, grad_output, spike, ctx.padding,
                                                                               ctx.stride, ctx.dilation, ctx.groups,
                                                                               torch.backends.cudnn.benchmark,
                                                                               torch.backends.cudnn.deterministic,
                                                                               torch.backends.cudnn.allow_tf32)

        elif ctx.needs_input_grad[0] and not ctx.needs_input_grad[1]:
            _, weight = ctx.saved_tensors[0]
            grad_spike = torch_cpp_wrapper.cudnn_convolution_backward_input(ctx.spike_shape, grad_output, weight, ctx.padding,
                                                                               ctx.stride, ctx.dilation, ctx.groups,
                                                                               torch.backends.cudnn.benchmark,
                                                                               torch.backends.cudnn.deterministic,
                                                                               torch.backends.cudnn.allow_tf32)

        if ctx.needs_input_grad[2]:
            # grad_output.shape = [N, C, *]
            out_channels = grad_output.shape[1]
            grad_bias = grad_output.transpose(0, 1).view(out_channels, -1).sum(1)
        return grad_spike, grad_weight, grad_bias, None, None, None, None

class spike_linear(torch.autograd.Function):
    @staticmethod
    def forward(ctx, spike, weight, bias=None):
        # spike.shape = [N, *, in_features]
        # weight.shape = [out_features, in_features]
        # bias.shape = [out_features]
        if ctx.needs_input_grad[0] or ctx.needs_input_grad[1] or ctx.needs_input_grad[2]:
            ctx.save_for_backward(spike.bool() if ctx.needs_input_grad[1] else None,
                                  weight if ctx.needs_input_grad[1] else None)
            if ctx.needs_input_grad[1]:
                ctx.spike_dtype = spike.dtype
        return F.linear(spike, weight, bias)

    @staticmethod
    def backward(ctx, grad_output):
        # grad_output.shape = [N, *, out_features]
        spike, weight = ctx.saved_tensors
        grad_spike = grad_weight = grad_bias = None

        if ctx.needs_input_grad[0]:
            grad_spike = F.linear(grad_output, weight.t(), bias=None)
        if ctx.needs_input_grad[1]:
            in_features = spike.shape[-1]
            out_features = grad_output.shape[-1]
            # grad_output.view(-1, out_features).t().shape = [out_features, N*]
            # spike.view(-1, in_features).shape = [N*, in_features]
            grad_weight = torch.mm(grad_output.view(-1, out_features).t(), spike.view(-1, in_features).to(ctx.spike_dtype))
        if ctx.needs_input_grad[2]:
            out_features = grad_output.shape[-1]
            grad_bias = grad_output.view(-1, out_features).sum(0)

        return grad_spike, grad_weight, grad_bias
