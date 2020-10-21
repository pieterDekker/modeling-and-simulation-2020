import argparse
import json

def parseArgs():
  ap = argparse.ArgumentParser(description='Simulate N bodies')
  ap.add_argument('file')
  ap.add_argument('-o', '--output-dir')
  args = ap.parse_args()
  with open(args.file, 'r') as f:
    params = json.load(f)
  return (*params)
  ngal = params['ngal']
  m = params['m']
  e = params['e']
  rmin = params['rmin']
  ring_spacing = params['ring_spacing']
  thetadeg = params['thetadeg']
  nrings = params['nrings']
  ninner = params['ninner']
  if 'output_dir' in params:
    outdir = params['output_dir']
    write_output = True