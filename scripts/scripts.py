from teachingutils.classUtils import *
from teachingutils.seat_randomizer import *
from teachingutils.stats import *
from teachingutils.error import *
import smtplib

"""
a few other functions that may be useful as well as a main() function to 
put things together if so desired.
"""
def assign_seats(sections=None):
  """
  reads input data and then runs seat_randomizer
  """
  cfg_dict = read_config()
  assert(len(cfg_dict.keys())>0)
  try:
    if sections is None:  
      sections = cfg_dict["mysections"] 
    tables = int(cfg_dict['tables'])
    seats  = int(cfg_dict["seats_per_table"])
  except KeyError:
    print('\nkey not in dict: check data.cfg.')
    print('the current list of keys available:\n')
    for key, value in cfg_dict.iteritems():
      print key
    raise
  except ValueError:
    print('\nvalues for seats and tables must be ints.\n\n')
    raise

  for item in sections:
    studentList = getData(cfg_dict,item)
    assert(len(studentList)>0 and tables!=0 and seats!=0)
    print(item+" "+str(len(studentList)))
    seat_randomizer(item,studentList,tables,seats,filename=str(item)+".txt")

  return

def printScores(assignments,sections=None):
  for section in list(sections):
    string = "\nsection: "+str(section)+"\n===========================================\n"
    for assignment in assignments:
      scores = getStats(assignment,section)
      string += "  %(asgn)-12s  %(mean)-6.3lf  +/-  %(std)-6.3lf\n"%{'asgn':assignment, 'mean':scores[0], 'std':scores[1]}
    scores = getOverallStats(section)
    string+="-------------------------------------------\n"
    string+="  totals:       %(mean)-6.3lf  +/-  %(std)-6.3lf\n"%{'mean':scores[0], 'std':scores[1]}
  return string

def check_email():
  message = open("email_text.txt").read()

  yn = raw_input("is this what you want to send? (y/n)")
  return message if yn=='y' else False

def send_email(to,server,port_num=None):
  """
  sends an email.  port defaults to None (smtp defaults as 25)
  """

  try:
    port = int(port_num)
  except:
    port = None
    
  message = open("email_text.txt").read()
  print "\nsubject: "+subject
  print "\nrecipients = "+str(to)
  print "\n"+message
  yn = raw_input("is this what you want to send? (y/n)")
  if yn!='y':
    return


  try:
    smtpserver = smtplib.SMTP(server,port)
  except:
    print server
    print "port = "+str(port)
    raise
  smtpserver.ehlo()
  smtpserver.starttls()
  smtpserver.ehlo
  try:
    user = raw_input('username:')
    while '@' not in user:
      user = raw_input('username needs \'@\'\nusername:')
      
    pswd = raw_input('password:')
    smtpserver.login(user, pswd)
  except smtplib.SMTPAuthenticationError:
    print("login failed.  try again.")
    raise

  failed_sent = []

  msg = ("From: %s\r\nBCC: %s\r\n%s"
       % (user, ", ".join(to),message))  
#Subject: line should be included at top of message

  try:
    smtpserver.sendmail(user, to, msg)
  except smtplib.SMTPRecipientsRefused:
    failed_sent.append(item)

  if len(failed_sent)>0:
    print 'these emails failed:'+repr(failed_sent)

  smtpserver.close()
  return

def getuname(sections=None):
  """print out email friendly comma-separated string of all email addresses"""
  studentList, cfg_dict = init_it()
  unames = []
  if sections is None:  
    try:
      sections = cfg_dict["mysections"]
    except KeyError:
      print("key: \'mysections\' does not exist")
      raise
    except:
      print("exception: key is "+cfg_dict["mysections"])
      raise
  ext = cfg_dict['emailext']
  for section in sections:
    studentList, cfg_dict = init_it(section)
    string = ''
    for item in studentList:
      string+=item["username"]+"@"+ext+","
      unames.append(item["username"]+"@"+ext)

  return unames
  
def getTotals(section):
  studentlist, cfg_dict = init_it(section)
  print len(studentlist)
  data = []
  for student in studentlist:
    data.append(getTotal(student,cfg_dict))
  return data

def runAll():
  """
  just an example of how to run a few of these functions
  """
  students, cfg_dict= init_it()
  unames = getuname(cfg_dict['mysections'])
  #assign_seats() 
  #text = printScores(['quiz09', 'prelab09', 'inlab09', 'conclusion08'],[784952, 784964])
  #text = printScores(['quiz09', 'prelab09', 'inlab09', 'conclusion08'],[784952])
  email_body = open("Data/email_text.txt").read()

  send_email(unames+['s1gustaf@physics.ucsd.edu'],cfg_dict['smtpserver'],cfg_dict["port"])
  #send_email(['s1gustaf@gmail.com','s1gustaf@physics.ucsd.edu'],cfg_dict['smtpserver'],'a test','the body')
if __name__ == '__main__':
  runAll()
      
    
