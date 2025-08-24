import helpers

# open file, collect content
le_filename = "../inputs/day_17_input.txt"
le_file_content = helpers.get_file_content_raw(le_filename)
# le_lines = helpers.get_file_content_as_lines(le_filename)
# le_char_table = helpers.get_file_content_as_table(le_filename)
le_test_desc = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""

######
# PART 1
######


# Just some notes first :
# 3-bit operators, 3-bit operands
# int registers

# combo :
#   1-3 : self
#   4-6 : registers
#   7 : reserved val

# adv/0 : int(divide reg_A by 2**(combo)) --> reg_A
# bxl/1 : XOR(reg_B, literal) --> reg_B
# bst/2 : combo % 8 --> reg_B
# jnz/3 : A != 0 ? jump(literal) : pass
#   !! no jump by 2 !!
# bxc/4 : XOR(reg_B, reg_C)
#   still consumes operand
# out/5 : combo % 8 --> add to out
# bdv/6 : int(divide reg_A by 2**(combo)) --> reg_B
# cdv/7 : int(divide reg_A by 2**(combo)) --> reg_C

# class ChronoSpatialComputer :
#   def __init__(self, instructions, registers):
#     self._instructions = instructions
#     self._
le_instruction_pointer = 0
le_instructions = []
le_reg_A = 0
le_reg_B = 0
le_reg_C = 0
le_operator_id = 0
le_operand = 1
le_out = []

def literal(operand = le_operand) :
  global le_instruction_pointer, le_reg_A, le_reg_B, le_reg_C, le_instructions, le_operator_id, le_operand, le_out
  return operand

def combo(operand = le_operand) :
  global le_instruction_pointer, le_reg_A, le_reg_B, le_reg_C, le_instructions, le_operator_id, le_operand, le_out
  if 0 <= operand <= 3 :
    return operand
  elif operand == 4 :
    return le_reg_A
  elif operand == 5 :
    return le_reg_B
  elif operand == 6 :
    return le_reg_C
  else :
    raise Exception("Error : invalid combo (operand = {})".format(operand))
#
def adv() :
  global le_instruction_pointer, le_reg_A, le_reg_B, le_reg_C, le_instructions, le_operator_id, le_operand, le_out
  le_reg_A = int(le_reg_A / pow(2, combo(le_operand)))
#
def bdv() :
  global le_instruction_pointer, le_reg_A, le_reg_B, le_reg_C, le_instructions, le_operator_id, le_operand, le_out
  le_reg_B = int(le_reg_A / pow(2, combo(le_operand)))
#
def cdv() :
  global le_instruction_pointer, le_reg_A, le_reg_B, le_reg_C, le_instructions, le_operator_id, le_operand, le_out
  le_reg_C = int(le_reg_A / pow(2, combo(le_operand)))
#
def bxl() :
  global le_instruction_pointer, le_reg_A, le_reg_B, le_reg_C, le_instructions, le_operator_id, le_operand, le_out
  le_reg_B = le_reg_B ^ literal(le_operand)

def bst() :
  global le_instruction_pointer, le_reg_A, le_reg_B, le_reg_C, le_instructions, le_operator_id, le_operand, le_out
  le_reg_B = combo(le_operand) % 8

def jnz() :
  global le_instruction_pointer, le_reg_A, le_reg_B, le_reg_C, le_instructions, le_operator_id, le_operand, le_out
  if le_reg_A != 0 :
    le_instruction_pointer = literal(le_operand)
  else :
    pass

def bxc() :
  global le_instruction_pointer, le_reg_A, le_reg_B, le_reg_C, le_instructions, le_operator_id, le_operand, le_out
  le_reg_B = le_reg_B ^ le_reg_C

def out() :
  global le_instruction_pointer, le_reg_A, le_reg_B, le_reg_C, le_instructions, le_operator_id, le_operand, le_out
  le_out.append(combo(le_operand) % 8)

le_operators = [adv, bxl, bst, jnz, bxc, out, bdv, cdv]

def load_machine(raw_desc) :
  global le_instruction_pointer, le_reg_A, le_reg_B, le_reg_C, le_instructions, le_operator_id, le_operand, le_out
  line_A, line_B, line_C, empty_line, line_program = raw_desc.split("\n")
  le_reg_A = int(line_A[len("Register A: "):])
  le_reg_B = int(line_B[len("Register B: "):])
  le_reg_C = int(line_C[len("Register C: "):])
  # helpers.print_log_entries("line_program[len(\"Program: \"):] : ", line_program[len("Program: "):], log_cats = {"D"})
  le_instructions = [int(e) for e in line_program[len("Program: "):].split(",")]
  le_instruction_pointer = 0
  le_out = []

