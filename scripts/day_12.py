import helpers
import copy

# open file, collect content
le_filename = "../inputs/day_12_input.txt"
# le_file_content = helpers.get_file_content_raw(le_filename)
# le_lines = helpers.get_file_content_as_lines(le_filename)
le_char_table = helpers.get_file_content_as_table(le_filename)
le_test_table = helpers.raw_to_table("""AAAA
BBCD
BBCC
EEEC""")
le_test_table_2 = helpers.raw_to_table("""RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE""")
le_test_table_3 = helpers.raw_to_table("""AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA""")

######
# PART 1
######

def get_neighboring_cells(table, cell_pos, bound_checking = True) :
  row_count = len(table)
  col_count = len(table[0])
  row, col = cell_pos
  helpers.print_log_entries("get_neighboring_cells() - table :", table, log_cats = "D")
  helpers.print_log_entries("get_neighboring_cells() - row_count and col_count :", \
    str(row_count) + ", " + str(col_count), log_cats = {"D"})
  neighbors = dict()
  if row > 0 or not bound_checking :
    neighbors["up"] = (row - 1, col)
  if row < row_count - 1 or not bound_checking :
    neighbors["down"] = (row + 1, col)
  if col > 0 or not bound_checking :
    neighbors["left"] = (row, col - 1)
  if col < col_count - 1 or not bound_checking :
    neighbors["right"] = (row, col + 1)
  helpers.print_log_entries("get_neighboring_cells() - neighbors :", neighbors, log_cats = {"D"})
  return neighbors

""" def get_area_from_cell_aux(table, cell_pos, area_color = None, checked_cells = set()) :
  row_count = len(table)
  col_count = len(table[0])
  row_idx, col_idx = cell_pos
  if area_color is None :
    area_color = table[row_idx][col_idx]
  if table[row_idx][col_idx] == area_color :
    checked_cells.add(cell_pos)
    for row, col in copy.copy(checked_cells) :
      for neighbor in get_neighboring_cells(table, (row, col)).values() :
        if neighbor not in checked_cells :
          checked_cells |= get_area_from_cell_aux(table, neighbor, area_color, checked_cells)
  else :
    helpers.print_log_entries("get_area_from_cell_aux() - not area_color !", log_cats = {"AREA"})
  helpers.print_log_entries("get_area_from_cell_aux() - checked_cells : " + str(checked_cells), log_cats = {"AREA"})
  return checked_cells

def get_area_from_cell(table, cell_pos, area_color = None) :
  return get_area_from_cell_aux(table, cell_pos, area_color, set())
"""

# Got a much less efficient version above, which I've replaced with this one
def get_area_from_cell_v2(table, cell_pos, area_color = None) :
  row_count = len(table)
  col_count = len(table[0])
  row_idx, col_idx = cell_pos
  if area_color is None :
    area_color = table[row_idx][col_idx]
  final_area = set()
  next_layer = {(cell_pos)}
  while len(next_layer) > 0 :
    final_area.update(next_layer)
    temp_next_layer = set()
    for layer_cell in next_layer :
      helpers.print_log_entries("get_neighboring_cells(table, layer_cell) :", get_neighboring_cells(table, layer_cell), log_cats = {"AREA", "TMP_LAYERS"}) # [debugging]
      neighbors = set([pos for pos in get_neighboring_cells(table, layer_cell).values() if table[pos[0]][pos[1]] == area_color])
      helpers.print_log_entries("neighbors :", neighbors, log_cats = {"AREA", "TMP_LAYERS"}) # [debugging]
      temp_next_layer |= neighbors
    helpers.print_log_entries("temp_next_layer :", temp_next_layer, log_cats = {"AREA", "TMP_LAYERS"}) # [debugging]
    next_layer = temp_next_layer.difference(final_area)
  return final_area

def compute_area_perimeter(table, area_cell_positions) :
  perimeter = 0
  for cell in area_cell_positions :
    for positions in get_neighboring_cells(table, cell, False).values() :
      if positions not in area_cell_positions :
        perimeter += 1
  return perimeter

def get_regions(table) :
  row_count = len(table)
  col_count = len(table[0])
  regions = []
  cells_set = set()
  # first, make set of all cells
  for row_idx in range(row_count) :
    for col_idx in range(col_count) :
      cells_set.add((row_idx, col_idx))
  # then group them into regions
  while len(cells_set) > 0 :
    next_cell = cells_set.pop()
    next_area = get_area_from_cell_v2(table, next_cell)
    regions.append(next_area)
    cells_set = cells_set.difference(next_area)
  return regions

