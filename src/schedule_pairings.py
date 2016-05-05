from __future__ import print_function
from days_and_times import *

def print_availability(a):
    for d in days_of_week:
        print(d)
        for t in time_slots:
            if t in a[d]:
                print(t + ": " + repr(a[d][t]))

        print("")


def schedule(pairings):
    final_schedule = {}
    lessons_per_day = len(pairings) / len(days_of_week)
    for d in days_of_week:
        lessons_today = lessons_per_day
        final_schedule[d] = {}
        for t in time_slots:
            if lessons_today == 0:
                break

            for p in pairings:
                if p.is_available_at(d, t):
                    lessons_today -= 1
                    pairings.remove(p)
                    final_schedule[d][t] = p
                    break

    print_availability(final_schedule)
    return final_schedule





