import misc

def teacher_is_higher_year(teacher, student):
    if teacher.year <= student.year and teacher.year < 4:
        return 500
    elif teacher.year == 5 and student.year == 5:
        return -500
    elif teacher.year <= student.year and teacher.year == 4:
        return 20


def teacher_knows_student(teacher, student):
    if (teacher.netid, student.netid) in misc.forbidden_pairings:
        return 1000

def available_at_same_time(teacher, student):
    has_matching_time = False

    cost = 0
    for d in misc.days_of_week:
        for t in misc.time_slots:
            if teacher.availability[d][t] and student.availability[d][t]:
                has_matching_time = True
            else:
                cost += 5

    if not has_matching_time:
        cost += 1000

    return 1000