def run() :
  global le_instruction_pointer, le_reg_A, le_reg_B, le_reg_C, le_instructions, le_operator_id, le_operand, le_out
  # le_instruction_pointer = 0
  # helpers.print_log_entries("le_instructions :", le_instructions, log_cats = {"D"})
  while le_instruction_pointer < len(le_instructions) :
    # helpers.print_log_entries("le_instructions_pointer :", le_instruction_pointer, log_cats = {"D"})
    # helpers.print_log_entries("registers :", le_reg_A, le_reg_B, le_reg_C, log_cats = {"D"})
    le_operator_id = le_instructions[le_instruction_pointer]
    le_operand = le_instructions[le_instruction_pointer + 1]
    operator = le_operators[le_operator_id]
    # helpers.print_log_entries("operator, operand : {}, {}".format(operator, le_operand), log_cats = {"D"})
    operator()
    if operator != jnz or le_reg_A == 0 :
      le_instruction_pointer += 2

helpers.LOG_DICT["D"] = [True, "[DEBUG]"]
helpers.LOG_DICT["T"] = [True, "[TESTING]"]

load_machine(le_file_content)
# load_machine(le_test_desc)
run()

helpers.print_log_entries("le_out : {}".format(le_out), log_cats = "T")
res = ",".join([str(e) for e in le_out])
helpers.print_log_entries("run() result : {}".format(res), log_cats = "R")

######
# PART 2
######

######
# PART 2 - Brute-force attempt
# (ended up using another approach, c.f. later code)
######

def octet_decompose(i) :
  final_str = ""
  while i > 0 :
    final_str = str(i & 7) + "|" + final_str
    i >>= 3
  return "|" + final_str

# i = 0
# while le_instructions != le_out :
#   if i % 100000 == 0 or True :
#     # print("Reached iteration n°{}".format(i))
#     print(octet_decompose(i))
#   load_machine(le_file_content)
#   le_reg_A = i
#   i += 1
#   run()
#   # helpers.print_log_entries(le_instructions, log_cats = {"D"})
#   helpers.print_log_entries(le_out, log_cats = {"D"})

# print("i : {}".format(i))

######
# PART 2 - Notes to prepare for second approach
######

# 2,4,1,3,7,5,4,0,1,3,0,3,5,5,3,0
# 2,4
# 1,3
# 7,5
# 4,0
# 1,3
# 0,3
# 5,5
# 3,0
# bst, 4 --> reg_A % 8 to B --> reg_B = reg_A % 8
# bxl, 3 --> reg_B ^ 3 to B --> reg_B ^= 3
# cdv, 5 --> reg_A >> reg_B to C --> reg_C = reg_A >> reg_B
# bxc, 0 --> reg_B ^ reg_C to B --> reg_B ^= reg_C
# bxl, 3 --> reg_B ^ 3 to B --> reg_B ^= 3
# adv, 3 --> reg_A >> 3 to A --> reg_A = reg_A >> 3
# out, 5 --> reg_B % 8 to out >> out.append(reg_B % 8)
# jnz, 0 --> back to start if reg_A != 0

# Equivalent program (except in the original the loop runs at least once, even if reg_A == 0) :

# while (le_reg_A != 0) :
#   le_reg_B = le_reg_A % 8
#   le_reg_B ^= 3 # flip out last two bits
#   le_reg_C = le_reg_A >> le_reg_B
#   le_reg_B ^= le_reg_C
#   le_reg_B ^= 3 # flip out last two bits again
#   le_reg_A >>= 3
#   le_out.append(le_reg_B % 8)

# # Equivalent program, some interpretation steps later :

# while (le_reg_A != 0) :
#   le_reg_B = (le_reg_A % 8) ^ 3 # flip out last two bits
#   le_reg_C = le_reg_A >> ((le_reg_A % 8) ^ 3)
#   le_reg_B = ((le_reg_A % 8) ^ 3) ^ (le_reg_C) ^ 3
#   le_reg_B ^= 3 # flip out last two bits again
#   le_reg_A >>= 3
#   le_out.append(le_reg_B % 8)

# while (le_reg_A != 0) :
#   curr_word = (le_reg_A % 8) ^ 3 # flip out last two bits
#   le_reg_B = curr_word
#   le_reg_C = le_reg_A >> (curr_word)
#   # le_reg_B = (curr_word) ^ (le_reg_C)
#   le_reg_B = (curr_word) ^ (le_reg_C) ^ 3 # flip out last two bits
#   le_reg_B = (le_reg_A % 8) ^ (le_reg_C)
#   le_reg_B = (curr_word ^ 3) ^ (le_reg_C)
#   le_reg_A >>= 3
#   le_out.append(le_reg_B % 8)

# # Equivalent program, some further interpretation steps later :

# while (le_reg_A != 0) :
#   le_reg_B = ((le_reg_A % 8) ^ 3) ^ (le_reg_A >> ((le_reg_A % 8) ^ 3)) ^ 3
#   le_reg_A >>= 3
#   le_out.append(le_reg_B % 8)


# # A little more :

# while (le_reg_A != 0) :
#   curr_word = (le_reg_A & 7) ^ 3
#   le_reg_B = (curr_word) ^ (le_reg_A >> curr_word)
#   le_reg_B ^= 3
#   le_reg_A >>= 3
#   le_out.append(le_reg_B & 7)

