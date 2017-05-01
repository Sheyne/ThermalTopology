import numpy as np
import cv2
from matplotlib import cm
import numpy as np
from PIL import Image
import mapper
import graphviz
from glob import glob

# http://stackoverflow.com/questions/16571150/how-to-capture-stdout-output-from-a-python-function-call

from io import StringIO
import sys

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout

cap = cv2.VideoCapture(0)

grid = np.mgrid[0:60, 0:80].transpose(1,2,0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = (frame[:,:,0] > 30)

    hot_points = grid[gray]


    cov = mapper.cover.balanced_cover_1d(30)
    flt = hot_points[:, 0].reshape(-1, 1).astype(np.float)
    pts = hot_points.astype(np.float)

    with Capturing() as output:
        mappered = mapper.mapper(pts, flt, cov, mapper.cutoff.histogram(30))

    canvas = np.zeros((gray.shape[0],gray.shape[1],3), dtype=np.uint8)

    for node in mappered.nodes:
        color,  = cm.viridis(np.random.rand(1)) * 255
        for x,y in hot_points[node.points]:
            canvas[x, y, 0] = color[0]
            canvas[x, y, 1] = color[1]
            canvas[x, y, 2] = color[2]



    # Display the resulting frame
    cv2.imshow('frame',canvas)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
