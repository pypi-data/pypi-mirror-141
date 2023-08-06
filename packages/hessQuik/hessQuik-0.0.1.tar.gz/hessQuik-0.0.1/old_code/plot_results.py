import torch
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np

import os
import pickle

plt.rcParams.update({'font.size': 32})
plt.rcParams.update({'image.interpolation': None})
plt.rcParams['figure.figsize'] = [18, 12]
plt.rcParams['figure.dpi'] = 200


#%% HESSQUIK VS PYTORCH
load_dir = '/Users/elizabethnewman/Desktop/hessQuikResults/scalar/'

os.chdir(load_dir)

markers = ['o', '^', 's']
filled = [True, False, False]
linewidth = 6
markersize = 20


plt.figure()
for i, name in enumerate(['hessQuik', 'PytorchAD', 'PytorchHessian']):
    output = pickle.load(open('12-22-2021--' + name + '-resnet-cpu-w16-d4-out1.p', 'rb'))
    results = output['results']

    x = results['in_feature_range']
    y = results['timing_trials_mean'].squeeze()

    plt.semilogy(x, y, '-' + markers[i], linewidth=linewidth, markersize=markersize, label=name + ': cpu')

    output = pickle.load(open('12-22-2021--' + name + '-resnet-cuda-w16-d4-out1.p', 'rb'))
    results = output['results']

    x = results['in_feature_range']
    y = results['timing_trials_mean'].squeeze()

    plt.semilogy(x, y, '--' + markers[i], linewidth=linewidth, markersize=markersize, label=name + ': cuda')


plt.xscale('log', base=2)
plt.yscale('log', base=10)
plt.xlabel('in features')
plt.ylabel('time (seconds)')
plt.grid()
plt.ylim(1e-3, 2e1)
plt.legend()
plt.show()

#%% WIDTH AND DEPTH
load_dir = '/Users/elizabethnewman/Desktop/hessQuikResults/scalar'
os.chdir(load_dir)
for w in [8, 16, 32, 64]:
    output = pickle.load(open('12-17-2021---hessQuik-cpu-w' + str(w) + '-d4.p', 'rb'))
    results = output['results']
    timing_trials_mean = results['timing_trials_mean']
    in_feature_range = results['in_feature_range']
    out_feature_range = results['out_feature_range']

    x = results['in_feature_range']
    y = results['timing_trials_mean'].squeeze()

    p = plt.semilogy(x, y, '-o', linewidth=linewidth, markersize=markersize, label=str(w))
    #
    # output = pickle.load(open('12-17-2021---hessQuik-cuda-w' + str(w) + '-d4.p', 'rb'))
    # results = output['results']
    # timing_trials_mean = results['timing_trials_mean']
    # in_feature_range = results['in_feature_range']
    # out_feature_range = results['out_feature_range']
    #
    # x = results['in_feature_range']
    # y = results['timing_trials_mean'].squeeze()
    #
    # plt.semilogy(x, y, '--o', linewidth=linewidth, markersize=markersize, label=str(w), color=p[0].get_color())


plt.xscale('log', base=2)
plt.yscale('log', base=10)
plt.xlabel('in features')
plt.ylabel('time (seconds)')
plt.grid()
plt.ylim(1e-3, 2e1)
plt.legend()
plt.show()


for d in [2, 4, 8, 16]:
    output = pickle.load(open('12-17-2021---hessQuik-cpu-w16-d' + str(d) + '.p', 'rb'))
    results = output['results']
    timing_trials_mean = results['timing_trials_mean']
    in_feature_range = results['in_feature_range']
    out_feature_range = results['out_feature_range']

    x = results['in_feature_range']
    y = results['timing_trials_mean'].squeeze()
    #
    p = plt.semilogy(x, y, '-o', linewidth=linewidth, markersize=markersize, label=str(d))
    #
    # output = pickle.load(open('12-17-2021---hessQuik-cuda-w16-d' + str(d) + '.p', 'rb'))
    # results = output['results']
    # timing_trials_mean = results['timing_trials_mean']
    # in_feature_range = results['in_feature_range']
    # out_feature_range = results['out_feature_range']
    #
    # x = results['in_feature_range']
    # y = results['timing_trials_mean'].squeeze()
    #
    # plt.semilogy(x, y, '--p', linewidth=linewidth, markersize=markersize, label=str(d), color=p[0].get_color())

plt.xscale('log', base=2)
plt.yscale('log', base=10)
plt.xlabel('in features')
plt.ylabel('time (seconds)')
plt.grid()
plt.ylim(1e-3, 2e1)
plt.legend()
plt.show()

#%% VECTOR OUTPUT
load_dir = '/Users/elizabethnewman/Desktop/hessQuikResults/vector/'

plt.rcParams.update({'font.size': 24})
plt.rcParams.update({'image.interpolation': None})
plt.rcParams['figure.figsize'] = [14, 12]
plt.rcParams['figure.dpi'] = 200

os.chdir(load_dir)

fig, axes = plt.subplots(nrows=1, ncols=4)
for i, name in enumerate(['cpu', 'cuda']):
    output = pickle.load(open('12-22-2021--hessQuik-resnet-' + name + '-w16-d4-out4.p', 'rb'))
    results = output['results']
    timing_trials_mean = results['timing_trials_mean']
    in_feature_range = results['in_feature_range']
    out_feature_range = results['out_feature_range']
    print(timing_trials_mean)

    # plt.subplot(1, 4, 2 * i + 1)

    im = axes[2 * i].imshow(torch.flipud(timing_trials_mean), norm=colors.LogNorm(vmin=1e-3, vmax=1e2))
    plt.sca(axes[2 * i])
    plt.xticks(list(torch.arange(len(out_feature_range)).numpy()), labels=['$2^0$', '$2^1$', '$2^2$', '$2^3$'])
    # plt.xlabel('out_features')

    if i == 0:
        plt.yticks(list(torch.arange(len(in_feature_range)).numpy()),
                   labels=['$2^{10}$', '$2^9$', '$2^8$', '$2^7$', '$2^6$', '$2^5$', '$2^4$', '$2^3$', '$2^2$', '$2^1$', '$2^0$'])
    else:
        plt.tick_params(axis='y', left=False, right=False, labelleft=False)
    plt.title('hessQuik: ' + name, fontsize=16)

    output = pickle.load(open('12-22-2021--PytorchAD-resnet-' + name + '-w16-d4-out4.p', 'rb'))
    results = output['results']
    timing_trials_mean = results['timing_trials_mean']
    in_feature_range = results['in_feature_range']
    out_feature_range = results['out_feature_range']
    print(timing_trials_mean)


    im = axes[2 * i + 1].imshow(torch.flipud(timing_trials_mean), norm=colors.LogNorm(vmin=1e-3, vmax=1e2))
    plt.sca(axes[2 * i + 1])
    plt.xticks(list(torch.arange(len(out_feature_range)).numpy()), labels=['$2^0$', '$2^1$', '$2^2$', '$2^3$'])
    plt.tick_params(axis='y', left=False, right=False, labelleft=False)
    plt.title('PytorchAD: ' + name, fontsize=16)

fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.27, 0.02, 0.45])
fig.colorbar(im, cax=cbar_ax)
fig.text(0.02, 0.5, 'input features', va='center', rotation='vertical')
fig.text(0.5, 0.15, 'output features', ha='center')
plt.show()

