import helpers
import copy

# open file, collect content
le_filename = "../inputs/day_14_input.txt"
# le_file_content = helpers.get_file_content_raw(le_filename)
le_lines = helpers.get_file_content_as_lines(le_filename)
# le_char_table = helpers.get_file_content_as_table(le_filename)
le_test_lines = helpers.raw_to_lines("""......2..1.
...........
1..........
.11........
.....1.....
...12......
.1....1....""")

######
# PART 1
######

le_width = 101
le_height = 103

def get_data_list(lines) :
  data_list = []
  for line in lines :
    pos_str, vel_str = [elem.split("=")[1] for elem in line.split(" ")]
    pos_x, pos_y = [int(elem) for elem in pos_str.split(",")]
    vel_x, vel_y = [int(elem) for elem in vel_str.split(",")]
    data_list.append(((pos_x, pos_y), (vel_x, vel_y)))
  return data_list

def move_robots(data_list, step_count, width = le_width, height = le_height) :
  # not sure it's relevant to make a deep copy, but this felt like good practice
  data_list_res = []
  for (pos_x, pos_y), (vel_x, vel_y) in data_list :
    new_pos = ((pos_x + step_count * vel_x) % width, (pos_y + step_count * vel_y) % height)
    data_list_res.append((new_pos, (vel_x, vel_y)))
  return data_list_res

def measure_safety_factor(data_list, width = le_width, height = le_height) :
  q1_score, q2_score, q3_score, q4_score = 0, 0, 0, 0
  for (pos_x, pos_y), vel in data_list :
    if pos_x < le_width // 2 :
      if pos_y < le_height // 2 :
        q1_score += 1
      elif pos_y > le_height // 2 :
        q2_score += 1
    elif pos_x > le_width // 2 :
      if pos_y < le_height // 2 :
        q3_score += 1
      elif pos_y > le_height // 2 :
        q4_score += 1
  return q1_score * q2_score * q3_score * q4_score

helpers.LOG_DICT["T"] = [True, "[TESTING]"]

# test_data_list = get_data_list(le_test_lines)
# test_score = measure_safety_factor(test_data_list)

# helpers.print_log_entries("Score for test data :", test_score, log_cats = {"T"})

le_data_list = get_data_list(le_lines)
le_score = measure_safety_factor(move_robots(le_data_list, 100))

helpers.print_log_entries("Final score :", le_score, log_cats = {"R"})

######
# PART 2
######

def display_data_list(data_list, width = le_width, height = le_height) :
  pos_set = set()
  for pos, vel in data_list :
    pos_set.add(pos)
  for row in range(height) :
    for col in range(width) :
      char = " "
      if (col, row) in pos_set :
        char = "0"
      print(char, end = "")
    print("")
  helpers.print_log_entries("pos_set :", pos_set, log_cats = {"D"})

# Explanation for the code below :
# I first ran the first code (the part that's currently commented out)
# I then noticed something happening each 14 + 101k iterations and each 76 + 103k iterations
# I had a hunch trying out some new code (the uncommented one below) might work, which it did
# If it hadn't, I might've tried the same with the "76 + 103k" iterations

# i = 0
# le_char = ""
# while le_char != "s" :
#   display_data_list(move_robots(le_data_list, i))
#   print("{}\n\n".format(i))
#   le_char = input("")
#   i += 1

i = 14
le_char = ""
while le_char != "s" :
  display_data_list(move_robots(le_data_list, i))
  print("{}\n\n".format(i))
  le_char = input("")
  i += 101