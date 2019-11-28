from matplotlib import cm

from matplotlib.colors import Normalize as color_norm

cmap = cm.get_cmap('jet')

norm = color_norm(vmin=1, vmax=1000)

_test = cmap(norm(400))
print(type(_test))