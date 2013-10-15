import os
import sys
from classUtils import *
from random import shuffle

class _Seat(object):
  def __init__(self,table,seat,student=None):
    self.table = table
    self.seat = seat
    self.student=student
  def studentString(self):
    return self.student.firstname+' '+self.student.lastname

def seat_randomizer(section,student_list,tables,seats,filename="seating.txt"):
  """
  randomize students.
  input:
    section number
    list of student instances

  output:
    None, but produces formatted txt file to be used as seating chart
  """
  seatList = []

  shuffle(student_list)
  for i in range(0,seats):
    for j in range(0,tables):
      try:
        seatList.append(_Seat(j,i,student_list[0]))
        del(student_list[0])
      except:
        continue

  f = open(filename,"w")
  
  for i in range(0,tables):
    f.write(("\nTable %-2d\n===============================\n")%(i+1))
    for j in range(0,seats):
      for item in seatList:
        if item.table == i and item.seat == j:
          f.write(item.studentString()+"\n")
        else:
          pass    
  f.close() 

  return


