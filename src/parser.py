from matcher import Person
from days_and_times import *
import misc
import re

def parse_columns(columns):
    indices = {}
    index = 0
    for column in columns:
        column = column.strip().lower()

        if re.search('name', column):
            indices['name'] = index
        elif re.search('netid', column):
            indices['netid'] = index
        elif re.search('year', column):
            indices['year'] = index
        elif re.search('musical experience', column):
            indices['musical_exp'] = index
        elif re.search('known students', column):
            indices['known_students'] = index
        elif re.search('sunday', column):
            indices['sunday'] = index
        elif re.search('monday', column):
            indices['monday'] = index
        elif re.search('tuesday', column):
            indices['tuesday'] = index
        elif re.search('wednesday', column):
            indices['wednesday'] = index
        elif re.search('thursday', column):
            indices['thursday'] = index
        elif re.search('friday', column):
            indices['friday'] = index
        elif re.search('saturday', column):
            indices['saturday'] = index

        index += 1

    return indices



def read_names(file_name, are_students=True):
    """
    Reads in a tab-separated file (TSV) with people's information and converts them to
    instances of the Person class.

    params
        file_name: name of the file as a string

    returns a list of the Person instances created
    """
    fd = open(file_name, 'r')

    group = []

    # parse first line (column names)
    indices = parse_columns(fd.readline().split("\t"))


    indices_days = [indices['sunday'], indices['monday'], indices['tuesday'],
                    indices['wednesday'], indices['thursday'], indices['friday'],
                    indices['saturday']]

    for line in fd:
        attributes = line.split("\t")
        name = attributes[indices['name']]
        netid = attributes[indices['netid']]
        year = years[attributes[indices['year']]]

        if are_students:
            musical_exp = int(attributes[indices['musical_exp']])

        if not are_students:
            known_students = [x.strip() for x in attributes[indices['known_students']].split(',')]
            for known_student in known_students:
                misc.forbidden.append((netid, known_student))



        availability = {}
        for i in range(7):
            times = [x.strip() for x in attributes[indices_days[i]].split(',')]

            available_map = {}
            for t in time_slots:
                if t in times:
                    available_map[t] = 1
                else:
                    available_map[t] = 0

            day_name = days_of_week[i]
            availability[day_name] = available_map

        if are_students:
            person = Person(availability, name, netid, musical_exp=musical_exp, year=year)
        else:
            person = Person(availability, name, netid, year=year)
        group.append(person)

    return group



