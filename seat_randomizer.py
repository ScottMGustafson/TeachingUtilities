import classutils
from random import shuffle

class _Seat(object):
    def __init__(self,table,seat,student):
        self.table = table
        self.seat = seat
        self.student=student
    def __str__(self):
        return str(self.student)

def seat_randomizer(section,tables,seats, filename=None, msg=None):
    """
    randomize students.
    input:
        section number
        list of student instances

    output:
        None, but produces formatted txt file to be used as seating chart
    """
    if filename is None:
        filename=str(section)+'.txt'

    seat_list = []
    student_list = classutils.get_section(section)

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
    f.write("::::::::::::::::::\n    "+msg+"\n::::::::::::::::::\n")
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


