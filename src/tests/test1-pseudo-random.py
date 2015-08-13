# -*- coding: utf-8 -*-
import random
import test2pseudorandom as test2

random.seed(1)

alist = []
blist = []

for a in range(10):
	alist.append(random.random())
	blist.append(test2.generate())

print alist
print blist

#A new import doesnt create a new instance!