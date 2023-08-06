from line_profiler import LineProfiler
import random
import torch
import hessQuik.activations as act
import hessQuik.layers as lay
import hessQuik.networks as net

# f = net.fullyConnectedNN([10, 20, 1], act=act.antiTanhActivation())

width = 20
f = net.NN(lay.singleLayer(2, width, act=act.antiTanhActivation()),
           net.resnetNN(width=width, depth=4, act=act.antiTanhActivation()),
           lay.singleLayer(width, 1, act=act.identityActivation()))

x = torch.randn(100, f.dim_input())

f = net.NNPytorchAD(f)
x.requires_grad = True

def eval(x):
    out = f(x, do_gradient=True, do_Hessian=True, forward_mode=False)


# numbers = [random.randint(1, 100) for i in range(1000)]
lp = LineProfiler()
lp_wrapper = lp(eval)
lp.add_function(f.forward)
# lp.add_function(f[1][0].forward)
# lp.add_function(f[1][0].backward)
lp_wrapper(x)
lp.print_stats()

