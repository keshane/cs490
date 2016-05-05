from __future__ import print_function
from days_and_times import *
import random

def print_availability(a):
    for d in days_of_week:
        print(d)
        for t in time_slots:
            if t in a[d]:
                print(t + ": " + repr(a[d][t]))

        print("")


def schedule(final_schedule, pairings, leftovers):
    """
    Schedule the pairings for lessons throughout the week.

    params
        final_schedule: an empty dictionary to put the schedule in
        pairings: the 'tasks' to be scheduled
        leftovers: a list where pairings that couldn't be scheduled will be put

    returns True if all pairings could be scheduled, False otherwise


    final_schedule[d][t] returns the pairing at that time, where
    d is day of the week and t is the time slot
    """
    lessons_per_day = len(pairings) / len(days_of_week)
    for d in days_of_week:
        # this variable helps to spread lessons out across
        # the week. This may lead to some pairings
        # not being able to get scheduled, but
        # reschedule should be able to schedule them.
        # The + 2 is arbitrary to allow some leeway
        #
        # If we DO want to bias lessons times toward particular days
        # the days_of_week list in days_and_times.py can be rearranged
        # and the lessons_today deleted
        lessons_today = lessons_per_day + 2
        final_schedule[d] = {}

        # reduce bias for early in the morning
        t_s = time_slots[:]
        random.shuffle(t_s)
        for t in t_s:
            if lessons_today == 0:
                break

            for p in pairings:
                if p.is_available_at(d, t):
                    lessons_today -= 1
                    pairings.remove(p)
                    final_schedule[d][t] = p
                    break
    if pairings:
        print("reschedule")
        leftovers.extend(pairings[:])
        return False
    else:
        return True

def reschedule(failed_schedule, pairings, leftovers):
    """
    Schedule pairings in an existing schedule.

    params
        failed_schedule: existing schedule made by the schedule() function
        pairings: the 'tasks' to be scheduled
        leftovers: a list where pairings that couldn't be scheduled will be put

    returns True if all pairings could be scheduled, False otherwise

    This function is less strict about spreading lessons evenly across the week
    """
    for d in days_of_week:
        for t in time_slots:
            for p in pairings:
                if p.is_available_at(d, t) and not t in failed_schedule[d]:
                    pairings.remove(p)
                    failed_schedule[d][t] = p
                    break

    if pairings:
        print("reschedule")
        leftovers.extend(pairings[:])
        return False 
    else:
        return True 






