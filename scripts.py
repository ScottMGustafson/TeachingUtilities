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
    string = "\nsection: "+str(section)+"\n===========================================\n")
    for assignment in assignments:
      scores = getStats(assignment,section)
      string += "  %(asgn)-12s  %(mean)-6.3lf  +/-  %(std)-6.3lf"%{'asgn':assignment, 'mean':scores[0], 'std':scores[1]}
    scores = getOverallStats(section)
    string+="-------------------------------------------"
    string+="  totals:       %(mean)-6.3lf  +/-  %(std)-6.3lf"%{'mean':scores[0], 'std':scores[1]}
  return string



def send_email(to,server,subject,message,port=None):
  """
  sends an email.  port defaults to None (smtp defaults as 25)
  """
  user = raw_input('username:')
  pswd = raw_input('password:')
  smtpserver = smtplib.SMTP(server,port)
  smtpserver.ehlo()
  smtpserver.starttls()
  smtpserver.ehlo
  try:
    smtpserver.login(user, pswd)
  except smtplib.SMTPAuthenticationError:
    print("login failed.  try again.")
    raise

  failed_sent = []
  for item in to: 
    header = 'To:' + item + '\n' + 'From: ' + user + '\n' + 'Subject:'+subject+' \n'
    msg = header + message

    try:
      smtpserver.sendmail(user, item, msg)
    except smtplib.SMTPRecipientsRefused:
      failed_sent.append(item)

  if len(failed_sent)>0:
    print 'these emails failed:'+repr(failed_sent)

      
  smtpserver.close()

def getuname(sections=None):
  """print out email friendly comma-separated string of all email addresses"""
  studentList, cfg_dict = init_it()
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
    print("\n\n  "+str(section))
    string = ''
    unames = []
    for item in studentList:
      string+=item.username+ext+","
      unames.append(item.username+ext)
    print(string)

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
  #students, cfg_dict= init_it()
  unames = getuname()
  assign_seats() 
  text = printScores(['quiz08', 'prelab08', 'inlab08', 'conclusion07'],[784952, 784964])
  print text
  email_subject=" "
  email_body=text
  #send_email(unames,cfg_dict['emailserver']email_subject,email_body)

if __name__ == '__main__':
  runAll()
      
    
