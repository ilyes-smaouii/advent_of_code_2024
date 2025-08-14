import helpers

# open file, collect content
le_char_table = helpers.get_file_content_as_table("../inputs/day_08_input.txt")
# le_char_table = helpers.raw_to_table("""..........
# ..........
# ..........
# ....a.....
# ........a.
# .....a....
# ..........
# ..........
# ..........
# ..........""")
# le_char_table = helpers.raw_to_table("""............
# ........0...
# .....0......
# .......0....
# ....0.......
# ......A.....
# ............
# ............
# ........A...
# .........A..
# ............
# ............""")

######
# PART 1
######

def get_antenna_positions(char_table) :
  row_count = len(char_table)
  col_count = len(char_table[0])
  antenna_positions = dict()
  for row_idx in range(row_count) :
    for col_idx in range(col_count) :
      curr_char = char_table[row_idx][col_idx]
      if curr_char == "." :
        continue
      if curr_char not in antenna_positions :
        antenna_positions[curr_char] = set()
      antenna_positions[curr_char].add((row_idx, col_idx))
  return antenna_positions

def get_antinodes_set(char_table) :
  row_count = len(char_table)
  col_count = len(char_table[0])
  antenna_positions = get_antenna_positions(char_table)
  antinodes_positions = set()
  for row_idx in range(row_count) :
    for col_idx in range(col_count) :
      for antenna_type, positions in antenna_positions.items() :
        for position_1 in positions :
          for position_2 in positions :
            row_diff_1 = position_1[0] - row_idx
            col_diff_1 = position_1[1] - col_idx
            row_diff_2 = position_2[0] - row_idx
            col_diff_2 = position_2[1] - col_idx
            if ((row_diff_1 == 2 * row_diff_2 and col_diff_1 == 2 * col_diff_2) \
              or (row_diff_2 == 2 * row_diff_1 and col_diff_2 == 2 * col_diff_1)) \
                and (row_diff_1 != 0 or col_diff_1 != 0) :
              antinodes_positions.add((row_idx, col_idx))
  return antinodes_positions

def count_antinodes(char_table) :
  return len(get_antinodes_set(char_table))

print("Antinodes count : ", count_antinodes(le_char_table), sep = "")
# print("Antinodes set : ", get_antinodes_set(le_char_table), sep = "")

######
# PART 2
######

def get_antinodes_set_v2(char_table) :
  row_count = len(char_table)
  col_count = len(char_table[0])
  antenna_positions = get_antenna_positions(char_table)
  antinodes_positions = set()
  for row_idx in range(row_count) :
    for col_idx in range(col_count) :
      for antenna_type, positions in antenna_positions.items() :
        for position_1 in positions :
          for position_2 in positions :
            if position_1 == position_2 :
              continue
            row_diff_1 = position_1[0] - row_idx
            col_diff_1 = position_1[1] - col_idx
            row_diff_2 = position_2[0] - row_idx
            col_diff_2 = position_2[1] - col_idx
            if row_diff_1 * col_diff_2 == row_diff_2 * col_diff_1 :
              antinodes_positions.add((row_idx, col_idx))
              # print("row_diff_1 : ", row_diff_1, sep = "") # [debugging]
              # print("col_diff_1 : ", col_diff_1, sep = "") # [debugging]
              # print("row_diff_2 : ", row_diff_2, sep = "") # [debugging]
              # print("col_diff_2 : ", col_diff_2, sep = "") # [debugging]
              # print("") # [debugging]
  return antinodes_positions

def count_antinodes_v2(char_table) :
  return len(get_antinodes_set_v2(char_table))

print("Antinodes count v2 : ", count_antinodes_v2(le_char_table), sep = "")
# print("Antinodes set v2 : ", get_antinodes_set_v2(le_char_table), sep = "")