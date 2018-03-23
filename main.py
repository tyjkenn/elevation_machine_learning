import dem_reader as dr

sample_coords = [
    (36.0544, -112.1401),  # grand canyon
    (44.4280, -110.5885),  # yellowstone
    (43.7904, -110.6818),  # grand tetons
    (31.5029, -90.9987),   # Homochitto
]

samples = dr.get_samples('30n120w_20101117_gmted_max075.tif', sample_coords, (.5, .5))
analysis = dr.analyze_samples(samples)
print(analysis)
