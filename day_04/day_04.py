# open file, collect content
le_filename = "day_04_input.txt"
le_file = open(le_filename, "r")
le_file_content = le_file.read()

######
# PART 1
######

le_lines = le_file_content.split("\n")
# don't change much, as strings can also be accessed using [], but at least this
# makes it clear that we're treating our variable as a table, rather than
# as a collection of lines :
le_char_table = [[c for c in line] for line in le_lines]

def word_count(char_table, pos_i, pos_j, word = "XMAS") :
  """
  Count how many "XMAS" we can count starting from cell at position (pos_i,pos_j)
  in char_table
  """
  row_count = len(char_table)
  # assuming we have a proper table, where each row has the same number of cells :
  col_count = len(char_table[0])
  #
  wl = len(word)
  wt = [c for c in word]
  wc = 0
  ct = char_table
  can_go_right = (0 <= pos_j <= col_count - wl)
  can_go_left = (-1 + wl <= pos_j <= col_count - 1)
  can_go_down = (0 <= pos_i <= row_count - wl)
  can_go_up = (-1 + wl <= pos_i <= row_count - 1)
  # check for regular horizontal "XMAS"
  if (can_go_right) :
    wrd = []
    for i in range(wl) :
      wrd.append(ct[pos_i][pos_j + i])
    # print("wrd : ", wrd) # [debugging]
    if (wrd == wt) :
      wc += 1
  # check for reverse horizontal "XMAS"
  if (can_go_left) :
    wrd = []
    for i in range(wl) :
      wrd.append(ct[pos_i][pos_j - i])
    # print("wrd : ", wrd) # [debugging]
    if (wrd == wt) :
      wc += 1
  # check for regular vertical "XMAS"
  if (can_go_down) :
    wrd = []
    for i in range(wl) :
      wrd.append(ct[pos_i + i][pos_j])
    # print("wrd : ", wrd) # [debugging]
    if (wrd == wt) :
      wc += 1
  # check for reverse vertical "XMAS"
  if (can_go_up) :
    wrd = []
    for i in range(wl) :
      wrd.append(ct[pos_i - i][pos_j])
    # print("wrd : ", wrd) # [debugging]
    if (wrd == wt) :
      wc += 1
  #
  # check for right-up diagonal "XMAS"
  if (can_go_up and can_go_right) :
    wrd = []
    for i in range(wl) :
      wrd.append(ct[pos_i - i][pos_j + i])
    # print("wrd : ", wrd) # [debugging]
    if (wrd == wt) :
      wc += 1
  # check for right-down diagonal "XMAS"
  if (can_go_down and can_go_right) :
    wrd = []
    for i in range(wl) :
      wrd.append(ct[pos_i + i][pos_j + i])
    # print("wrd : ", wrd) # [debugging]
    if (wrd == wt) :
      wc += 1
  # check for left-up diagonal "XMAS"
  if (can_go_up and can_go_left) :
    wrd = []
    for i in range(wl) :
      wrd.append(ct[pos_i - i][pos_j - i])
    # print("wrd : ", wrd) # [debugging]
    if (wrd == wt) :
      wc += 1
  # check for left-down diagonal "XMAS"
  if (can_go_down and can_go_left) :
    wrd = []
    for i in range(wl) :
      wrd.append(ct[pos_i + i][pos_j - i])
    # print("wrd : ", wrd) # [debugging]
    if (wrd == wt) :
      wc += 1
  return wc

test_text = [
  "XMAS",
  "MM..",
  "A.A.",
  "S..S",
]
test_table = [[c for c in list(line)] for line in test_text]

# print("test_table :\n", test_table, sep = "") # debugging

print("Test table's count :\n", word_count(test_table, 0, 0), sep = "")

total_count = 0
for i in range(len(le_char_table)) :
  for j in range(len(le_char_table[0])) :
    total_count += word_count(le_char_table, i, j)

print("Actuable table's XMAS count :\n", total_count, sep = "")

######
# PART 2
######

def has_x_mas(char_table, pos_i, pos_j) :
  """
  Check for X-MAS, where pos_i and pos_j are centered on "A"
  """
  row_count = len(char_table)
  # assuming we have a proper table, where each row has the same number of cells :
  col_count = len(char_table[0])
  if (pos_i < 1 or pos_i >= row_count - 1 or pos_j < 1 or pos_j >= col_count - 1) :
    return False
  word_a = "".join(char_table[pos_i - 1][pos_j - 1] + char_table[pos_i][pos_j] + char_table[pos_i + 1][pos_j + 1])
  word_b = "".join(char_table[pos_i - 1][pos_j + 1] + char_table[pos_i][pos_j] + char_table[pos_i + 1][pos_j - 1])
  # print("word_a and word_b :", word_a, word_b, sep = "\n") # [debugging]
  if (word_a == "MAS" or word_a == "SAM") and (word_b == "MAS" or word_b == "SAM") :
    return True
  return False

def count_x_mas(char_table) :
  """
  Count occurrences of X-MAS in table
  """
  row_count = len(char_table)
  # assuming we have a proper table, where each row has the same number of cells :
  col_count = len(char_table[0])
  x_mas_count = 0
  for i in range(row_count) :
    for j in range(col_count) :
      if has_x_mas(char_table, i, j) :
        x_mas_count += 1
  return x_mas_count

print("Actuable table's X-MAS count :\n", count_x_mas(le_char_table), sep = "")