######
# PART 2 - Checking correctness of disassembled code in notes
######

def run2() :
  global le_instruction_pointer, le_reg_A, le_reg_B, le_reg_C, le_instructions, le_operator_id, le_operand, le_out
  if le_reg_A == 0 :
    le_out.append(0)
  while (le_reg_A != 0) :
    curr_word = le_reg_A & 7
    curr_word_xor_3 = curr_word ^ 3
    shifted_reg = le_reg_A >> curr_word_xor_3
    shifted_xored = curr_word_xor_3 ^ shifted_reg
    le_reg_B = shifted_xored ^ 3
    out_word = le_reg_B & 7
    le_reg_A >>= 3
    le_out.append(out_word)

def run2_and_display_res() :
  run2()
  res = ",".join([str(e) for e in le_out])
  return res

def run_and_display_res() :
  run2()
  res = ",".join([str(e) for e in le_out])
  print(res)


load_machine(le_file_content)
run2()
res = ",".join([str(e) for e in le_out])
helpers.print_log_entries("run2() result : {}".format(res), log_cats = "T")

######
# PART 2 - Attempt at findind "reversal" function
######

def get_res_for_reg_A_value(val) :
  global le_reg_A
  load_machine(le_file_content)
  le_reg_A = val
  return run2_and_display_res()

def out_to_reg_A_aux(_out, _last_out_idx, curr_reg_val = 0, recursion_depth = 0) :
  reg_val_list = []
  # for _out_idx in range(_last_out_idx - 1, -1, -1) :
  _out_idx = _last_out_idx - 1
  out_word = _out[_out_idx]
  # found = False
  # helpers.print_log_entries("", log_cats = {"D"})
  # helpers.print_log_entries("out_to_reg_A_aux() - _out, _last_out_idx, out_word, curr_reg_val, recursion_depth :",\
  #   "{}, {}, {}, {}, {}".format(_out, _last_out_idx, out_word, octet_decompose(curr_reg_val), recursion_depth), log_cats = {"D"})
  # helpers.print_log_entries(get_res_for_reg_A_value(curr_reg_val), log_cats = {"D"})
  # helpers.print_log_entries("", , log_cats = {"D"})
  for tmp_curr_word in range(0, 8) :
    tmp_reg_val = (curr_reg_val << 3) | tmp_curr_word
    tmp_curr_word_xor_3 = tmp_curr_word ^ 3
    tmp_shifted_reg = tmp_reg_val >> tmp_curr_word_xor_3
    tmp_shifted_xored = tmp_shifted_reg ^ tmp_curr_word_xor_3
    tmp_b = tmp_shifted_xored ^ 3
    tmp_out_word = tmp_b & 7
    # Need second condition because otherwise re-running program on finding will halt too earl (at reg_A = 0)
    if tmp_out_word == out_word and tmp_reg_val != 0 :
      # reg_val = tmp_reg_val
      if _out_idx == 0 :
        return [tmp_reg_val]
      else :
        reg_val_list = out_to_reg_A_aux(_out, _out_idx, tmp_reg_val, recursion_depth + 1)
    else :
      continue
    if len(reg_val_list) > 0 :
      return reg_val_list
  return reg_val_list

def out_to_reg_A_aux_v2(_out, _last_out_idx, curr_reg_val = 0, recursion_depth = 0) :
  """
  Shorter version of out_to_reg_A_aux()
  """
  reg_val_list = []
  out_word = _out[_last_out_idx - 1]
  for tmp_curr_word in range(0, 8) :
    tmp_reg_val = (curr_reg_val << 3) | tmp_curr_word
    tmp_b = tmp_curr_word ^ (tmp_reg_val >> (tmp_curr_word ^ 3))
    if tmp_b & 7 == out_word and tmp_reg_val != 0 :
      if _last_out_idx - 1 == 0 :
        return [tmp_reg_val]
      else :
        reg_val_list = out_to_reg_A_aux(_out, _last_out_idx - 1, tmp_reg_val, recursion_depth + 1)
    else :
      continue
    if len(reg_val_list) > 0 :
      return reg_val_list
  return []

def out_to_reg_A(_out) :
  return out_to_reg_A_aux_v2(_out, len(_out)).pop()

helpers.LOG_DICT["D"] = [False, "[DEBUG]"]

helpers.print_log_entries("Reversal function on instructions (dec then octet representations) :", log_cats = {"R"})
# le_res_p2 = out_to_reg_A(le_out)
le_res_p2 = out_to_reg_A(le_instructions)
helpers.print_log_entries("{} i.e. {}".format(le_res_p2, octet_decompose(le_res_p2)), log_cats = {"R"})
# print(octet_decompose(le_res_p2))


helpers.print_log_entries("Re-running machine on finding {} :".format(le_res_p2), log_cats = {"R"})
# load_machine(le_file_content)
helpers.print_log_entries(get_res_for_reg_A_value(le_res_p2), log_cats = {"R"})