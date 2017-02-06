from matcher import Person
from days_and_times import *
import misc

index_name = 1
index_netid = 2
index_year = 3
index_musical_exp = 4
index_known_students = 5
index_sunday = 6
index_monday = 7
index_tuesday = 8
index_wednesday = 9
index_thursday = 10 
index_friday = 11 
index_saturday = 12

def parse_columns(columns):
    index = 0
    for column in columns:
        column = column.strip().lower()

        if column == 'name':
            index_name = index
        elif column == 'netid':
            index_netid = index
        elif column == 'year':
            index_year = index
        elif column == 'musical experience':
            index_musical_exp = index
        elif column == 'known students':
            index_known_students = index
        elif column == 'sunday':
            index_sunday = index
        elif column == 'monday':
            index_monday = index
        elif column == 'tuesday':
            index_tuesday = index
        elif column == 'wednesday':
            index_wednesday = index
        elif column == 'thursday':
            index_thursday = index
        elif column == 'friday':
            index_friday = index
        elif column == 'saturday':
            index_saturday = index

        index += 1

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
    parse_columns(fd.readline())

    for line in fd:
        attributes = line.split("\t")
        name = attributes[index_name]
        netid = attributes[index_netid]
        musical_exp = int(attributes[index_musical_exp])
        year = years[attributes[index_year]]

        index_days = [index_sunday, index_monday, index_tuesday,
                      index_wednesday, index_thursday, index_friday,
                      index_saturday]

        if not are_students:
            known_students = [x.strip() for x in attributes[index_known_students].split(',')]
            for known_student in known_students:
                misc.forbidden.append((netid, known_student))


        availability = {}
        for day_index in range(7):
            attribute_index = index_days[day_index]

            times = [x.strip() for x in attributes[attribute_index].split(',')]

            available_map = {}
            for t in time_slots:
                if t in times:
                    available_map[t] = 1
                else:
                    available_map[t] = 0

            day_name = days_of_week[day_index]
            availability[day_name] = available_map

        person = Person(availability, name, netid, musical_exp=musical_exp, year=year)
        group.append(person)

    return group



