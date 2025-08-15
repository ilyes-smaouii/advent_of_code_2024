
def get_file_content_raw(filename) :
  _file = open(filename, "r")
  _file_content = _file.read()
  return _file_content

def id_func(arg) :
  return arg

def raw_to_table(raw_content, transformation_func = None) :
  _lines = raw_content.split("\n")
  if transformation_func == None :
    transformation_func = id_func
  _char_table = []
  for _line in _lines :
    _char_table.append([transformation_func(char) for char in _line])
  return _char_table

def get_file_content_as_table(filename, transformation_func = None) :
  if transformation_func == None :
    transformation_func = id_func
  _file_content = get_file_content_raw(filename)
  return raw_to_table(_file_content, transformation_func)

def concat_table_as_str(table, func = None) :
  if func == None :
    func = str
  return "".join(func(elem) for elem in table)