from PIL import Image
import numpy as np


def get_samples(filename, coordinates, size):
    Image.MAX_IMAGE_PIXELS = 1000000000
    im = Image.open(filename)
    full_map = np.array(im)
    samples = []
    for co in coordinates:
        sample = full_map[co[0]-size[0]:co[0]+size[0],co[1]-size[1]:co[1]+size[1]]
        samples.append(sample)
    return samples


def analyze_sample(sample):
    mini = sample.min()
    maxi = sample.max()
    avg = sample.mean()
    stdev = sample.std()
    # TODO: calc slopes
    return [mini, maxi, avg, stdev]


def analyze_samples(samples):
    result = []
    for sample in samples:
        result.append(analyze_sample(sample))
    return result
