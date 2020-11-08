import os
from math import floor

from numpy import zeros

from animated_scatter import AnimatedScatter
from args import parse_args, parse_file
from data_stream import barnes_hut_pos_stream, massless_pos_stream, barnes_hut_pos_vel_stream, massless_pos_vel_stream, unpickle_stream
from init import initialize, initialize_masses, expected_particles
from potentials import get_acceleration
from output import pickle_hyper_params, unpickle_hyper_params, pickle_params, unpickle_params, pickle_state, unpickle_state, write_params, write_state


def main():
    file, outdir, sim_method, bhut_theta, out_method, delta_t, output_interval, t_total = parse_args()
    ngal, m, e, r_min, ring_spacing, inclination_angle, n_rings, n_inner = parse_file(file)

    if not os.path.isabs(outdir):
        outdir = os.path.join(os.getcwd(), outdir)

    nsteps = floor(t_total / delta_t)
    nout = round(output_interval / delta_t)

    n_particles = expected_particles(ngal, n_inner, n_rings)

    x, v, maxes = initialize(m, e, r_min, inclination_angle, n_rings, n_inner, ring_spacing, ngal, n_particles)
    a = zeros(shape=(n_particles, 3))
    a = get_acceleration(x, a, m, ngal, n_particles)
    m = initialize_masses(m, n_particles)

    if sim_method == 'unpickle' and out_method == 'pickle':
        print('It makes no sense to unpickle and pickle')
        exit()

    if sim_method == 'barnes-hut':
        print(f'setting up barnes-hut, theta is {bhut_theta}')
        stream = barnes_hut_pos_stream(x, v, a, m, n_particles, delta_t, nsteps, 2, max(maxes))
    elif sim_method == 'massless':
        stream = massless_pos_stream(x, v, a, m, ngal, n_particles, delta_t, nsteps)
    elif sim_method == 'unpickle':
        bhut_theta, delta_t, output_interval, t_total = unpickle_hyper_params(outdir)
        ngal, m, e, r_min, ring_spacing, inclination_angle, n_rings, n_inner = unpickle_params(outdir)
        print(f'output_interval was {output_interval}')
        print(f'delta_t was {output_interval}')
        nsteps = floor(t_total / delta_t)
        nout = round(output_interval / delta_t)
        total_out = floor(nsteps / nout)
        print(f'with nstepts={nsteps} and nout={nout} expecting {total_out} files')
        stream = unpickle_stream(outdir, total_out)
    else:
        raise Exception(f'invalid simulation method: {sim_method}')

    if out_method == 'write':
        write_params(ngal, m, e, r_min, inclination_angle, n_rings, n_inner, r_min, outdir)
        t = 0
        file_n = 0
        for x, v in massless_pos_vel_stream(x, v, a, m, ngal, n_particles, delta_t, nsteps):
            if t % nout == 0:
                write_state(x, v, m, t, file_n, outdir)
                file_n += 1
            t += 1
    elif out_method == 'pickle':
        pickle_hyper_params(bhut_theta, delta_t, output_interval, t_total, outdir)
        pickle_params(ngal, m, e, r_min, ring_spacing, inclination_angle, n_rings, n_inner, outdir)
        t = 0
        file_n = 0
        print(f'with nsteps={nsteps} and nout={nout}, expecting {nsteps / nout} outputs')
        for x in stream:
            if t % nout == 0:
                print(f'pickling {file_n}/{floor(nsteps / nout)}')
                pickle_state(x, file_n, outdir)
                file_n += 1
            t += 1
    elif out_method == 'animate':
        print('starting the animation')
        anim = AnimatedScatter(
            stream,
            1.01 * max(maxes),
            ngal,
            500,
            os.path.join(os.getcwd(), 'barnes_hut_output')
        )

if __name__ == '__main__':
    main()
    # cProfile.run('main()', sort='cumtime')
