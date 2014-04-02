import os
import sys
from .classutils import *
from .error import *
from random import shuffle

class _Seat(object):
  def __init__(self,table,seat,student=None):
    self.table = table
    self.seat = seat
    self.student=student
  def __str__(self):
    return self.student['firstname']+' '+self.student['lastname']

def seat_randomizer(section,student_list,tables,seats,filename="seating.txt",msg=None):
  """
  randomize students.
  input:
    section number
    list of student instances

  output:
    None, but produces formatted txt file to be used as seating chart
  """
  seat_list = []

  shuffle(student_list)
  for i in range(0,seats):
    for j in range(0,tables):
      try:
        seat_list.append(_Seat(j,i,student_list[0]))
        del(student_list[0])
      except:
        continue

  if msg is None: msg=''
  f = open(filename,"w")
  f.write(":::::::::::::::\n  "+str(section)+msg+"\n:::::::::::::::\n")
  for i in range(0,tables):
    f.write(("\nTable %-2d\n===============================\n")%(i+1))
    for j in range(0,seats):
      for item in seat_list:
        if item.table == i and item.seat == j:
          f.write(str(item)+"\n")
        else:
          pass    
  f.close() 

  return


