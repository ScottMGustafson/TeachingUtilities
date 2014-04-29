import csv
import re
import os
from . import stringtools
from configparser import ConfigParser
from .error import *
import warnings


def defaultfilepath(cfgpath=os.path.join('Data','configdata.cfg')): 
    """get the path to the default location for the data directory"""
    data_path, _ = os.path.split(__file__)
    data_path_lst = data_path.split(os.sep)
    data_path = (os.sep).join(data_path_lst[0:-1])
    data_path = os.path.join(data_path,cfgpath)
    try:
        if not os.path.isfile(data_path):
            raise FileDNE(data_path)
    except FileDNE:
        raise
    return os.path.abspath(data_path)

@lenchecker
def read_config(file = os.path.join('Data','configdata.cfg')):
    """
    read the configuration file, by default configdata.cfg.
    returns a dict containing relevant config info.
    """

    config = ConfigParser()
    config.read(file)
    assert(os.path.isfile(config['Config']['csvfile'].strip()))
    try:
        assert(os.path.isfile(config['Email']['email_text'].strip()))
    except:
        warnings.warn("email_text not specified in "+filestream)
    for key, val in dict(config["Column Headers"]).items():       
        key = stringtools.sanitize(key)   #should be unneccessary
        val = stringtools.sanitize(val) 
        config["Column Headers"][key] = val

    for key, val in list(config["Assignments"].items()):       
        key = stringtools.sanitize(key)   #should be unneccessary
        val = stringtools.sanitize(val) 
        config["Assignments"][key] = val
    return config


def getData(cfg_dict=None, mySection=None,verbose=False):    #this code only works if csv.reader returns a list
    """
    input a csv file
    output a list of student instances
    """
    if not cfg_dict: cfg_dict = read_config()
    stringtools.stripExtraCommas(cfg_dict['Config']['csvfile'])
    gradeFile = csv.DictReader(open(cfg_dict['Config']['csvfile']), delimiter=',', quotechar='\"')

    if mySection==None:
        mySection = [ item.strip() for item in list(cfg_dict['Config']['mysections'].split(',')) ]
    else:   
        mySection = [ str(mySection) ]


    old_keys = gradeFile.fieldnames

    #concatenate two configparser sections into one dict
    keys = dict(cfg_dict['Column Headers'])
    keys.update(dict(cfg_dict['Assignments']))

    #map new keys onto old keys
    new_keys = stringtools.sanitizeKeys(keys, old_keys) 

    studentList = []
    for row in list(gradeFile):
        for i in range(0,len(old_keys)): 
            row[ new_keys[i] ] = row.pop(old_keys[i]) 
        row['section'] = str(stringtools.numConvert(row['section'].split('.')[0]))

        if row['section'] in mySection:
            studentList.append(row)

    if len(studentList)==0:
        print(str(mySection))
    return studentList

def init_it(section=None):
    cfgdict = read_config()
    mysections = [int(item.strip()) for item in list(cfgdict['Config']['mysections'].split(','))]
    if section is None:
        lst = []
        for item in list(cfgdict["Config"]["mysections"].split(',')):
            lst+=getData(cfg_dict=cfgdict,mySection=item.strip())
    else:
        lst = getData(cfg_dict=cfgdict,mySection=section)
    if len(lst)==0: 
        raise EmptyList("student list is empty for section "+str(section))
    return lst, cfgdict

