from os import path, getcwd, mkdir

def write_int(f, v):
  f.write(str(v) + '\n')

def write_float(f, v):
  f.write(str(v) + '\n')

def write_float_list(f, l, s):
  f.write(s.join(list(map(lambda x: str(x), l))) + '\n')

def write_int_list(f, l, s):
  f.write(s.join(list(map(lambda x: str(int(x)), l))) + '\n')

def write_params(ngal,m,e,rmin,thetadeg,nrings,ninner,dr,outdir, separator = '\t'):
  if not path.isdir(outdir):
    mkdir(outdir)
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

def write_state(xs, vs, ms, time, nfile, outdir, separator = '\t'):
  if not path.isdir(outdir):
    mkdir(outdir)
  filename = path.join(outdir, f'snap_{nfile:05d}')
  with open(filename, 'w') as f:
    write_float(f, time)
    for x, v, m in zip(xs, vs, ms):
      write_float_list(f, [*x, *v, m], separator)

if __name__ == '__main__':
  write_params(2, [1, 2], [0, 0], 20, [0, 120], [5, 4], [20, 30], 14, path.join(getcwd(), 'output_test'))
  write_state([[1,2,3],[4,5,6]], [[1,1,1],[2,2,2]], [10, 20], 10, 1, 'output_test')