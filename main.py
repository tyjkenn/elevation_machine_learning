import dem_reader as dr
from sklearn.naive_bayes import GaussianNB
import random as rd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
from sklearn.cluster import KMeans


# increases the size of the coordinate list by varying
# the given coordinates uniformly no further than dev
# latitude or longitude away
def vary_coordinates(coords, classes, times, dev):
    new_coords = []
    new_class = []
    for i in range(len(coords)):
        for j in range(times):
            new_coords.append((coords[i][0] + rd.uniform(-dev, dev), coords[i][1] + rd.uniform(-dev, dev)))
            new_class.append(classes[i])
    return new_coords, new_class


def get_coord_grid(minLat, minLon, maxLat, maxLon, size):
    coords = []
    i = minLat + size
    while i < maxLat - size:
        coord_row = []
        j = minLon + size
        while j < maxLon - size:
            coord_row.append((i, j))
            j += size * 2
        coords.append(coord_row)
        i += size * 2
    return coords


def map_classifications(model, sample_width):
    coords = get_coord_grid(30, -120, 50, -90, .1)
    samples = dr.get_samples('30n120w_20101117_gmted_max075.tif', coords, (sample_width, sample_width))
    data = dr.analyze_samples(samples)
    dr.draw_class_map("classification_map.png", data, model, ['mountain', 'plains', 'canyon', 'random'])


def make_cluster_map(cluster_count, sample_width):
    coords = get_coord_grid(30, -120, 50, -90, sample_width)
    samples = dr.get_samples('30n120w_20101117_gmted_max075.tif', coords, (sample_width, sample_width))
    data = dr.analyze_samples(samples)
    model = KMeans(n_clusters=cluster_count).fit([item for sublist in data for item in sublist])
    dr.draw_class_map("cluster_map.png", data, model, range(cluster_count))


def add_random_samples(samples, classes, count):
    rdmaps = np.asarray([[[rd.randrange(0, 2000) for i in range(120)] for j in range(120)] for k in range(count)])
    samples.extend(rdmaps)
    classes.extend(['random'] * count)


# tuples of latitude followed by longitude. Note that
# north and east are the positive directions
coordinates = [
    (36.0544, -112.1401),  # grand canyon
    (44.4280, -110.5885),  # yellowstone
    (43.7904, -110.6818),  # grand tetons
    (31.5029, -90.9987),   # Homochitto
    (36.2369, -112.6891),  # Supai
    (32.7767, -96.7970),   # Dallas
    (36.2144, -113.0565),  # Toroweap overlook
    (40.8419, -104.0907),  # Pawnee Grassland
    (44.1371, -113.7803),  # Mt. Borah
]


classes = [
    "canyon",
    "mountain",
    "mountain",
    "plains",
    "canyon",
    "plains",
    "canyon",
    "plains",
    "mountain"
]

full_coord, full_class = vary_coordinates(coordinates, classes, 10, .4)

# convert the coordinates into samples, then take summaries of the samples.
# Then split the summaries for training and testing
samples = dr.get_samples('30n120w_20101117_gmted_max075.tif', full_coord, (.1, .1))
add_random_samples(samples, full_class, 10)
data = dr.analyze_samples(samples)
train_data, test_data, train_target, test_target = train_test_split(data, full_class, test_size=.3, train_size=.7, shuffle=True)

# Time to learn!
gnb = GaussianNB()
model = gnb.fit(train_data, train_target)
pred = model.predict(test_data)
score = accuracy_score(test_target, pred)

# Time to score!
print("Score: " + ("%.1f" % (score * 100)) + "%")


# Try some random and flat samples
rdmaps = np.asarray([[[rd.randrange(0, 2000) for i in range(120)] for j in range(120)] for k in range(10)])
flatmaps = np.asarray([[[50 for i in range(120)] for j in range(120)] for k in range(10)])
rddata = dr.analyze_samples(rdmaps)
flatdata = dr.analyze_samples(flatmaps)
rdpred = model.predict(rddata)
flatpred = model.predict(flatdata)
print('Classification of random terrains:')
print(rdpred)
print('Classification of flat samples')
print(flatpred)

# Map based on training
map_classifications(model, .1)

# Try clustering
make_cluster_map(7, 1)
