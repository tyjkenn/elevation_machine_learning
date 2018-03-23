from PIL import Image
import numpy as np
import plotly
import plotly.graph_objs as go


def convert_coordinates(coordinates):
    for i in range(len(coordinates)):
        coordinates[i] = (int((50 - coordinates[i][0]) * 480), int((coordinates[i][1] + 90) * 480))


def get_new_size(size):
    return int(size[0] * 480), int(size[1] * 480)


def display_sample(sample):
    img = Image.fromarray(sample, 'I')
    img = img.point(lambda p: p * 0.5)
    img.show()


def display_sample_3d(sample):
    data = [
        go.Surface(
            z=sample
        )
    ]
    layout = go.Layout(
        title='Elevation',
        autosize=False,
        width=1000,
        height=1000,
        margin=dict(
            l=65,
            r=50,
            b=65,
            t=90
        )
    )
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig)


def get_samples(filename, coordinates, size):
    convert_coordinates(coordinates)
    size = get_new_size(size)
    Image.MAX_IMAGE_PIXELS = 1000000000
    im = Image.open(filename)
    full_map = np.array(im)
    samples = []
    for co in coordinates:
        sample = full_map[co[0]-size[0]:co[0]+size[0], co[1]-size[1]:co[1]+size[1]]
        samples.append(sample)
    # test sample
    # display_sample_3d(sample)
    return samples


def calc_slopes(sample):
    slopes = []
    for x in range(sample.shape[0] - 1):
        for y in range(sample.shape[1] - 1):
            new_slopes = [
                sample[x, y] - sample[x - 1, y - 1],
                sample[x, y] - sample[x + 1, y - 1],
                sample[x, y] - sample[x - 1, y + 1],
                sample[x, y] - sample[x + 1, y + 1]
            ]
            slopes.extend(new_slopes)
    return slopes


def analyze_sample(sample):
    mini = sample.min()
    maxi = sample.max()
    avg = sample.mean()
    stdev = sample.std()
    slopes = calc_slopes(sample)
    slope_std = np.std(slopes)
    steep_count = 0
    for slope in slopes:
        if slope >= 50:
            steep_count += 1
    return [mini, maxi, avg, stdev, slope_std, steep_count]


def analyze_samples(samples):
    result = []
    for sample in samples:
        result.append(analyze_sample(sample))
    return result
