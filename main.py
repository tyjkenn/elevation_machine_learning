import dem_reader as dr
import terrain_generator as tg
from sklearn.naive_bayes import GaussianNB
import random as rd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def vary_coordinates(coords, classes, times, dev):
    new_coords = []
    new_class = []
    for i in range(len(coords)):
        for j in range(times):
            new_coords.append((coords[i][0] + rd.uniform(-dev, dev), coords[i][1] + rd.uniform(-dev, dev)))
            new_class.append(classes[i])
    return new_coords, new_class


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

samples = dr.get_samples('30n120w_20101117_gmted_max075.tif', full_coord, (.25, .25))
data = dr.analyze_samples(samples)

train_data, test_data, train_target, test_target = train_test_split(data, full_class, test_size=.3, train_size=.7, shuffle=True)

gnb = GaussianNB()
pred = gnb.fit(train_data, train_target).predict(test_data)
score = accuracy_score(test_target, pred)

print("Score: " + ("%.1f" % (score * 100)) + "%")
