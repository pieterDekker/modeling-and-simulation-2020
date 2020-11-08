from os import path, makedirs
import pickle
import numpy as np


def pickle_hyper_params(bhut_theta, delta_t, output_interval, t_total, outdir):
    if not path.isdir(outdir):
        makedirs(outdir)
    filename = path.join(outdir, 'hyperparameters.par')
    with open(filename, 'wb') as f:
        pickle.dump((bhut_theta, delta_t, output_interval, t_total), f)


def unpickle_hyper_params(outdir):
    filename = path.join(outdir, 'hyperparameters.par')
    with open(filename, 'rb') as f:
        return pickle.load(f)


def pickle_params(ngal, m, e, r_min, ring_spacing, inclination_angle, n_rings, n_inner, outdir):
    if not path.isdir(outdir):
        makedirs(outdir)
    filename = path.join(outdir, 'parameters.par')
    with open(filename, 'wb') as f:
        pickle.dump((ngal, m, e, r_min, ring_spacing, inclination_angle, n_rings, n_inner), f)


def unpickle_params(outdir):
    filename = path.join(outdir, 'parameters.par')
    with open(filename, 'rb') as f:
        return pickle.load(f)


def pickle_state(x, nfile, outdir):
    if not path.isdir(outdir):
        makedirs(outdir)
    filename = path.join(outdir, f'snap_{nfile:05d}')
    with open(filename, 'wb') as f:
        pickle.dump(x, f)


def unpickle_state(nfile, outdir):
    filename = path.join(outdir, f'snap_{nfile:05d}')
    with open(filename, 'rb') as f:
        return pickle.load(f)


if __name__ == '__main__':
    pickle_hyper_params(1, 2, 3, 4, 'output_test')
    print(unpickle_hyper_params('output_test'))
    pickle_params(1, [2], [3], 4, [1], [90], [1], [1], 'output_test')
    print(unpickle_params('output_test'))
    pickle_state(np.array([1,2,3,4]), 0, 'output_test')
    print(unpickle_state(0, 'output_test'))
