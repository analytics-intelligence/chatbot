"""
 Handles cvs data
"""
import csv

question_set = []
training_set = []

with open('./dataset/kadirs.csv', newline='') as read_file:
    data = csv.reader(read_file)
    for row in data:
        question_set.append(row[1])
        training_set.append(row[1])
        training_set.append(row[2])

question_list = question_set
training_list = training_set

