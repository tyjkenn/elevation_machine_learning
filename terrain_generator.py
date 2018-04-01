from random import randint
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
    def __init__(self, classes=None):
        self._classes=classes
        if self._classes == None:
            raise ValueError("no array for classes passed")

    def _gen_random_list_of_classes(self, size):
        """make a random list of classes"""
        random_classes, size_classes = [], len(self._classes)
        for i in range(size):
            random_n = randint(0,size_classes-1)
            random_classes.append(self._classes[random_n])
        return random_classes

def test(size):
    tg = TerrainGenerator(test_classes)
    rc = tg._gen_random_list_of_classes(size)
    print(rc)