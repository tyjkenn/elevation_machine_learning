import dem_reader as dr

samples = dr.get_samples('30n120w_20101117_gmted_max075.tif', [(300, 300)], (100, 100))
analysis = dr.analyze_samples(samples)
print(analysis)
