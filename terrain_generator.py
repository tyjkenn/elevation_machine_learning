from random import randint, gauss
import numpy as np
# random datasets within a range
### https://stackoverflow.com/questions/48875494/in-python-how-do-i-generate-random-data-sets-within-a-range-that-follow-a-func

# random image generator PIL script
### https://www.daniweb.com/programming/software-development/threads/488949/looking-for-random-image-generator-pil-script

# How do I generate data using a Naive Bayes model?
### https://www.quora.com/How-do-I-generate-data-using-a-Naive-Bayes-model

# >>> This is just useful <<<
### https://communities.sas.com/t5/General-SAS-Programming/using-rand-function-to-generate-random-numbers-based-on/td-p/329514

# Generating a gaussian distribution with only positive numbers
### https://stackoverflow.com/questions/1683461/generating-a-gaussian-distribution-with-only-positive-numbers

test_classes = ["canyon", "mountain", "plains", "random"]

class TerrainGenerator:
    """class for the terrain generator"""
    def __init__(self, sigma, theta, classes):
        self._classes=classes
        self._sigma=sigma # variance
        self._theta=theta # mean

    def _gen_random_data(self):
        """generate random data given the classes"""
        n = 100
        # hard coding to index 1 to generate mountains
        print(self._theta[1])
        # eventually get rid of the hard-coded [0]
        return np.random.normal(loc=self._theta[1][0], scale=self._sigma[1][0], size=(n,n))

    ## box muller method to generate random data for each random class

    ## turn random data into a TIF image, appending to the last TIF image generated

def test(size):
    tg = TerrainGenerator(None, None, test_classes)
