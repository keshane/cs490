import numpy

days_of_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
time_slots = [ '8:00', '8:30', '9:00', '9:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30',
         '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30',
         '18:00', '18:30', '19:00', '19:30', '20:00', '20:30', '21:00', '21:30', '22:00', '22:30',
         '23:00', '23:30']

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
        person = "Person: %s, %s, %s" % (self.name, self.netid, self.email)
        return person

    def __init__(self, availability, name, netid, email):
        self.availability = availability
        self.name = name
        self.netid = netid
        self.email = email

class Pairing(object):
    """
    This class represents a pairing between a guild member and a Heeler.

    Attributes:
        heeler: get the Person instance that represents the Heeler
        teacher: get the Person instance that represents the teacher
    """

    def __init__(self, teacher, heeler):
        self.teacher = teacher
        self.heeler = heeler
        self.availabilities = add_availabilities(teacher.availability, heeler_availability)

        # calculate cost should always come after add_availabilities()
        self.cost = calculate_cost()


    def calculate_cost(self):
        cost = 0
        has_matching_time = False

        for d in days_of_week:
            for t in range(len(time_slots)):
                if self.availabilities[d][t] == 1:
                    has_matching_time = True
                else:
                    cost += 1

        if not has_matching_time:
            cost += 1000

        return cost
    

    def add_availabilities(self, teacher_availability, heeler_availability):
        availabilities = {}
        for d in days_of_week:
            times = []
            for t in range(len(time_slots)):
                if teacher_availability[d][t] and heeler_availability[d][t]:
                    times.append(1)
                else:
                    times.append(0)

            self.availabilities[d] = times

        return availabilities






def read_names(file_name, group):
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
        email = attributes[3]

        i = 4
        availability = {}
        for d in days_of_week:
            times = attributes[i]
            available_list = []
            for t in time_slots:
                if t in times:
                    available_list.append(1)
                else:
                    available_list.append(0)
            availability[d] = available_list
            i += 1

        person = Person(availability, name, netid, email)
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
            pairings[t.repr() + h.repr()] = p

    return pairings


def create_matrix(pairings, teachers, heelers):
    assert len(teachers) < len(heelers)

    num_teachers = len(teachers)

    teacher_index_map = {}
    heeler_index_map = {}

    mat = numpy.zeros(shape=(num_teachers, num_teachers))
    
    for t in range(num_teachers):
        for h in range(num_teachers):
            mat[t][h] = pairings[teachers[t].repr() + heelers[h].repr()].cost

    return mat

def hungarian(matrix):
    min_costs = numpy.amin(matrix, axis=1)

    matrix = matrix - min_costs.transpose()

    min_costs = numpy.amin(matrix, axis=0)

    matrix = matrix - min_costs

    cols_covered = [False for j in range(matrix.shape[1])]
    rows_covered = [False for j in range(matrix.shape[0])]

    



    


guild_members = []
# heelers = []
# 
# read_names('heelers.tsv', heelers)

read_names('guild_members.tsv', guild_members)




for g in guild_members:
    print(g)
    print(g.availability)






        



