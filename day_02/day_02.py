# open file, collect content and split into two columns
le_filename = "day_02_input.txt"
le_file = open(le_filename, "r")
le_lines = le_file.readlines()
le_table = [[int(j) for j in e.split()] for e in le_lines] # this time, perform conversion to int directly in assignment to le_table

def line_is_good(line) :
    direction = -1
    line_good = True
    if (line[0] < line[1]) :
        direction = 1
    for i in range(len(line) - 1) :
        if not(1 <= ((line[i+1] - line[i]) * direction) <= 3) :
            line_good = False
    return line_good

good_lines_count = 0
for line in le_table :
    if (line_is_good(line)) :
        good_lines_count += 1

print("Total number of good reports :\n", good_lines_count, sep = "")

######
# PART 2
######

def line_is_good_tolerant(line) :
    line_good = line_is_good(line)
    if (line_good) :
        return True
    for i in range(len(line)) :
        if (line_is_good(line[:i] + line[i+1:])) :
            return True
    return False

good_lines_count_tolerant = 0
for line in le_table :
    if (line_is_good_tolerant(line)) :
        good_lines_count_tolerant += 1

print("Total number of good reports, when tolerating one bad level per report :\n", good_lines_count_tolerant, sep = "")