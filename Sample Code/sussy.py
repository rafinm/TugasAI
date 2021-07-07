import matplotlib.pyplot as plt
import random_forest
import csv

with open('Iris.csv') as csvfile:
    dummy_iris_data = list(csv.reader(csvfile, delimiter=','))

iris_data = list()
for x in dummy_iris_data:
    iris_data.append(x[1:])

del dummy_iris_data
