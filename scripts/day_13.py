import helpers
import re
import math as m

# open file, collect content
le_filename = "../inputs/day_13_input.txt"
le_file_content = helpers.get_file_content_raw(le_filename)
le_test_content = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""

######
# PART 1
######

le_number_regex = """[0-9]+"""
a_cost = 3
b_cost = 1

def parse_machine_list_input(input) :
  le_machine_data_list = [] # format of data for each element in list : ((A.x, A.y), (B.x, B.y), (Prize.x, Prize.y))
  le_separated_input = [machine.split("\n") for machine in input.split("\n\n")]
  for machine_input in le_separated_input :
    a_line = machine_input[0]
    b_line = machine_input[1]
    p_line = machine_input[2]
    a_x = int(re.findall(le_number_regex, a_line)[0])
    a_y = int(re.findall(le_number_regex, a_line)[1])
    b_x = int(re.findall(le_number_regex, b_line)[0])
    b_y = int(re.findall(le_number_regex, b_line)[1])
    p_x = int(re.findall(le_number_regex, p_line)[0])
    p_y = int(re.findall(le_number_regex, p_line)[1])
    le_machine_data_list.append(((a_x, a_y), (b_x, b_y), (p_x, p_y)))
  return le_machine_data_list

def machine_winnable(machine_data) :
  a_x, a_y = machine_data[0]
  b_x, b_y = machine_data[1]
  p_x, p_y = machine_data[2]
  # Option 1 : use GCD, which is fast, but not entirely accurate (doesn't take rule of
  # using less than 100 button presses into account)
  # if p_x % (m.gcd(a_x, b_x)) != 0 :
  #   return False
  # if p_y % (m.gcd(a_y, b_y)) != 0 :
  #   return False
  # return True
  # Option 2 : do it manually, and count button presses
  curr_a_x = -a_x
  for i in range(0, min(101, p_x//a_x + 1)) :
    curr_a_x = i * a_x
    b_mul = (p_x - curr_a_x) // b_x
    if b_mul + i <= 100 and curr_a_x + b_mul * b_x == p_x and a_y * i + b_mul * b_y == p_y :
      return True
  return False

def find_min_cost(machine_data, a_cost = a_cost, b_cost = b_cost) :
  a_x, a_y = machine_data[0]
  b_x, b_y = machine_data[1]
  p_x, p_y = machine_data[2]
  winning_cost = -1
  curr_a_x = -a_x
  for i in range(0, min(101, p_x//a_x + 1)) :
    curr_a_x = i * a_x
    b_mul = (p_x - curr_a_x) // b_x
    if b_mul <= 100 and curr_a_x + b_mul * b_x == p_x and a_y * i + b_mul * b_y == p_y :
      new_price = i * a_cost + b_mul * b_cost
      if winning_cost == -1 or winning_cost < new_price :
        winning_cost = new_price
  return winning_cost

def find_min_cost_all_machines(machine_data_list, a_cost = a_cost, b_cost = b_cost) :
  total_min_cost = 0
  for machine_data in machine_data_list :
    machine_min_cost = find_min_cost(machine_data, a_cost, b_cost)
    if machine_min_cost > -1 :
      total_min_cost += machine_min_cost
  return total_min_cost

helpers.LOG_DICT["T"] = [False, "[TESTING]"]
helpers.LOG_DICT["PARSING"] = [False, "[PARSING]"]

le_machine_data_list = parse_machine_list_input(le_file_content)
le_test_data_list = parse_machine_list_input(le_test_content)

helpers.print_log_entries("le_machine_data_list :", le_machine_data_list, log_cats = {"PARSING"})
helpers.print_log_entries("le_test_data_list :", le_test_data_list, log_cats = {"PARSING"})

helpers.print_log_entries("Min cost for all machines (test) :", find_min_cost_all_machines(le_test_data_list), log_cats = {"T"})
helpers.print_log_entries("Min cost for all machines :", find_min_cost_all_machines(le_machine_data_list), log_cats = {"R"})

######
# PART 2
######

def parse_machine_list_input_corrected(input) :
  le_machine_data_list = [] # format of data for each element in list : ((A.x, A.y), (B.x, B.y), (Prize.x, Prize.y))
  le_separated_input = [machine.split("\n") for machine in input.split("\n\n")]
  for machine_input in le_separated_input :
    a_line = machine_input[0]
    b_line = machine_input[1]
    p_line = machine_input[2]
    a_x = int(re.findall(le_number_regex, a_line)[0])
    a_y = int(re.findall(le_number_regex, a_line)[1])
    b_x = int(re.findall(le_number_regex, b_line)[0])
    b_y = int(re.findall(le_number_regex, b_line)[1])
    p_x = int(re.findall(le_number_regex, p_line)[0]) + 10000000000000
    p_y = int(re.findall(le_number_regex, p_line)[1]) + 10000000000000
    le_machine_data_list.append(((a_x, a_y), (b_x, b_y), (p_x, p_y)))
  return le_machine_data_list

# Note : this was taken from here :
# https://medium.com/@kilichbekhaydarov/the-greatest-common-divisor-in-python-fc77cc38a70a
# return (g, x, y) a*x + b*y = gcd(x, y)
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)

def find_min_cost_corrected(machine_data, a_cost = a_cost, b_cost = b_cost) :
  a_x, a_y = machine_data[0]
  b_x, b_y = machine_data[1]
  p_x, p_y = machine_data[2]
  # work with assumption that button B costs the least
  if a_cost < b_cost :
    a_x, a_y, b_x, b_y = b_x, b_y, a_x, a_y
    a_cost, b_cost = b_cost, a_cost
  helpers.print_log_entries("find_min_cost_corrected() - machine_data :", machine_data, log_cats = {"D"})
  helpers.print_log_entries("a_x, a_y, b_x, b_y, p_x, p_y :", "{}, {}\n{}, {}\n{}, {}"\
    .format(a_x, a_y, b_x, b_y, p_x, p_y), log_cats = {"D"})
  _gcd, a_coef, b_coef = egcd(a_x, b_x)
  helpers.print_log_entries("_gcd, a_coef, b_coef :", "{}, {}, {}".format(_gcd, a_coef, b_coef), log_cats = {"D"})
  if p_x % _gcd != 0 :
    helpers.print_log_entries("find_min_cost_corrected() - unsolvable because p_x"\
                              " % _gcd != 0 !", log_cats = {"UNSOLV"})
    return -1
  # a_mul, b_mul = 0, 0
  # first, reach result for X-coordinate, using GCD
  a_mul = a_coef * p_x // _gcd
  b_mul = b_coef * p_x // _gcd
  x_diff = p_x - (a_mul * a_x + b_mul * b_x)
  if x_diff != 0 :
    raise Exception("find_min_cost_corrected() error : x_diff should be = 0 ! (found {} instead)".format(x_diff))
  else :
    # then, correct for Y, while trying to keep b_mul as high as possible/a_mul as low as possible
    # Note : only one is possible, actually :
    # Either we're correcting for Y, but there's only one solution, or we're trying to lower a_mul,
    # in which case the multiplication coefficient should already be correct for Y
    # (at least I think)
    y_diff = p_y - (a_mul * a_y + b_mul * b_y)
    helpers.print_log_entries("y_diff : {}".format(y_diff), log_cats = {"D"})
    a_mul_step_size = abs(b_x // _gcd) # step to keep x_diff constant
    b_mul_step_size = abs(a_x // _gcd) # step to keep x_diff constant
    y_diff_step_size = b_y * b_mul_step_size - a_y * a_mul_step_size # how much y_diff can change while keeping x_diff constant
    if y_diff_step_size == 0 :
      # Case 1 : can't change y_diff, so should already be at 0 --> try minimize cost
      # if not correct for Y, i.e. y_diff != 0, return -1
      if y_diff != 0 :
        helpers.print_log_entries("find_min_cost_corrected() - unsolvable"\
          "because y_diff_step_size == 0, but y_diff = 0 !", log_cats = {"UNSOLV"})
        return -1
      # otherwise, we can keep both x_diff and y_diff at 0
      # --> find _mul coefs that minimize cost
      else :
        step_count = m.ceil(a_mul // a_mul_step_size)
        # a_mul -= step_count * a_mul_step_size
        # b_mul -= step_count * b_mul_step_size
        # return a_mul * a_cost + b_mul * b_cost
    else :
      # Case 2 : can change y diff --> there should be a unique solution
      # we have to be reach 0 from y_diff using steps of size y_diff_step_size
      if y_diff % y_diff_step_size != 0 :
        helpers.print_log_entries("find_min_cost_corrected() - unsolvable"\
          " because y_diff % y_diff_step_size != 0 !", log_cats = {"UNSOLV"})
        return -1
      else :
        step_count = y_diff // y_diff_step_size
      pass
    # finally, tweak _mul coefs while keeping x_diff = 0
    a_mul -= step_count * a_mul_step_size
    b_mul += step_count * b_mul_step_size
    res = a_mul * a_cost + b_mul * b_cost
    helpers.print_log_entries("find_min_cost_corrected() - solved with result {}".format(res)\
      + " (a_mul = {}, b_mul = {})".format(a_mul, b_mul), log_cats = {"SOLVED"})
    return res

# def quick_test(machine_data_list, a_cost = a_cost, b_cost = b_cost) :
#   for machine_data in machine_data_list :
#     a_x, a_y = machine_data[0]
#     b_x, b_y = machine_data[1]
#     if a_x * b_y == a_y * b_x :
#       print("Found one !")
#     else :
#       print(".", end = "")

def find_min_cost_all_machines_corrected(machine_data_list, a_cost = a_cost, b_cost = b_cost) :
  total_min_cost = 0
  for machine_data in machine_data_list :
    machine_min_cost = find_min_cost_corrected(machine_data, a_cost, b_cost)
    if machine_min_cost > -1 :
      total_min_cost += machine_min_cost
  return total_min_cost

le_machine_data_list_corrected = parse_machine_list_input_corrected(le_file_content)
le_test_data_list_corrected = parse_machine_list_input_corrected(le_test_content)

helpers.LOG_DICT["D"] = [False, "[DEBUG]"]
helpers.LOG_DICT["UNSOLV"] = [False, "[UNSOLVED]"]
helpers.LOG_DICT["SOLVED"] = [False, "[SOLVED]"]
helpers.LOG_DICT["PARSING"] = [False, "[PARSING]"]

helpers.print_log_entries("le_test_data_list :", le_test_data_list, log_cats = {"PARSING"})

helpers.print_log_entries("Min cost for all machines, corrected (test) :", \
  find_min_cost_all_machines_corrected(le_test_data_list), log_cats = {"T"})
helpers.print_log_entries("Min cost for all machines, corrected :", \
  find_min_cost_all_machines_corrected(le_machine_data_list_corrected), log_cats = {"R"})

# quick_test(le_machine_data_list_corrected)