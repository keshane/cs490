from __future__ import print_function
from days_and_times import *

def print_availability(a):
    for d in days_of_week:
        print(d)
        for t in time_slots:
            if not a[d][t] == None:
                print(t + ": " + repr(a[d][t]))

        print("")


def schedule(pairings):
    final_schedule = {}
    for d in days_of_week:
        final_schedule[d] = {}
        for t in time_slots:
            final_schedule[d][t] = None

            for p in pairings:
                if p.is_available_at(d, t):
                    pairings.remove(p)
                    final_schedule[d][t] = p
                    break

    print_availability(final_schedule)





