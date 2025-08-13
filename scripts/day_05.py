# open file, collect content
le_filename = "day_05_input.txt"
le_file = open(le_filename, "r")
le_file_content = le_file.read()

######
# PART 1
######

def get_rules_and_updates(lines) :
  rules = []
  updates = []
  for line in lines :
    if "," in line :
      # case 1 : update
      new_update = [int(elem) for elem in line.split(",")]
      updates.append(new_update)
    elif "|" in line :
      # case 2 : rule
      new_rule = [int(elem) for elem in line.split("|")]
      if new_rule[0] == new_rule[1] :
        # ?
        continue
      rules.append(new_rule)
    else :
      # case 3 : ?
      pass
  return (rules, updates)

le_rules, le_updates = get_rules_and_updates(le_file_content.split("\n"))
# print("le_rules :\n", le_rules, sep = "") # [debugging]
# print("le_updates :\n",le_updates, sep = "") # [debugging]
def process_updates(updates, rules) :
  total_sum = 0
  rev_rules_dict = {}
  for rule in rules :
    if rule[1] in rev_rules_dict :
      rev_rules_dict[rule[1]].add(rule[0])
    else :
      rev_rules_dict[rule[1]] = set([rule[0]])
  for curr_update in updates :
    # check if valid
    # if valid, add middle element to sum
    cant_appear = set()
    bad_update = False
    for elem in curr_update :
      if elem in rev_rules_dict :
        cant_appear.update(rev_rules_dict[elem])
      if elem in cant_appear :
        bad_update = True
        break
    if not bad_update :
      if (len(curr_update) % 2 == 1) :
        total_sum += curr_update[(len(curr_update) - 1)//2]
      else :
        pass
  return total_sum

print("Total sum is equal to :\n", process_updates(le_updates, le_rules), sep = "")

######
# PART 2
######

# Will try to use Kahn's algorithm for topological sorting here

# 1 - Helping functions for graph exploration and sorting/ordering

def get_outgoing_edges(vertex, set_of_edges) :
  out_edges = set()
  for edge in set_of_edges :
    if edge[0] == vertex :
      out_edges.add(edge)
  return out_edges

def get_incoming_edges(vertex, set_of_edges) :
  in_edges = set()
  for edge in set_of_edges :
    if edge[1] == vertex :
      in_edges.add(edge)
  return in_edges

def get_ordering(set_of_vertices, set_of_edges) :
  final_sorting = []
  starting_nodes = set()
  # starting_nodes = set of vertices with no incoming edges
  for v in set_of_vertices :
    if len(get_incoming_edges(v, set_of_edges)) == 0 :
      starting_nodes.add(v)
    else :
      pass
  # main loop
  while (len(starting_nodes) > 0) :
    curr_node = starting_nodes.pop()
    final_sorting.append(curr_node)
    for out_edge in get_outgoing_edges(curr_node, set_of_edges) :
      out_vertex = out_edge[1]
      set_of_edges.remove(out_edge)
      if len(get_incoming_edges(out_vertex, set_of_edges)) == 0 :
        starting_nodes.add(out_vertex)
  # end result
  if (len(set_of_edges) > 0) :
    raise Exception("get_ordering() Error : graph has at least one cycle !""\n""Remaining edges :\n" + str(set_of_edges) +
                    "\nfinal_sorting :\n" + str(final_sorting) +
                    "\nstarting_nodes :\n" + str(starting_nodes))
  else :
    return final_sorting

# 2 - Function built on previous ones

def sort_update_using_ordering(update, ordering) :
  from_ordering = []
  for e in ordering :
    for i in range(update.count(e)) :
      from_ordering.append(e)
  new_update = []
  j = 0
  for i in range(len(update)) :
    if update[i] in ordering :
      new_update.append(ordering[j])
      j += 1
    else :
      new_update.append(update[i])
  return new_update

def process_incorrect_updates(updates, rules) :
  all_pages_set = set()
  for ud in updates :
    all_pages_set.update(ud)
  for ru in rules :
    all_pages_set.update(ru)
  #
  sum_of_incorrect = 0
  #
  for update in updates :
    # make set of rules with only rules pertaining to current update
    update_rules_set = set()
    update_rules_pages_set = set()
    # include only rules relevant to current update in update_rules_pages_set
    for rule in rules :
      if (rule[0] in update and rule[1] in update) :
        update_rules_set.add((rule[0], rule[1]))
        update_rules_pages_set.update(rule)
    # retrieve ordering obtained using only rules in update_rules_set
    update_ordering = get_ordering(update_rules_pages_set, update_rules_set)
    cant_appear = []
    bad_update = False
    for elem in update :
      for rule in rules :
        if rule[1] == elem :
          cant_appear.append(rule[0])
      if elem in cant_appear :
        bad_update = True
        break
    # print("process_incorrect_updates() - update : ", update, sep = "", end = "\n\n") # [debugging]
    #
    # check if valid
    # if not valid, reorder then add middle element to sum
    if bad_update :
      corrected_update = sort_update_using_ordering(update, update_ordering)
      # print("process_incorrect_updates() - corrected_update : ", corrected_update, sep = "", end = "\n\n") # [debugging]
      if (len(corrected_update) % 2 == 1) :
        sum_of_incorrect += corrected_update[(len(update) - 1)//2]
      else :
        pass
  return sum_of_incorrect

# 3 - Now we can see the result

le_sum_of_incorrect = process_incorrect_updates(le_updates, le_rules)

print("le_sum_of_incorrect : ", le_sum_of_incorrect, sep = "")