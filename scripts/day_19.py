import helpers

# open file, collect content
le_filename = "../inputs/day_19_input.txt"
le_file_content = helpers.get_file_content_raw(le_filename)
# le_lines = helpers.get_file_content_as_lines(le_filename)
# le_char_table = helpers.get_file_content_as_table(le_filename)
le_test_input = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""

######
# PART 1
######

def parse_input(input) :
  patterns_data, designs_data = input.split("\n\n")
  patterns_str = patterns_data.split(", ")
  designs_str = designs_data.split("\n")
  return patterns_str, designs_str

def check_design_rec(design, patterns) :
  if len(design) == 0 :
    return True
  for pattern in patterns :
    pattern_len = len(pattern)
    if design[:pattern_len] == pattern :
      res = check_design_rec(design[pattern_len:], patterns)
      if res :
        return True
  return False

def count_possible_designs(designs, patterns) :
  possible_designs_count = 0
  for design in designs :
    if check_design_rec(design, patterns) :
      possible_designs_count += 1
  return possible_designs_count

helpers.LOG_DICT["T"][0] = False

helpers.print_log_entries("parse_input(le_file_content)[0] :", parse_input(le_file_content)[0], log_cats = {"T"})
helpers.print_log_entries("parse_input(le_file_content)[1] :", parse_input(le_file_content)[1], log_cats = {"T"})

le_patterns, le_designs = parse_input(le_file_content)
le_possible_design_count = count_possible_designs(le_designs, le_patterns)

helpers.print_log_entries("Possible designs count :", le_possible_design_count, log_cats = {"R"})

######
# PART 2
######

def count_possible_ways_for_design_rec(design, patterns) :
  total_count = 0
  if len(design) == 0 :
    return 1
  for pattern in patterns :
    pattern_len = len(pattern)
    if design[:pattern_len] == pattern :
      total_count += count_possible_ways_for_design_rec(design[pattern_len:], patterns)
  return total_count

def count_possible_ways_efficient(design, patterns) :
  total_count = 0
  if len(design) == 0 :
    return 1
  for pattern in patterns :
    pattern_len = len(pattern)
    if design[:pattern_len] == pattern :
      total_count += count_possible_ways_for_design_rec(design[pattern_len:], patterns)
  return total_count

def count_total_possible_ways(designs, patterns) :
  total_possible_ways = 0
  for design in designs :
    total_possible_ways += count_possible_ways_for_design_rec(design, patterns)
  return total_possible_ways

helpers.LOG_DICT["T"][0] = True

le_test_patterns, le_test_designs = parse_input(le_test_input)

le_test_total_possible_ways = count_total_possible_ways(le_test_designs, le_test_patterns)

helpers.print_log_entries("Total possible ways count :", le_test_total_possible_ways, log_cats = {"T"})

le_total_possible_ways = count_total_possible_ways(le_designs, le_patterns[:250])

helpers.print_log_entries("Total possible ways count :", le_total_possible_ways, log_cats = {"R"})