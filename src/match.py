from __future__ import print_function
import numpy
import sys
import random
import itertools
from collections import defaultdict
from hungarian import Hungarian
import scheduler
from days_and_times import *
from forbidden_pairings import forbidden

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
        person = "%s, %s" % (self.name, self.netid)
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

        if (self.teacher.netid, self.heeler.netid) in forbidden:
            cost += 1000

        if self.teacher.year <= self.heeler.year and self.teacher.year < 4:
            cost += 500
        elif self.teacher.year == 5 and self.heeler.year == 5:
            # reduce cost of graduate students teaching fellow grad students
            # so this will be more likely
            if cost - 100 > 0:
                cost -= 100
            else:
                cost = 0
        elif self.teacher.year <= self.heeler.year and self.teacher.year == 4:
            cost += 20

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






def read_names(file_name, are_heelers=False):
    """
    Reads in a tab-separated file (TSV) with people's information and converts them to
    instances of the Person class.

    params
        file_name: name of the file as a string

    returns a list of the Person instances created
    """
    fd = open(file_name, 'r')
    group = []

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

    return group


def create_pairings(teachers, heelers):
    """
    Create a collection of all possible combinations of (teacher, heeler).

    params
        teachers: list of guildies
        heelers: list of heelers

    returns a dictionary of Pairing objects that's accessed by the repr of
    the teacher concatenated with the repr of the heeler.

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
    """
    Create a cost matrix

    params
        pairings: list of Pairing objects that are all combinations of guildies and heelers
        teachers: list of guildies
        heelers: list of heelers

    returns a cost matrix between the teachers and heelers with padded columns if
    necessary
    """
    num_teachers = len(teachers)

    mat = numpy.zeros(shape=(num_teachers, num_teachers))
    
    for t in range(num_teachers):
        for h in range(num_teachers):
            if h >= len(heelers):
                mat[t][h] = 100000
            else:
                mat[t][h] = pairings[repr(teachers[t]) + repr(heelers[h])].cost

    return mat

def match_teachers_heelers(guildies, heelers, pairings):
    """
    Matching Guildies and Heelers using the Hungarian algorithm.

    params
        guildies: list of Guildies
        heelers: list of Heelers
        pairings: list of Pairing objects that are all combinations of guildies and heelers

    returns a list of pairings that have been matched by the Hungarian algorithm
    """

    low = 0
    matched_pairings = []

    # We sort heelers so that each teacher gets students with a range of
    # musical experience. In each iteration, all the teachers get
    # students with about the same musical experience.
    heelers.sort(key= lambda x: x.musical_exp)
    while low < len(heelers):
        high = min(low+len(guildies), len(heelers))
        heelers_subset = heelers[low:high]
        # if we have failed scheduling, try shuffling the order of the
        # heelers to try to obtain a different set of matched pairings
        random.shuffle(heelers_subset)

        # creates the cost matrix
        matrix = create_matrix(pairings, guildies, heelers_subset)

        if len(heelers_subset) < len(guildies):
            hun = Hungarian(matrix, real_ncols=len(heelers_subset))
        else:
            hun = Hungarian(matrix)
        paired_matrix = hun.run()

        # go through result matrix and extract the pairings that it indicates
        for i in range(paired_matrix.shape[0]):
            for j in range(paired_matrix.shape[1]):
                if paired_matrix[i][j] == Hungarian.STAR:
                    if j >= len(heelers_subset):
                        break
                    matched_pairing = pairings[repr(guildies[i]) + repr(heelers_subset[j])]
                    matched_pairings.append(matched_pairing)

        low = high 

    return matched_pairings


def brute_force(guildies, heelers, final_schedule):
    """
    Warning: Using this function is not recommended.
    This goes through all possible combinations of guildies and heelers.
    It takes forever.
    
    If x and y and lists and len(x) < len(y), this creates
    (y choose x) * x! combinations
    """
    if len(guildies) <= len(heelers):
        print('hi')
        all_pairings = [zip(guildies, x) for x in itertools.permutations(heelers, len(guildies))]
        print(all_pairings)
    else:
        print('hi')
        all_pairings = [zip(x, heelers) for x in itertools.permutations(guildies, len(heelers))]
        print(all_pairings)

    # DISCONTINUED BECAUSE THIS CRASHES MY COMPUTER

def pseudo_brute_force(guildies, heelers, pairings, final_schedule):
    """
    This function is a greedy "brute force" way to assign
    guildies and heelers to an existing schedule. It doesn't
    examine all possible possibilities, though it could certainly
    be made to do so by a calling function.
    """

    for d in days_of_week:
        for t in time_slots:
            # if this time slot is open
            if not t in final_schedule[d]:
                # assign first pair that works
                for g in guildies:
                    for h in heelers:
                        p = pairings[repr(g) + repr(h)]
                        if p.availabilities[d][t] == 1:
                            if p.cost < 1000:
                                final_schedule[d][t] = p
                                heelers.remove(h)



    


guildies_file = sys.argv[1]
heelers_file = sys.argv[2]

guildies = read_names(guildies_file)
heelers = read_names(heelers_file, are_heelers=True)

# pairings is a dictionary that keepss track of all the pairings
pairings = create_pairings(guildies, heelers)

matched_pairings = match_teachers_heelers(guildies, heelers, pairings)


leftover_pairings = []
final_schedule = {}


schedule_success = scheduler.schedule(final_schedule, matched_pairings[:], leftover_pairings)


# The scheduler wasn't able to assign all matched_pairings to a time
if not schedule_success:
    # Only attempts to redo the assignment 11 times
    attempts = 0 
    while not schedule_success:
        leftover_heelers = [x.heeler for x in leftover_pairings]
        leftover_pairings = []
        # Redo assignments for the Heelers left without a lesson time
        rematched_pairings = match_teachers_heelers(guildies, leftover_heelers, pairings)
        schedule_success = scheduler.reschedule(final_schedule, rematched_pairings[:], leftover_pairings)
        attempts += 1
        if attempts > 10:
            # try to stick Heelers wherever we can in the schedule
            pseudo_brute_force(guildies, leftover_heelers, pairings, final_schedule)
            if leftover_heelers:
                # if we get to this point, it means that we would have to try at least a few different
                # combinations of entire permutations of pairings. This would take too long
                # (see the brute_force() function).
                print("""The following Heelers could not be assigned. Finding somewhere to put him/her
                        would take longer than you finding you a teacher to take him/her on.""")
                print(leftover_heelers)
            break

    # do something

# The rest of the code pretty prints everything
scheduler.print_availability(final_schedule)

count = 0
teachers_students_map = defaultdict(list) 
for d in days_of_week:
    for t in time_slots:
        if t in final_schedule[d]:
            p = final_schedule[d][t]
            teachers_students_map[p.teacher].append(p.heeler)
            count += 1

print(count)

for t, l in teachers_students_map.items():
    print("{} {}".format(t, t.year))
    for h in l:
        print("\t{}: {}, {}".format(h, h.musical_exp, h.year))
#for t in guildies:
#    print("{} {}".format(t, t.year))
#    for p in matched_pairings:
#        if p.teacher == t:
#            print("\t{}: {}, {}".format(p.heeler, p.heeler.musical_exp, p.heeler.year))

