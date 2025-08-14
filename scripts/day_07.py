import math as m

# open file, collect content
le_filename = "../inputs/day_07_input.txt"
le_file = open(le_filename, "r")
le_file_content = le_file.read()
# le_file_content = """190: 10 19
# 3267: 81 40 27
# 83: 17 5
# 156: 15 6
# 7290: 6 8 6 15
# 161011: 16 10 13
# 192: 17 8 14
# 21037: 9 7 18 13
# 292: 11 6 16 20"""

######
# PART 1
######

le_equations = []
# first, parse file
for line in le_file_content.split("\n") :
  fst_split = line.split(": ")
  res = int(fst_split[0])
  operands = [int(elem) for elem in fst_split[1].split(" ")]
  le_equations.append((res, operands))
  pass

def try_add_mult(operands, iteration_idx, hint = None) :
  # print("iteration_idx : ", iteration_idx, sep = "") # [debugging]
  res = operands[0]
  for i in range(len(operands) - 1) :
    if iteration_idx%2 == 0 :
      res += operands[i+1]
    else :
      res *= operands[i+1]
    if (res > hint) :
      # print("hint triggered, res : ", res, sep = "") # [debugging]
      return res
    iteration_idx = iteration_idx//2
  # print("operands : ", operands, sep = "") # [debugging]
  # print("hint : ", hint, sep = "") # [debugging]
  # print("res : ", res, sep = "") # [debugging]
  # print("") # [debugging]
  return res

def display_operation(operands, iteration_idx) :
  operation_str = str(operands[0])
  for i in range(len(operands) - 1) :
    if iteration_idx%2 == 0 :
      operation_str += "+" + str(operands[i+1])
    else :
      operation_str += "*" + str(operands[i+1])
    iteration_idx //= 2
  return operation_str

def sum_solvable(equations) :
  solvable_sum = 0
  eq_count = 0
  for hoped_res, operands in equations :
    if (eq_count % 20 == 0) :
      print("Reacher eq_count = ", eq_count, sep = "")
    for i in range(pow(2, len(operands) - 1)) :
      if try_add_mult(operands, i, hoped_res) == hoped_res :
        # print("Found solution !") # [debugging]
        # print("hoped_res, operands, i : ", hoped_res, ", ", operands, ", ", i, sep = "") # [debugging]
        # print("display_operation : ", display_operation(operands, i), sep = "") # [debugging]
        # print("solvable_sum : ", solvable_sum, sep = "") # [debugging]
        solvable_sum += hoped_res
        break
    eq_count += 1
  return solvable_sum

print("Solvable sum : ", sum_solvable(le_equations), sep = "")

######
# PART 2
######

# Assu
def digit_count(number) :
  number = abs(number)
  # if number < 10 :
  #   return 1
  # elif number < 100 :
  #   return 2
  # elif number < 1000 :
  #   return 3
  # elif number < 10000 :
  #   return 4
  # elif number < 100000 :
  #   return 5
  # elif number < 1000000 :
  #   return 6
  # elif number < 10000000 :
  #   return 7
  # elif number < 100000000 :
  #   return 8
  # elif number < 1000000000 :
  #   return 9
  # elif number < 10000000000 :
  #   return 10
  # elif number < 100000000000 :
  #   return 11
  # elif number < 1000000000000 :
  #   return 12
  # elif number < 1000000000000 :
  #   return 13
  # elif number < 1000000000000 :
  #   return 14
  # elif number < 10000000000000 :
  #   return 15
  # else :
  return 1 + int(m.log(number, 10))

def try_add_mult_concat(operands, iteration_idx, hint = None) :
  # print("iteration_idx : ", iteration_idx, sep = "") # [debugging]
  res = operands[0]
  for i in range(len(operands) - 1) :
    if iteration_idx%3 == 0 :
      res += operands[i+1]
    elif iteration_idx%3 == 1:
      res *= operands[i+1]
    else :
      # res = int(str(res) + str(operands[i+1]))
      shift = digit_count(operands[i+1])
      res = res * pow(10, shift) + operands[i+1]
    if (res > hint) :
      # print("hint triggered, res : ", res, sep = "") # [debugging]
      return res
    iteration_idx = iteration_idx//3
  # print("operands : ", operands, sep = "") # [debugging]
  # print("hint : ", hint, sep = "") # [debugging]
  # print("res : ", res, sep = "") # [debugging]
  # print("") # [debugging]
  return res

def display_operation_v2(operands, iteration_idx) :
  operation_str = str(operands[0])
  for i in range(len(operands) - 1) :
    if iteration_idx%3 == 0 :
      operation_str += "+" + str(operands[i+1])
    elif iteration_idx%3 == 1 :
      operation_str += "*" + str(operands[i+1])
    else :
      operation_str += "||" + str(operands[i+1])
    iteration_idx //= 3
  return operation_str

def sum_solvable_v2(equations) :
  solvable_sum = 0
  eq_count = 0
  for hoped_res, operands in equations :
    if (eq_count % 20 == 0) :
      print("Reacher eq_count = ", eq_count, sep = "")
    for i in range(pow(3, len(operands) - 1)) :
      if try_add_mult_concat(operands, i, hoped_res) == hoped_res :
        # print("Found solution !") # [debugging]
        # print("hoped_res, operands, i : ", hoped_res, ", ", operands, ", ", i, sep = "") # [debugging]
        # print("display_operation_v2 : ", display_operation_v2(operands, i), sep = "") # [debugging]
        # print("solvable_sum : ", solvable_sum, sep = "") # [debugging]
        solvable_sum += hoped_res
        break
    eq_count += 1
  return solvable_sum

print("Solvable sum v2 : ", sum_solvable_v2(le_equations), sep = "")