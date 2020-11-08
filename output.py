from os import path, getcwd, mkdir, makedirs
import pickle
import numpy as np


def write_int(f, v):
    f.write(str(v) + '\n')


def write_float(f, v):
    f.write(str(v) + '\n')


def write_float_list(f, l, s):
    f.write(s.join(list(map(lambda x: str(x), l))) + '\n')


def write_int_list(f, l, s):
    f.write(s.join(list(map(lambda x: str(int(x)), l))) + '\n')


def write_params(ngal, m, e, rmin, thetadeg, nrings, ninner, dr, outdir, separator='\t'):
    if not path.isdir(outdir):
        makedirs(outdir)
    filename = path.join(outdir, 'parameters.par')
    with open(filename, 'w') as f:
        write_int(f, ngal)
        write_float_list(f, m, separator)
        write_float_list(f, e, separator)
        write_float(f, rmin)
        write_float_list(f, thetadeg, separator)
        write_int_list(f, nrings, separator)
        write_int_list(f, ninner, separator)
        write_float(f, dr)


def write_state(xs, vs, ms, time, nfile, outdir, separator='\t'):
    if not path.isdir(outdir):
        makedirs(outdir)
    filename = path.join(outdir, f'snap_{nfile:05d}')
    with open(filename, 'w') as f:
        write_float(f, time)
        for x, v, m in zip(xs, vs, ms):
            write_float_list(f, [*x, *v, m], separator)


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
    write_params(2, [1, 2], [0, 0], 20, [0, 120], [5, 4], [20, 30], 14, path.join(getcwd(), 'output_test'))
    write_state([[1, 2, 3], [4, 5, 6]], [[1, 1, 1], [2, 2, 2]], [10, 20], 10, 1, 'output_test')
    pickle_hyper_params(1, 2, 3, 4, 'output_test')
    print(unpickle_hyper_params('output_test'))
    pickle_params(1, [2], [3], 4, [1], [90], [1], [1], 'output_test')
    print(unpickle_params('output_test'))
    pickle_state(np.array([1,2,3,4]), 0, 'output_test')
    print(unpickle_state(0, 'output_test'))