from math import sqrt
from PIL import Image
from base64 import b64encode
import numpy as np
from io import BytesIO
from uuid import uuid4

def euclideanDistance(i1, j1, i2, j2):
    return sqrt((i1 - i2) ** 2 + (j1 - j2) ** 2)


def getDB(db, key, cnt):
    return [b64encode(db.get(key + ':' + str(count))).decode('utf-8') for count in range(cnt)]

def storePath(db, path, image, key, cnt):
    img = np.array(image)
    for point in path:
        img[point[1], point[0]] = [255, 0, 0]
    img_path = Image.fromarray(img)
    img_resize = img_path.resize((300, 300), resample=Image.LANCZOS).convert('LA')
    conv = BytesIO()
    value = img_resize.save(conv, format='PNG')
    key = key + ':' + cnt
    db.set(key, conv.getvalue())



