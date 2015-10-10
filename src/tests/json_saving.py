# -*- coding: utf-8 -*-
import json

data = {"Fullscreen": True, "pos_x": 0.3462345254}

data_json = json.dumps(data, indent=12)
print((data_json))
file_obj = open("test1.json", "rw+")
json.dump(data, file_obj)
file_obj.close()

file_obj = open("test1.json", "r")
read_data = json.load(file_obj)
print type(read_data["Fullscreen"])