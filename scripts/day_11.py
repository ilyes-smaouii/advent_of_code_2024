import helpers
import math as m

# open file, collect content
le_filename = "../inputs/day_11_input.txt"
le_file_content = helpers.get_file_content_raw(le_filename)
# le_file_content = "125 17"
le_stones = [int(stone_str) for stone_str in le_file_content.split(" ")]

######
# PART 1
######

helpers.LOG_DICT["D"] = (False, "[DEBUG]")
helpers.LOG_DICT["R"] = (True, "[RESULTS]")

def count_digits(number) :
  return m.floor(m.log(number, 10)) + 1

def after_next_blink (stones) :
  after_blink = []
  for stone in stones :
    if stone == 0 :
      after_blink.append(1)
    else :
      digit_count = count_digits(stone)
      _pow = pow(10, digit_count//2)
      if digit_count % 2 == 0 :
        # half_1, half_2 = str(stone)[:digit_count], str(stone)[len(str(stone))//2:]
        after_blink.append(stone // _pow)
        after_blink.append(stone % _pow)
      else :
        after_blink.append(stone*2024)
  return after_blink

blink_count = 25
for i in range(blink_count) :
  le_stones = after_next_blink(le_stones)
  helpers.print_log_entries("stones afer " + str(i + 1) + " blinks : " + str(le_stones), log_cats = {"D"})
  helpers.print_log_entries("number of stones afer " + str(i + 1) + " blinks : " + str(len(le_stones)), log_cats = {"D"})
helpers.print_log_entries("number of stones afer " + str(blink_count) +\
  " blinks : " + str(len(le_stones)), log_cats = {"R"})

######
# PART 2
######

def after_next_blink_v2 (stones, iter_count) :
  after_blink = {1 : 0}
  for stone in stones :
    if stone not in after_blink :
      after_blink[stone] = 0
    after_blink[stone] += 1
  for i in range(iter_count) :
    if i % 5 == 0 :
      helpers.print_log_entries("after_next_blink_v2() - i = {}".format(i), log_cats = "I")
    next_after_blink = {1 : 0}
    for stone, count in after_blink.items() :
      if stone == 0 :
        next_after_blink[1] += count
      else :
        digit_count = count_digits(stone)
        _pow = pow(10, digit_count//2)
        if digit_count % 2 == 0 :
          # half_1, half_2 = str(stone)[:digit_count], str(stone)[len(str(stone))//2:]
          half_1 = stone // _pow
          half_2 = stone % _pow
          if half_1 not in next_after_blink :
            next_after_blink[half_1] = 0
          if half_2 not in next_after_blink :
            next_after_blink[half_2] = 0
          next_after_blink[half_1] += count
          next_after_blink[half_2] += count
        else :
          new_num = 2024 * stone
          if new_num not in next_after_blink :
            next_after_blink[new_num] = 0
          next_after_blink[new_num] += count
    after_blink = next_after_blink
  return after_blink

# for i in range(50) :
#   if i % 5 == 0 :
#     print("i = ", i, sep = "")
blink_count_2 = 75
le_stones = after_next_blink_v2(le_stones, blink_count_2 - blink_count)
stones_count = 0
for stone, count in le_stones.items() :
  stones_count += count
helpers.print_log_entries("number of stones afer 50 more blinks (i.e. 75 blinks) : " + str(stones_count), log_cats = "R")
helpers.print_log_entries("number of distinct types of stones afer 50 more blinks (i.e. 75 blinks) : " + str(len(le_stones)), log_cats = "I")