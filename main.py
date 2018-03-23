import dem_reader as dr

sample_coords = [
    (36.0544, -112.1401)  # grand canyon
]

samples = dr.get_samples('30n120w_20101117_gmted_max075.tif', sample_coords, (.5, .5))
analysis = dr.analyze_samples(samples)
print(analysis)
