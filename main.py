import dem_reader as dr
from sklearn.naive_bayes import GaussianNB

train = [
    (36.0544, -112.1401),  # grand canyon
    (44.4280, -110.5885),  # yellowstone
    (43.7904, -110.6818),  # grand tetons
    (31.5029, -90.9987),   # Homochitto
    (36.2369, -112.6891),  # Supai
    (32.7767, -96.7970),   # Dallas
]

test = [
    (36.2144, -113.0565),  # Toroweap overlook
    (40.8419, -104.0907),  # Pawnee Grassland
    (44.1371, -113.7803),  # Mt. Borah
]

class_train = [
    "canyon",
    "mountain",
    "mountain",
    "plains",
    "canyon",
    "plains"
]

class_test = [
    "canyon",
    "plains",
    "mountain"
]

train_samples = dr.get_samples('30n120w_20101117_gmted_max075.tif', train, (.25, .25))
test_samples = dr.get_samples('30n120w_20101117_gmted_max075.tif', test, (.25, .25))
train_data = dr.analyze_samples(train_samples)
test_data = dr.analyze_samples(test_samples)

gnb = GaussianNB()
pred = gnb.fit(train_data, class_train).predict(test_data)


print(pred)
