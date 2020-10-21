import os
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class AnimatedScatter(object):
  """An animated scatter plot using matplotlib.animations.FuncAnimation.
  Adapted from https://stackoverflow.com/a/9416663/5521776
  """
  def __init__(self, data_stream, scope, ngal, output_interval, outdir):
    self.stream = data_stream
    self.scope = scope
    self.ngal = ngal
    # Setup the figure and axes...
    self.fig = plt.figure()
    self.ax = self.fig.add_subplot(111, projection='3d')
    self.output_interval = output_interval
    self.center = [0,0,0]
    if not os.path.isdir(outdir):
      os.mkdir(outdir)
    self.outdir = outdir
    self.title = self.ax.text(0.5, 0.5, 0, "N-Body", transform=self.ax.transAxes)
    # Then setup FuncAnimation.
    self.ani = animation.FuncAnimation(self.fig, self.update, interval=0, init_func=self.setup_plot, blit=True)
    plt.show()

  def setup_plot(self):
    self.center = [self.scope, self.scope, self.scope]

    """Initial drawing of the scatter plot."""
    try:
      x = next(self.stream)
      self.ax.set_xlim([self.center[0] - self.scope,self.center[0] + self.scope])
      self.ax.set_ylim([self.center[1] - self.scope, self.center[1] + self.scope])
      self.ax.set_zlim([self.center[2] - self.scope, self.center[2] + self.scope])
      self.scat, = self.ax.plot(x[:self.ngal,0], x[:self.ngal,1], x[:self.ngal,2], color="blue", linestyle="", marker="o", markersize=1.5)
      self.scat, = self.ax.plot(x[self.ngal:,0], x[self.ngal:,1], x[self.ngal:,2], color="orange",  linestyle="", marker="o", markersize=0.5)
    except StopIteration:
      self.ani.event_source.stop()
      exit()
    
    # self.ax.set_title('N-Body, time={}'.format(i))
    # For FuncAnimation's sake, we need to return the artist we'll be using
    # Note that it expects a sequence of artists, thus the trailing comma.
    return self.scat, self.ax

  def update(self, i):
    """Update the scatter plot."""
    x = next(self.stream)
    # self.ax.clear()
    self.ax.set_xlim([x[0,0] - self.scope, x[0,0] + self.scope])
    self.ax.set_ylim([x[0,1] - self.scope, x[0,1] + self.scope])
    self.ax.set_zlim([x[0,2] - self.scope, x[0,2] + self.scope])
    self.scat.set_data(x[:,0], x[:,1])
    self.scat.set_3d_properties(x[:,2])
    print('i: ', i)
    if i % self.output_interval == 0:
      self.save(x, i)
    self.title.set_text('N-Body, time={}'.format(i))

    # We need to return the updated artist for FuncAnimation to draw..
    # Note that it expects a sequence of artists, thus the trailing comma.
    return self.scat, self.ax
  
  def save(self, x, i):
    fname = os.path.join(self.outdir, f'fig_{i}')
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim([x[0,0] - self.scope, x[0,0] + self.scope])
    ax.set_ylim([x[0,1] - self.scope, x[0,1] + self.scope])
    ax.set_zlim([x[0,2] - self.scope, x[0,2] + self.scope])
    ax.plot(x[:self.ngal,0], x[:self.ngal,1], x[:self.ngal,2], color="blue", linestyle="", marker="o", markersize=1.5)
    ax.plot(x[self.ngal:,0], x[self.ngal:,1], x[self.ngal:,2], color="orange",  linestyle="", marker="o", markersize=0.5)
    fig.savefig(fname)