def compute_cost(table) :
  cost = 0
  regions = get_regions(table)
  helpers.print_log_entries("Got {} regions".format(len(regions)), log_cats = {"REG_COUNT"})
  helpers.print_log_entries(regions, log_cats = {"REG_DEETS"})
  for region in regions :
    cost += len(region) * compute_area_perimeter(table, region)
  return cost

helpers.LOG_DICT["D"] = [False, "[DEBUG]"]
helpers.LOG_DICT["T"] = [False, "[TESTING]"]
helpers.LOG_DICT["AREA"] = [False, "[AREA]"]
helpers.LOG_DICT["REG_DEETS"] = [False, "[REG_DEETS]"]
helpers.LOG_DICT["REG_COUNT"] = [True, "[REG_COUNT]"]
helpers.LOG_DICT["TMP_LAYERS"] = [False, "[TMP_LAYERS]"]

helpers.print_log_entries("compute_area_perimeter(le_test_table, (1, 3) :", \
  compute_area_perimeter(le_test_table, {(1, 3)}), log_cats = {"T"}) # [testing]
helpers.print_log_entries("get_area_from_cell(le_test_table, (1, 3)) :", get_area_from_cell_v2(le_test_table, (1, 3)), log_cats = "T")
helpers.print_log_entries("compute_area_perimeter(le_test_table, get_area_from_cell_v2(le_test_table, (1, 3)) :", \
  compute_area_perimeter(le_test_table, get_area_from_cell_v2(le_test_table, (1, 3))), log_cats = {"T"}) # [testing]
helpers.print_log_entries("", log_cats = {"T"})
helpers.print_log_entries("get_area_from_cell_v2(le_test_table, (1,0)) :", get_area_from_cell_v2(le_test_table, (1,0)), log_cats = "T")
helpers.print_log_entries("compute_area_perimeter(le_test_table, get_area_from_cell_v2(le_test_table, (1,0)) :", \
  compute_area_perimeter(le_test_table, get_area_from_cell_v2(le_test_table, (1,0))), log_cats = {"T"}) # [testing]

helpers.print_log_entries("Total cost for le_test_table :", compute_cost(le_test_table), log_cats = {"T"})

helpers.print_log_entries("Total cost le_test_table_2 :", compute_cost(le_test_table_2), log_cats = {"T"})

helpers.print_log_entries("Total cost for le_char_table :", compute_cost(le_char_table), log_cats = {"R"})

######
# PART 2
######

def count_area_sides(table, area_cell_positions) :
  """
  Works by counting corners rather than sides directly, since there are as many corners as there are
  sides
  """
  side_count = 0
  for (row, col) in area_cell_positions :
    neighbors = {dir : pos for dir, pos in get_neighboring_cells(table, (row, col)).items() if pos in area_cell_positions}
    neighbor_count = len(neighbors)
    # count "outwards" corners
    if neighbor_count < 3 :
      if neighbor_count == 1 :
        side_count += 2
      elif neighbor_count == 2 :
        if ("up" in neighbors) != ("down" in neighbors) :
          side_count += 1
      elif neighbor_count == 0 :
        side_count += 4 # should only happen for regions with exactly one cell, unless I'm mistaked
    # count "inwards" corners
    directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    for i in range(len(directions)) :
      row_1, col_1 = directions[i]
      row_2, col_2 = directions[(i + 1)%len(directions)]
      if (row + row_1, col + col_1) in area_cell_positions and \
        (row + row_2, col + col_2) in area_cell_positions and \
          (row + row_1 + row_2, col + col_1 + col_2) not in area_cell_positions :
            side_count += 1
  return side_count

def compute_cost_with_promo(table) :
  cost = 0
  regions = get_regions(table)
  helpers.print_log_entries("Got {} regions".format(len(regions)), log_cats = {"REG_COUNT"})
  helpers.print_log_entries(regions, log_cats = {"REG_DEETS"})
  for region in regions :
    cost += len(region) * count_area_sides(table, region)
  return cost

helpers.print_log_entries("Total cost with promotions for le_test_table :", compute_cost_with_promo(le_test_table), log_cats = {"T"})

helpers.print_log_entries("Total cost with promotions le_test_table_3 :", compute_cost_with_promo(le_test_table_3), log_cats = {"T"})

helpers.print_log_entries("Total cost with promotions for le_char_table :", compute_cost_with_promo(le_char_table), log_cats = {"R"})
