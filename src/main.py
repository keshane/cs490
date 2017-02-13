"""
Assigning lessons consists of two parts:
    - matching teachers to students
    - scheduling lessons
"""

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
import matcher
import parser

def main(_guildies_file, _heelers_file):
    guildies_file = _guildies_file
    heelers_file = _heelers_file

    guildies = parser.read_names(guildies_file, are_students=False)
    heelers = parser.read_names(heelers_file, are_students=True)


    # pairings is a dictionary that keeps track of all possible pairings
    pairings = matcher.create_pairings(guildies, heelers)

    # match teachers to heelers
    matched_pairings = matcher.match_teachers_heelers(guildies, heelers, pairings)


    leftover_pairings = []
    final_schedule = {}


    # schedule the matched pairings
    schedule_success = scheduler.schedule(final_schedule, matched_pairings[:], leftover_pairings)


    # The scheduler wasn't able to assign all matched_pairings to a time
    if not schedule_success:
        # Only attempts to redo the assignment 11 times
        attempts = 0 
        attempt_limit = 10
        while not schedule_success:
            leftover_heelers = [x.heeler for x in leftover_pairings]
            leftover_pairings = []
            # Redo assignments for the Heelers left without a lesson time
            rematched_pairings = matcher.match_teachers_heelers(guildies, leftover_heelers, pairings)
            schedule_success = scheduler.reschedule(final_schedule, rematched_pairings[:], leftover_pairings)
            attempts += 1
            if attempts > attempt_limit:
                # try to stick Heelers wherever we can in the schedule
                matcher.pseudo_brute_force(guildies, leftover_heelers, pairings, final_schedule)
                if leftover_heelers:
                    # if we get to this point, it means that we would have to try at least a few different
                    # combinations of entire permutations of pairings. This would take too long
                    # (see the brute_force() function).
                    print("""The following Heelers could not be assigned. Finding somewhere to put him/her
                            would take longer than you finding a teacher to take him/her on.""")
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

