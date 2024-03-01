week = ['Mon', 'Tue', 'Wen', 'Thu', 'Fri', 'Sat', 'Sun']
first_day = 'Thu'
day_count = 29
week_length = len(week)

week_counter = 0
for k in range(week_length):
    if first_day == week[k]:
        break
    else:
        week_counter += 1

row = ''
for i in range(week_length):
    row += ('' if i == 0 else '\t') + week[i]
print(row)

row = ''

for l in range(week_counter):
    row += ('' if l == 0 else '\t')

for j in range(day_count):
    row += ('' if week_counter == 0 else '\t') + str(j + 1)
    if week_counter < 6:
        week_counter += 1
    else:
        week_counter = 0
        print(row)
        row = ''

print(row)
