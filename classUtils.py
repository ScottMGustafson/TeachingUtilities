import csv
from sys import exit
import re
from os.path import isfile
from collections import namedtuple

"""
this module includes various functions for taking data from csv into a usable 
form for the rest of this code.  the core thing here is getData() which parses 
data into a list of students.

"""

def extraComma(string):
  for item in string.split('\",\"'):
    if ',' in item:  
      return True
  return False

def stripExtraCommas(filename):
  """
  since we are using csv data with the delimiter:  
    "value","newvalue"

  we need to strip off excess commas in the case where the data is like:
    "value","value,with a comma"

  input:
  ---------------------------
  a filename of csv data delimited with ","

  output:
  ---------------------------
  None
  """
  f = open(filename,'r')
  data = f.readlines()
  newdata = []
  for string in data:
    strlist = string.split('\",\"')
    for i in range(0,len(strlist)):
      strlist[i] = strlist[i].replace(',','')
    newdata.append('\",\"'.join(strlist))
  f.close()

  f = open(filename,'w')
  f.writelines(newdata)
  f.close()
  return

def non_blank(filestream):
  """return lines which are neither empty, nor contain any # symbols"""
  for line in filestream:
    lines = line.rstrip()
    if lines and lines[0]!='#':
      yield lines 

def sanitize(string,ishead=False):    #issue maybe with stray quotes....maybenot.
  """
  erase all text that is not alphanumeric text or underscores.
  
  head is True if the input string will be used as a head item
  if true, then only '_' and alphanumeric characters are allowed.
  otherwise, a wider range of chars are permitted.

  also, due to restrictions of named_tuple, head cannot start with number:
  to fix this, append 'N' to front.  (name doesn't matter since this item)
  will never get used anyway.
  """
  string = string.replace('\"','')
  string = re.sub(r'\s+','_',((string.lower()).strip()))
  if ishead:
    string = re.sub(r'[^0-9a-zA-Z_\$\"]+','_',string)
    if string[0].isdigit() or string[0]=='_':
      string = 'N'+string
  else:
    string = re.sub(r'[^0-9a-zA-Z_\.\$\"]+','_',string)


  return re.sub(r'_+','_',string)   #  replace recurring instances of _ 

def sanitizeList(lst,ishead=False):
  return [ sanitize(item,ishead) for item in lst  ]

def indices(lst,value):
  for i, x in enumerate(lst):
    y = x[:len(value)] if len(value)<len(x) else x
    if sanitize(rm_nums(y))==sanitize(rm_nums(value)):
      yield i
    
def sanitizeKeys(cfg_dict,lstt):
  """
  sanitize all strings to pure alphanumeric or underscores.
  lst is incoming header data
  """

  lst = [sanitize(item,True) for item in lstt]
  if lst[0][0]=='\"':
    lst[0].replace('\"','')

  if lst[-1][-1]=='\"':
    lst[0].replace('\"','')



  for key, value in cfg_dict.iteritems():  
#problem lies in here!!!  assignments still not mapping correctly
    if not '$' in key:  
      if value in lst:
        lst[lst.index(value)] = key
      else:
        continue

    else:
      for j in indices(lst,value):
        y = lst[j][:len(value)] if len(value)<len(lst[j]) else lst[j]
        assert(len(y)==len(value))
        num = get_nums(value,y)
        if num is None: 
          continue
        newKey = key.replace('$',str(num))
        lst[j] = newKey
  return lst

def rm_nums(string,specialChar='$'):
  """
  rm digits and any other special chars
  """
  return re.sub(r'[0-9]+|\$+','',string)

def rm_nums_replace(string):
  """
  replace nums with $
  """
  return re.sub(r'[0-9]+','$',string)

def get_nums(var,raw,specialChar='$'):
  """
  find num in raw to replace specialChar in var.
  """
  #in case the order gets messed up:
  var = sanitize(var)
  raw = sanitize(raw)

  result1 = re.findall(r'[0-9]+|\$+',var)
  result2 = re.findall(r'[0-9]+|\$+',raw)

  try:
    assert(len(result1)==len(result2))
  except AssertionError:
    print("get_nums length error:\n")
    print(var+" : "+str(result1))
    print(raw+" : "+str(result2))
    raise
  try:
    ind  = result1.index('$')
    return result2[ind]
  except ValueError:
    return None

def printFields(obj):
  """
  print all the fields.  This is useful when the object fields seem screwy
  """
  for name in obj._fields:
    print name

  return

def read_config(filename='data.cfg'):
  """
  read the configuration file, by default data.cfg.
  returns a dict containing relevant config info.
  """
  cfg_dict = {}
  with open(filename,'r') as f:
    for line in non_blank(f):
      temp = line.split('::')
      if not '::' in line or len(temp)>2: 
        print(line+'\nbad formatting: data.cfg')
        exit()
      elif len(re.findall(r'\$',line.split()[1]))>1:
        print(line+": should only have 1 \'$\' character.  please reformat.")
        exit()
      
      if 'mysections' in temp[0]:
        key = 'mysections'  
        value=[item.strip() for item in temp[1].split(',')]
      else:
        key  = sanitize(temp[0])
        value= sanitize(temp[1])
      cfg_dict[key] = value
        
  return cfg_dict

def numConvert(string):
  """
  for a string that should be an int, remove any weird chars and strip off 
  everything right of the decimal
  """
  string = re.sub(r'[^0-9\.]','',string)
  string = string.split('.')[0]
  try:
    temp = int(string)
  except:
    print(string)
    sys.exit()
  return string


def getData(cfg_dict=read_config(), mySection=None,verbose=False):  #this code only works if csv.reader returns a list
  """
  input a csv file
  output a list of student instances
  """
  try:
    assert(isfile(cfg_dict['csvfile'])) 
  except IOError:
    print(str(cfg_dict['csvfile'])+' doesn\'t exist.')
    exit()
  except KeyError:
    if cfg_dict is not None:
      print(str(cfg_dict))
    else:
      print('cfg_dict is None')
    raise
  
  stripExtraCommas(cfg_dict['csvfile'])
  f = open(cfg_dict['csvfile'], 'r')
  gradeFile = list(csv.reader(f, delimiter=',', quotechar='\"'))
  assert(type(gradeFile)==list)
  head = sanitizeKeys(cfg_dict,gradeFile[0])
  try:
    student = namedtuple('Student',head)  #student class factory
  except ValueError:
    print("error with header data:\n\n")
    for item in head:
      print(item)
    print("\n\n")
    raise
    
  del(gradeFile[0])   

  if mySection is None:  
    return  [ student._make([sanitize(item) for item in row]) for row in gradeFile ]
  else:
    studentList = []
    for row in gradeFile:
      if mySection in row:
        pupil=student._make([sanitize(item) for item in row])   #a list counts as only one input...need to split it up
        pupil = pupil._replace(section=numConvert(pupil.section))
        if verbose:
          print(pupil.section+mySection)
        if pupil.section == mySection:
          studentList.append(pupil)
    #printFields(studentList[0])
    return(studentList)

