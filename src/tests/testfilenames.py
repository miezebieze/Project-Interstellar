# -*- coding: utf-8 -*-

#yay new way of implementing the music
#\\ may be used to replace spaces

import os
files = []
for file in os.listdir(".."):
	if file.endswith(".py"):
		files.append(file)
print files