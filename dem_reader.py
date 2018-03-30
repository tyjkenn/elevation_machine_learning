from PIL import Image
import numpy as np
import plotly
import plotly.graph_objs as go
import random as rd


def convert_coordinates(coordinates):
    for i in range(len(coordinates)):
        if isinstance(coordinates[i], list):
            convert_coordinates(coordinates[i])
        else:
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


def get_samples(dem, coordinates, size):
    if isinstance(dem, str):
        convert_coordinates(coordinates)
        size = get_new_size(size)
        Image.MAX_IMAGE_PIXELS = 1000000000
        im = Image.open(dem)
        full_map = np.array(im)
    else:
        full_map = dem
    samples = []
    for co in coordinates:
        if isinstance(co, list):
            samples.append(get_samples(full_map, co, size))
        else:
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
    return [mini, maxi, avg, stdev, slope_std, steep_count / 100]


def analyze_samples(samples):
    result = []
    for sample in samples:
        if isinstance(sample, list):
            result.append(analyze_samples(sample))
        else:
            result.append(analyze_sample(sample))
    return result


def pick_colors(classes):
    colors = []
    for i in range(len(classes)):
        color = (rd.randrange(0, 256), rd.randrange(0, 256), rd.randrange(0, 256))
        colors.append(color)
    return colors


def draw_class_map(filename, sample_map, model, classes):
    colors = pick_colors(classes)
    im = Image.new("RGB", (len(sample_map[0]), len(sample_map)), "white")
    for i in range(len(sample_map)):
        for j in range(len(sample_map[i])):
            pred = model.predict([sample_map[i][j]])[0]
            color = colors[classes.index(pred)]
            im.putpixel((j, len(sample_map) - i - 1), color)
    im.save(filename, "PNG")
    return im