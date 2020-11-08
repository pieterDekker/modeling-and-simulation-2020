import argparse
import json

def parse_args():
    ap = argparse.ArgumentParser(description='Simulate N bodies')
    ap.add_argument('file')
    ap.add_argument('--output-dir', default='output', type=str)
    ap.add_argument('--simulation-method', default='barnes-hut', choices=['massless', 'barnes-hut', 'unpickle'])
    ap.add_argument('--barnes-hut-theta', default=1, type=float )
    ap.add_argument('--output-method', default='animate', choices=['animate', 'write', 'pickle'])
    ap.add_argument('--delta-t', default=0.05, type=float)
    ap.add_argument('--output-interval', default=10, type=int)
    ap.add_argument('--t-total', default=1000, type=int)
    args = ap.parse_args()
    return args.file, args.output_dir, args.simulation_method, args.barnes_hut_theta, args.output_method, args.delta_t, args.output_interval, args.t_total

def parse_file(file):
    with open(file, 'r') as f:
        params = json.load(f)
        return params['ngal'], params['m'], params['e'], params['rmin'], params['ring_spacing'], params['thetadeg'], params['nrings'], params['ninner']