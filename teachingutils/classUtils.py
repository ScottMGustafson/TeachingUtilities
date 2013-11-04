import csv
from sys import exit
import re
import os.path
from collections import namedtuple
from pkg_resources import resource_stream
import stringtools

def printFields(obj):
  """
  print all the fields.  This is useful when the object fields seem screwy
  """
  for name in obj._fields:
    print name

  return

data_path, _ = os.path.split(__file__)
data_path = os.path.join(data_path[0:-1],'Data','data.cfg')

def read_config(filestream=open(data_path)):
  """
  read the configuration file, by default data.cfg.
  returns a dict containing relevant config info.
  """
  cfg_dict = {}
  f = filestream
  for line in stringtools.non_blank(f):
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
      key  = stringtools.sanitize(temp[0])
      value= stringtools.sanitize(temp[1])
    cfg_dict[key] = value
        
  return cfg_dict

def getData(cfg_dict=read_config(), mySection=None,verbose=False):  #this code only works if csv.reader returns a list
  """
  input a csv file
  output a list of student instances
  """
  try:
    assert(os.path.isfile(cfg_dict['csvfile'])) 
  except IOError:
    print(str(cfg_dict['csvfile'])+' doesn\'t exist.')
    exit()
  except KeyError:
    if cfg_dict is not None:
      print(str(cfg_dict))
    else:
      print('cfg_dict is None')
    raise
  
  stringtools.stripExtraCommas(cfg_dict['csvfile'])
  f = open(cfg_dict['csvfile'], 'r')
  gradeFile = list(csv.reader(f, delimiter=',', quotechar='\"'))
  assert(type(gradeFile)==list)
  head = stringtools.sanitizeKeys(cfg_dict,gradeFile[0])
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

