import classutils 
from classutils import all_students
import seat_randomizer
import smtplib
import time
from getpass import getpass

"""
a few other functions that may be useful as well as a main() function to 
put things together if so desired.
"""

date = time.strftime("%Y-%m-%d")
mysections = [item.strip() for item in list(classutils.cfg_dict['Config']['mysections'].split(','))]

def get_thisweek():
    """get the latest few assignments, as relevant only to UCSD phys 1-series labs."""
    lab=int(input("which is this week's upcoming lab? (integer number): "))    #this week's upcoming lab
    if lab<2:
        raise Exception("no grades to post")
    elif lab==2:
        thisweek=['quiz01', 'prelab01', 'inlab01']
    elif 2<lab<=10:
        thisweek=['conclusion0'+str(lab-2),'quiz0'+str(lab-1), \
                'prelab0'+str(lab-1), 'inlab0'+str(lab-1)]
    elif lab==11:
        thisweek=['conclusion09','quiz10','prelab10', 'inlab10']
    else:
        thisweek=['conclusion'+str(lab-2),'quiz'+str(lab-1), \
                'prelab'+str(lab-1), 'inlab'+str(lab-1)]
    return thisweek, lab

thisweek, lab = get_thisweek()

#thisweek, lab = 1,0

def assign_seats(sections=mysections):
    """
    reads input data and then runs seat_randomizer

    input params:
    -------------
    sections : the list of sections to assign.    if None, will do all in mysections

    output:
    -------
    will create one formatted .txt file for each section.
    """
    try:
        tables = int(classutils.cfg_dict["Config"]['tables'])
        seats  = int(classutils.cfg_dict["Config"]["seats_per_table"])
        assert(tables!=0 and seats!=0)
    except ValueError:
        raise ValueError('\nvalues for seats and tables must be ints.\n\n')

    for sec in sections:
        sec=str(sec)
        students = classutils.get_section(sec)
        
        try:
            assert(len(students)>0)
        except AssertionError:
            print(sec, type(sec))
            print(all_students[24].section, type(all_students[24].section))
            raise
        print(sec+'.txt')
        seat_randomizer.seat_randomizer(sec,tables,seats,
            filename=sec+".txt", msg=str(sec)+" lab "+str(lab))
    return

def print_scores(assignments,section):
    """
    input params:
    -------------
    assignments : a list of assignment names to use.    Should follow whats in Data/data.cfg
    sections : the list of sections to use.    if None, will do all in classutils.cfg_dict['mysections']

    output:
    -------
    a string of data to be printed
    """
    string = ''
    lst=classutils.get_section(str(section))

    assert(len(lst)>0 and type(assignments) is list)

    string += "\n\nsection: "+str(section)+\
    "     mean            std. dev."+\
    "\n===========================================\n"
    for assignment in assignments:
        assert(type(assignment) is str)
        scores = classutils.Student.getStats(assignment, lst)
        string += "    %(asgn)-12s    %(mean)-6.3lf           %(std)-6.3lf\n"%{'asgn':assignment, 'mean':scores[0], 'std':scores[1]}
    scores = classutils.Student.get_all_stats(lst)
    string+="-------------------------------------------\n"
    string+="    totals:         %(mean)-6.3lf           %(std)-6.3lf\n"%{'mean':scores[0], 'std':scores[1]}
    return string

def automate_grade_email(unames,section, text='Subject: Phys 1BL: grades\n\n'):
    text+=print_scores(thisweek,section)
    filename=str(section)+'_grades.txt'
    f=open(filename,'w').write(text)
    send_email(unames+[ classutils.cfg_dict['Email']['myuname']+'@ucsd.edu' ], classutils.cfg_dict['Email']['smtpserver'], 
                filename, classutils.cfg_dict['Email']["port"])
    return

def send_email(to, 
               server=classutils.cfg_dict["Email"]["smtpserver"],
               email_file=classutils.cfg_dict["Email"]["email_text"],
               port_num=classutils.cfg_dict["Email"]["port"]):

    try:
        port = int(port_num)
    except:
        port = None
        
    message = open(email_file).read()
    print("\nrecipients = "+str(to))
    print("\n"+message)
    yn = input("is this what you want to send? (y/n)")
    if yn!='y':
        return

    try:
        smtpserver = smtplib.SMTP(server,port)
    except:
        print(server)
        print("port = "+str(port))
        raise
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    try:
        user = input('username:')
        while '@' not in user:
            user = input('username needs \'@\'\nusername:')
            
        pswd = getpass()
        smtpserver.login(user, pswd)
    except smtplib.SMTPAuthenticationError:
        print("login failed.    try again.")
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
        print('these emails failed:'+repr(failed_sent))

    smtpserver.close()
    return

if __name__=='__main__':
    assign_seats() 

    #for an automated weekly email, to be performed upon running this code:
    all_sections=[]
    for section in mysections:
        lst=classutils.get_section(section)
        all_sections+=lst
        unames=classutils.Student.get_emails(lst)
        automate_grade_email(unames,section)
        
    #for a general mass email to all sections, fill in Data/email_text.txt as desired
    #unames=classutils.Student.get_emails(classutils.get_section('842222')+classutils.get_section('842226'))

    print(unames)

    """unames=classutils.Student.get_emails(all_sections)

    send_email(unames+[classutils.cfg_dict['Email']['myuname']+'@ucsd.edu'],
        server=classutils.cfg_dict['Email']['smtpserver'],
        port_num=classutils.cfg_dict['Email']["port"])
    """

