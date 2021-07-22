import os
from src.satellite_parser import GF5Satellite

base_path = 'C:\\Users\\chine\\Downloads\\高分样例数据'

for file in os.listdir(base_path):
    if file.startswith('GF5_'):
        print(file)
        satellite = GF5Satellite(file, os.path.join(base_path, file))
        if hasattr(satellite, 'meta'):
            print(satellite.meta)
            print(satellite.image_name)
            print(satellite.xml_name)
            print(satellite.generate_nid())
