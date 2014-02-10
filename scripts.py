from teachingutils.classUtils import *
from teachingutils.seat_randomizer import *
from teachingutils.stats import *
from teachingutils.error import *
import smtplib
import time

"""
a few other functions that may be useful as well as a main() function to 
put things together if so desired.
"""
#define these for the rest of the functions here
students, cfg_dict= init_it() 
 
date = time.strftime("%Y-%m-%d")
lab=3  #this week's lab
if lab<10:
  thisweek=['conclusion0'+str(lab-1),'quiz0'+str(lab), \
    'prelab0'+str(lab), 'inlab0'+str(lab)]
else:
  thisweek=['conclusion'+str(lab-1),'quiz'+str(lab), \
    'prelab'+str(lab), 'inlab'+str(lab)]



def run():
  """
  everything is run through here...
  """
  assign_seats() 
  print cfg_dict['mysections']
  print printScores(thisweek,cfg_dict['mysections'])

  #for an automated weekly email, to be performed upon running this code:
  for item in cfg_dict['mysections']:
    automate_grade_email(lab,item)
    
  
  # for a general mass email to all sections, fill in Data/email_text.txt as desired
  unames = getuname()
  send_email(unames+[cfg_dict['myuname']+'@ucsd.edu'],cfg_dict['smtpserver'],port_num=cfg_dict["port"])


def automate_grade_email(lab_no,section):
  unames = getuname(section)

  text='Subject: Phys 1CL: lab '+str(lab_no)+' grades\n\n'
  text+=printScores(thisweek,section)
  filename=str(section)+'_grades.txt'
  f=open(filename,'w').write(text)
  send_email(unames+[cfg_dict['myuname']+'@ucsd.edu'], cfg_dict['smtpserver'], \
      filename, cfg_dict["port"])
  return
    

def assign_seats(sections=None):
  """
  reads input data and then runs seat_randomizer

  input params:
  -------------
  sections : the list of sections to assign.  if None, will do all in cfg_dict['mysections']

  output:
  -------
  will create one formatted .txt file for each section.
  """
  #cfg_dict = read_config()
  assert(len(cfg_dict.keys())>0)
  try:
    if sections is None:  
      sections = cfg_dict["mysections"] 
    tables = int(cfg_dict['tables'])
    seats  = int(cfg_dict["seats_per_table"])
  except KeyError:
    msg = '\nkey not in dict: check data.cfg the current list of keys available:\n'
    msg+=str(cfg_dict.keys())
    raise Exception(msg)
  except ValueError:
    raise Exception('\nvalues for seats and tables must be ints.\n\n')

  for item in sections:
    students = getData(cfg_dict,item)
    assert(len(students)>0 and tables!=0 and seats!=0)
    print(item+" "+str(len(students)))
    seat_randomizer(item,students,tables,seats,filename=str(item)+".txt",msg=" lab "+str(lab))

  return

def printScores(assignments,sections=None):
  """
  input params:
  -------------
  assignments : a list of assignment names to use.  Should follow whats in Data/data.cfg
  sections : the list of sections to use.  if None, will do all in cfg_dict['mysections']

  output:
  -------
  a string of data to be printed
  """
  string = ''
  if sections is None:
    sections = cfg_dict['mysections']
  elif type(sections) is not list:
    if type(sections) is int:
      sections = [ str(sections) ]
    else:
      try:
        sections = int(sections)   #test if can cast as int.  If yes, make as list of str
        sections = [ str(sections) ]
      except:
        raise Exception('Type of sections should be int, instead got '+str(type(sections)))

  for section in sections:
    string += "\n\nsection: "+str(section)+" lab "+str(lab)+"\n===========================================\n"
    for assignment in assignments:
      scores = getStats(assignment,section)
      string += "  %(asgn)-12s  %(mean)-6.3lf  +/-  %(std)-6.3lf\n"%{'asgn':assignment, 'mean':scores[0], 'std':scores[1]}
    scores = getOverallStats(section)
    string+="-------------------------------------------\n"
    string+="  totals:       %(mean)-6.3lf  +/-  %(std)-6.3lf\n"%{'mean':scores[0], 'std':scores[1]}
  return string

def send_email(to,server,email_file=cfg_dict["emailtext"],port_num=None):
  """
  sends an email.  port defaults to None (smtp defaults as 25)
  input:
  ------
  to : list of email address to send to
  server : server name.  usually cfg_dict["smtpserver"]
  port : port name.  defaults to 25 if None
  """

  try:
    port = int(port_num)
  except:
    port = None
    
  message = open(email_file).read()
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
  else:
    if not type(sections)==list:
      try:
        sections = [sections]
      except:
        raise Exception("can\'t convert %s to list "%str(sections))
  ext = cfg_dict['emailext']
  for section in sections:
    studentList = init_it(section)[0]
    string = ''
    for item in studentList:
      string+=item["username"]+"@"+ext+","
      unames.append(item["username"]+"@"+ext)
  return unames
  
def getTotals(section):
  """
  gets class totals
  """
  studentlist = init_it(section)[0]
  print len(studentlist)
  data = []
  for student in studentlist:
    data.append(getTotal(student,cfg_dict))
  return data



if __name__=='__main__':
  run()
    
