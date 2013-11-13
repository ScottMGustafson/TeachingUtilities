class AllErrors(Exception):
  def __init__(self,msg=''):
    self.msg = msg

class FileDNE(AllErrors):
  def __str__(self):
    return self.msg+' does not exist'

class EmptyDict(AllErrors):
  def __str__(self):
    return(' dict is empty:'+self.msg)

class EmptyString(AllErrors):
  def __str__(self):
    return(' string is empty:'+self.msg)

class EmptyList(AllErrors):
  def __str__(self):
    return(' List is empty:'+self.msg)

class EmptyCsvData(AllErrors):
  def __str__(self):
    return(self.msg)

class TooManyArgs(AllErrors):
  def __init__(self,expected=None,received=None):
    self.received = received
    self.expected = expected
    self.args = [item for item in args]
  def __str__(self):
    if self.expected and self.received:
      return(self.msg+"\nexpected: "+repr(self.expected)+"\nreceived: "+repr(self.received)+"\n")  
    elif self.received and self.expected is None:
      return(self.msg+"\nreceived: "+repr(self.received)+"\n")
    elif self.expected and self.received is None:
      return(self.msg+"\nreceived: "+repr(self.expected)+"\n")
    else:
      return('wrong number of args:'+self.msg)

class BadFormatting(AllErrors):
  def __str__(self):
    return "Bad formatting in "+repr(self.msg)
    
def lenchecker(func):
  """checks that a list, string or dict is not zero in length"""
  def inner(*args,**kwargs):
    lst = func(*args,**kwargs)
    if type(lst) is dict:
      if len(lst.keys())==0: raise EmptyDict
    elif type(lst) is list:
      if len(lst)==0: raise EmptyList
    elif type(lst) is str:
      if lst=='': raise EmptyString
    else:
      pass
    return lst 
  return inner

def printFields(obj):
  """
  print all the fields.  This is useful when the object fields seem screwy
  """
  for name in obj._fields:
    print name
  return
