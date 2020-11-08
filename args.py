import argparse
import json

def parse_args():
    ap = argparse.ArgumentParser(description='Simulate N bodies')
    ap.add_argument('file')
    ap.add_argument('--output-dir', default='output', type=str, help='The directory to which output is written, if  \'pickle\' is selected as ouptut method or whre output is read from if \'simulatino-method\' is unpickle')
    ap.add_argument('--simulation-method', default='barnes-hut', choices=['massless', 'barnes-hut', 'unpickle'], help='\'unpickle\' means that data is read from \'output-dir\'')
    ap.add_argument('--barnes-hut-theta', default=1, type=float, help='theta value to use, ignored unless simulation-method is \'barnes-hut\'')
    ap.add_argument('--output-method', default='animate', choices=['animate', 'pickle'], help='either animate the results or write the states to python pickles')
    ap.add_argument('--delta-t', default=0.05, type=float, help='timestep in megayears')
    ap.add_argument('--output-interval', default=10, type=int, help='output every t=? megayears')
    ap.add_argument('--t-total', default=1000, type=int, help='the amount of megayears to simulate')
    ap.add_argument('--savefig-dir', default='figures', type=str, help='where every 250th figure is saved, if the output-method is \'animate\' ')
    args = ap.parse_args()
    return args.file, args.output_dir, args.simulation_method, args.barnes_hut_theta, args.output_method, args.delta_t, args.output_interval, args.t_total, args.savefig_dir

def parse_file(file):
    with open(file, 'r') as f:
        params = json.load(f)
        return params['ngal'], params['m'], params['e'], params['rmin'], params['ring_spacing'], params['thetadeg'], params['nrings'], params['ninner']
