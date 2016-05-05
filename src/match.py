from __future__ import print_function
import numpy
import sys
import hungarian
import schedule_pairings
from days_and_times import *

def print_availability(a):
    for d in days_of_week:
        print(d)
        for t in time_slots:
            if a[d][t] == 1:
                print(t, end=" ")

        print("")

class Person(object):
    """
    This class represents either a Yale Guild member or a Heeler.

    Attributes:
        availability: a dictionary of lists. key is day of the week. value is list of 0s and 1s
            that indicate whether this person is available during a half-hour duration between
            8:00 AM and 11:30 PM
        name: proper name of this person
        netid: netid
    """

    def __repr__(self):
        person = "Person: %s, %s" % (self.name, self.netid)
        return person

    def __str__(self):
        return self.name

    def __init__(self, availability, name, netid, email='', musical_exp=1, year=3):
        self.availability = availability
        self.name = name
        self.netid = netid
        self.email = email
        self.musical_exp = musical_exp
        self.year = year

class Pairing(object):
    """
    This class represents a pairing between a guild member and a Heeler.

    Attributes:
        heeler: get the Person instance that represents the Heeler
        teacher: get the Person instance that represents the teacher
    """

    def __str__(self):
        return "Pairing(Teacher: %s, Heeler: %s)" % (self.teacher, self.heeler)

    def __repr__(self):
        return "Pairing(Teacher: %s, Heeler: %s)" % (self.teacher, self.heeler)
    def __init__(self, teacher, heeler):
        self.teacher = teacher
        self.heeler = heeler
        self.availabilities = self.add_availabilities(teacher.availability, heeler.availability)

        # calculate cost should always come after add_availabilities()
        self.cost = self.calculate_cost()


    def calculate_cost(self):
        cost = 0
        has_matching_time = False

        for d in days_of_week:
            for t in time_slots:
                if self.availabilities[d][t] == 1:
                    has_matching_time = True
                else:
                    cost += 1

        if not has_matching_time:
            cost += 1000

        if self.teacher.year <= self.heeler.year:
            cost += 500

        return cost
    

    def add_availabilities(self, teacher_availability, heeler_availability):
        availabilities = {}
        for d in days_of_week:
            times = {} 
            for t in time_slots:
                if teacher_availability[d][t] == 1 and heeler_availability[d][t] == 1:
                    times[t] = 1
                else:
                    times[t] = 0

            availabilities[d] = times

        return availabilities

    def is_available_at(self, day, time):
        if self.availabilities[day][time] == 1:
            return True
        else:
            return False






def read_names(file_name, group, are_heelers=False):
    """
    Reads in a tab-separated file (TSV) with people's information and converts them to
    instances of the Person class.

    params
        file_name: name of the file as a string
        group: an empty list in which the instances of Person should be put
    """
    fd = open(file_name, 'r')

    # skip first line (column names)
    fd.readline()

    for line in fd:
        attributes = line.split("\t")
        name = attributes[1]
        netid = attributes[2]

        musical_exp = 0

        if are_heelers:
            musical_exp = int(attributes[3])
            year = years[attributes[4]]
            i = 5
        else:
            year = years[attributes[3]]
            i = 4

        # for real data
        #   email = attributes[3]
        #   i = 4

        availability = {}
        for d in days_of_week:
            times = [x.strip() for x in attributes[i].split(",")]
            available_map = {}

            for t in time_slots:
                if t in times:
                    available_map[t] = 1
                else:
                    available_map[t] = 0

            availability[d] = available_map
            i += 1

        person = Person(availability, name, netid, musical_exp=musical_exp, year=year)
        group.append(person)


def create_pairings(teachers, heelers):
    """
    Calculate the cost of a teacher teaching a Heeler for each pair of teacher and Heeler

    len of teachers < len of heelers
    """

    # key is the concatenations of the repr of the teacher and student
    # value is a Pairing instance
    pairings = {}
    for t in teachers:
        for h in heelers:
            p = Pairing(t, h)
            pairings[repr(t) + repr(h)] = p

    return pairings


def create_matrix(pairings, teachers, heelers):
    if len(teachers) <= len(heelers):
        num_teachers = len(teachers)

        mat = numpy.zeros(shape=(num_teachers, num_teachers))
        
        for t in range(num_teachers):
            for h in range(num_teachers):
                mat[t][h] = pairings[repr(teachers[t]) + repr(heelers[h])].cost

        return mat
    else:
        mat = numpy.zeros(shape=(len(teachers), len(teachers)))

        for t in range(len(teachers)):
            for h in range(len(teachers)):
                if h >= len(heelers):
                    mat[t][h] = 0
                else:
                    mat[t][h] = pairings[repr(teachers[t]) + repr(heelers[h])].cost

        return mat




    


guild_members = []
heelers = []
# 
# read_names('heelers.tsv', heelers)

guildies_file = sys.argv[1]
heelers_file = sys.argv[2]
read_names(guildies_file, guild_members)
read_names(heelers_file, heelers, are_heelers=True)

#for g in guild_members:
#    print(g)
#    print_availability(g.availability)
#for h in heelers:
#    print(h)
#    print_availability(h.availability)

heelers.sort(key= lambda x: x.musical_exp)

pairings = create_pairings(guild_members, heelers)

low = 0
matched_pairings = []
c = 1
print("len of heelers:" + str(len(heelers)))
while low < len(heelers):
    print(c)
    c += 1
    high = min(low+len(guild_members), len(heelers))
    heelers_subset = heelers[low:high]
    matrix = create_matrix(pairings, guild_members, heelers_subset)

    hun = hungarian.Hungarian(matrix)
    paired_matrix = hun.run()

    for i in range(paired_matrix.shape[0]):
        for j in range(paired_matrix.shape[1]):
            if paired_matrix[i][j] == hungarian.Hungarian.STAR:
                if j >= len(heelers_subset):
                    break
                matched_pairing = pairings[repr(guild_members[i]) + repr(heelers_subset[j])]
                matched_pairings.append(matched_pairing)

    low = high 
    print(low)

print(matched_pairings)

schedule_pairings.schedule(matched_pairings)



