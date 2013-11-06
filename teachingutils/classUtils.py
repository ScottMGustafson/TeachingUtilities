import csv
from sys import exit
import re
import os
from collections import namedtuple
from pkg_resources import resource_stream
import stringtools

class FileDNE(Exception):
  def __init__(self,name):
    self.name = name
  def __str__(self):
    return self.name+' does not exist'

class EmptyDict(Exception):
  def __str__(self):
    return(' dict is empty')

class TooManyArgs(Exception):
  def __init__(self,expected=None,received=None,*args):
    self.received = received
    self.expected = expected
    self.args = [item for item in args]
  def __str__(self):
    if self.expected and self.received:
      return("\nexpected: "+repr(self.expected)+"\nreceived: "+repr(self.received)+"\n")  
    elif self.received and self.expected is None:
      return("\nreceived: "+repr(self.received)+"\n")
    elif self.expected and self.received is None:
      return("\nreceived: "+repr(self.expected)+"\n")
    else:
      return(repr(self.args))

class BadFormatting(Exception):
  def __init__(self,string):
    self.string = string
  def __str__(self):
    return "Bad formatting in "+repr(string)
    
      

def lenchecker(func):
  def inner(*args,**kwargs):
    try:
      lst = func(*args,**kwargs)
      if len(lst)==0:
        raise EmptyDict
    except EmptyDict:
      raise
    return lst
  return inner


def printFields(obj):
  """
  print all the fields.  This is useful when the object fields seem screwy
  """
  for name in obj._fields:
    print name
  return

def defaultfilepath():
  data_path, _ = os.path.split(os.path.abspath(__file__))
  data_path_lst = data_path.split(os.sep)
  data_path = (os.sep).join(data_path_lst[0:-1])
  data_path = os.path.join(data_path,'Data','data.cfg')
  try:
    if not os.path.isfile(data_path):
      raise FileDNE
  except FileDNE:
    raise
  return data_path

@lenchecker
def read_config(filestream = resource_stream(__name__,'../Data/data.cfg')):
  """
  read the configuration file, by default data.cfg.
  returns a dict containing relevant config info.
  """
  cfg_dict = {}
  f = filestream
  for line in stringtools.non_blank(f):
    temp = line.split('::')
    if not '::' in line or len(temp)>2: 
      raise BadFormatting(line)
    elif len(re.findall(r'\$',line.split()[1]))>1:
      raise BadFormatting(line+": should only have 1 \'$\' character.")
      
    if 'mysections' in temp[0]:
      key = 'mysections'  
      value=[item.strip() for item in temp[1].split(',')]
    elif 'csvfile' in temp[0]:
      key = temp[0].strip()
      temp[1] = temp[1].strip()
      value = os.path.abspath(temp[1])
      assert(os.path.isfile(value))
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

  assert(os.path.isfile(cfg_dict['csvfile'])) 
  
  stringtools.stripExtraCommas(cfg_dict['csvfile'])
  f = open(cfg_dict['csvfile'], 'r')
  gradeFile = list(csv.reader(f, delimiter=',', quotechar='\"'))
  assert(type(gradeFile)==list)

  head = stringtools.sanitizeKeys(cfg_dict,gradeFile[0])
  assert(len(head)==6)
  student = namedtuple('Student',head)  #student class factory  

  if mySection is None:  
    return  [ student._make([stringtools.sanitize(item) for item in row]) for row in gradeFile[1:] ]

  else:
    studentList = []
    for row in gradeFile[1:]:
      if mySection in row:
        pupil=student._make([stringtools.sanitize(item) for item in row])   #a list counts as only one input...need to split it up
        pupil = pupil._replace(section=stringtools.numConvert(pupil.section))
        if pupil.section == mySection:
          studentList.append(pupil)
    return(studentList)

