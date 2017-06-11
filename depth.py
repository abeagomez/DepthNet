import freenect
import numpy as np

depth, timestamp = freenect.sync_get_depth()
np.clip(depth, 0, 2**10 - 1, depth)
depth >>= 2
depth = depth.astype(np.uint8)
#print(len(depth))

frame = freenect.sync_get_video()[0]