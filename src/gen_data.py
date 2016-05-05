import random
import math
import string
import numpy
from collections import defaultdict
from days_and_times import *

file_name = "guildies.tsv"
fd = open(file_name, 'r')
fd.readline()

# keeps track of number of students available at a given time slot
stats = {}
num_times_per_day = {}

for d in days_of_week:
    stats[d] = defaultdict(list)
    num_times_per_day[d] = [] 

# how many people in total
count = 0
# keep track of how many times each time slot was chosen
for line in fd:
    attributes = line.split("\t")

    i = 4 # index into day of week in input file
    for d in days_of_week:
        n_times_avail = 0
        times = [x.strip() for x in attributes[i].split(",")]
        for t in time_slots:
            if t in times:
                stats[d][t].append(1)
                n_times_avail += 1
            else:
                stats[d][t].append(0)

        num_times_per_day[d].append(n_times_avail)
        i += 1

    
    count += 1

fd.close()

# divide counts by total number of people
calc_stats = {}
calc_num_times_per_day = {}
for d in days_of_week:
    npy_arr = numpy.array(num_times_per_day[d])
    # sample standard deviation
    std_dev = numpy.std(npy_arr, ddof=1)
    mean = numpy.mean(npy_arr)
    calc_num_times_per_day[d] = (mean, std_dev)

    day = {}
    for t in time_slots:
        day[t] = sum(stats[d][t]) / float(len(stats[d][t])) 

    calc_stats[d] = day

# use results to generate sample heelers 
with open('heelers.tsv', 'w') as heeler_file, open("names/dist.all.last", 'r') as last_file,\
     open("names/dist.all.first", 'r') as first_file:
    num_heelers = 100
    heeler_file.write("blah blah blah first line\r\n")

    # represents freshman, sophomore, graduate/professional student
    possible_years = [1, 2, 5, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
    year_to_class = {1: 'Freshman', 2: 'Sophomore', 5: 'Grad/Prof'}

    for x in range(num_heelers):
        name = first_file.readline().split(" ")[0] + " " + last_file.readline().split(" ")[0]
        netid = name.split(" ")[0][0] + name.split(" ")[1][0]
        netid = netid + ''.join(random.choice(string.digits) for _ in range(2))

        # musical experience ranked from 1 to 10
        # assumes that everyone has a decent amount of musical experience
        musical_exp = int(random.gauss(7, 2))
        if musical_exp > 10:
            musical_exp = 10
        musical_exp = str(musical_exp)

        year = year_to_class[random.choice(possible_years)]

        line = "2016-05-06\t%s\t%s\t%s\t%s" % (name, netid, musical_exp, year)

        for d in days_of_week:
            times = []

            n_times_avail_this_day = random.gauss(calc_num_times_per_day[d][0],
                                                  calc_num_times_per_day[d][1])

            # shuffle order of times so that earlier times aren't favored by
            # the num_times_per_day
            t_s = time_slots[:]
            random.shuffle(t_s)
            for t in t_s:
                chance = random.random()

                if chance <= random.gauss(calc_stats[d][t], math.sqrt(calc_stats[d][t] * (1 - calc_stats[d][t]))) and n_times_avail_this_day > 0:
                    n_times_avail_this_day -= 1
                    times.append(t)

            times.sort()
            line += "\t" + ', '.join(times)

        line += "\r\n"

        heeler_file.write(line)



#print(stats)
#print(calc_stats)
#print(count)



