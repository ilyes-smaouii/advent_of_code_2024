# open file, collect content
le_filename = "../inputs/day_07_input.txt"
le_file = open(le_filename, "r")
le_file_content = le_file.read()

######
# PART 1
######

le_equations = []
for line in le_file_content.split("\n") :
  fst_split = line.split(":")
  res = int(fst_split[0])
  operands = [int(elem) for elem in fst_split[1].split(" ")]
  le_equations.append((res, operands))
  pass

######
# PART 2
######