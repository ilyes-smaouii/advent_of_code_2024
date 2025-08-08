# open file, collect content and split into two columns
le_filename = "day_01_input.txt"
le_file = open(le_filename, "r")
le_lines = le_file.readlines()
le_table = [e.split() for e in le_lines]

# store colums separately and convert them to int
left_col = [int(e[0]) for e in le_table]
left_col.sort()
right_col = [int(e[1]) for e in le_table]
right_col.sort()

# compute total distance by cycling through lines
total_dist = 0
for i in range(len(left_col)) :
    total_dist += abs(left_col[i] - right_col[i])

print("Total distance :", total_dist)

######
# PART 2 #
######

total_sim = 0
count_dict = {}

for e in right_col :
    if (e not in count_dict) :
        count_dict[e] = 1
    else :
        count_dict[e] += 1

for e in left_col :
    if (e in count_dict) :
        total_sim += e * count_dict[e]

print("Total similarity :", total_sim)