import random
import string

days_of_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
time_slots = [ '8:00', '8:30', '9:00', '9:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30',
         '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30',
         '18:00', '18:30', '19:00', '19:30', '20:00', '20:30', '21:00', '21:30', '22:00', '22:30',
         '23:00', '23:30']

file_name = "guildies.tsv"
fd = open(file_name, 'r')
fd.readline()

stats = {}
num_avail_times = {}

for d in days_of_week:
    stats[d] = {}
    num_avail_times[d] = 0

# how many people in total
count = 0
for line in fd:
    attributes = line.split("\t")

    i = 3 # index into day of week in input file
    for d in days_of_week:
        n_times_avail = 0
        times = [x.strip() for x in attributes[i].split(",")]
        for t in time_slots:
            if t in times:
                stats[d][t] = stats[d].get(t, 0) + 1
                n_times_avail += 1
            else:
                stats[d][t] = stats[d].get(t, 0)

        num_avail_times[d] += n_times_avail
        i += 1

    
    count += 1

# divide counts by total number of people
calc_stats = {}
for d in days_of_week:

    day = {}
    num_avail_times[d] = num_avail_times[d] / count

    for time in stats[d]:
        c = stats[d][time]

        day[time] = float(c) / count

    calc_stats[d] = day

print(num_avail_times)

with open('heelers.tsv', 'a') as heeler_file:
    heeler_file.write("blah blah blah first line\r\n")

    for x in range(50):
        name_len = random.randint(3, 10)
        netid_len = random.randint(2, 3)
        name = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(name_len))
        netid = ''.join(random.choice(string.ascii_lowercase) for _ in range(netid_len))
        netid = netid + ''.join(random.choice(string.digits) for _ in range(netid_len))

        line = "2016-05-06\t%s\t%s" % (name, netid)

        for d in days_of_week:
            times = []

            # -2, +2 for variability
            n_times_avail_this_day = random.randint(num_avail_times[d] - 2, num_avail_times[d] + 2)

            # shuffle order of times so that earlier times aren't favored by
            # the num_avail_times
            t_s = time_slots[:]
            random.shuffle(t_s)
            for t in t_s:
                chance = random.random()

                if chance <= calc_stats[d][t] and n_times_avail_this_day > 0:
                    n_times_avail_this_day -= 1
                    times.append(t)

            times.sort()
            line += "\t" + ', '.join(times)

        line += "\r\n"

        heeler_file.write(line)



#print(stats)
#print(calc_stats)
#print(count)



