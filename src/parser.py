from matcher import Person
from days_and_times import *

def read_names(file_name, are_heelers=False, is_file_object=False):
    """
    Reads in a tab-separated file (TSV) with people's information and converts them to
    instances of the Person class.

    params
        file_name: name of the file as a string

    returns a list of the Person instances created
    """
    if not is_file_object:
        fd = open(file_name, 'r')
    else:
        fd = file_name

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



