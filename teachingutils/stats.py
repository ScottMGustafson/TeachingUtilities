from .classutils import init_it
from .stringtools import *
import numpy as np
from warnings import warn

"""
Some functions to get relevant statistics
"""
def getStats(assignment, section, studentlist, cfg_dict):
    """
    input:    assignment name (str), section number
    output: tuple of (mean, stdev).    returns None on failure
    """
    if not rm_nums_replace(assignment) in dict(cfg_dict['Assignments']).keys():
        raise Exception(assignment+" not in "+str(dict(cfg_dict['Assignments']).keys()))
    data = []

    for item in studentlist:
        try:
            data.append(float(item[assignment]))
        except KeyError:
            raise KeyError(assignment+" not in "+str(item.keys()))
        except:    #item is presumably None
            if item[assignment] is None or item[assignment]=='':
                pass
            else:
                raise ValueError(assignment+": "+item[assignment])
    return np.mean(data), np.std(data)
    
def getOverallStats(section, studentlist, cfg_dict):
    """
    input:    section
    output:    tuple of (mean, stdev)
    """
    data=[getTotal(item,cfg_dict) for item in studentlist]
    try:
        return np.mean(data),np.std(data)
    except:
        print(data)
        raise

def getTotal(student, cfg_dict):
    """
    get the totals for a student.
    input:
    ----------------------------
    student: an instance of Student
    cfg_dict: the configuration dictionary defined in classUtils.read_config

    output:
    ----------------------------
    score summed over all assignments
    
    """
    summ = 0.
    for item in list(student.keys()):
        if rm_nums_replace(item) in cfg_dict['Assignments'].keys():
            try:
                summ+=float(student[item])
            except:
                if student[item]=='' or student[item]==None:
                    continue
                else:
                    raise ValueError("cannot convert: "+str(student[item]))
    return summ

    
