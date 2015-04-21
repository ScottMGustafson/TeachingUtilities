import os
from configparser import ConfigParser
import string
from numpy import std, mean

def read_config(file = 'configdata.cfg'):
    """
    read the configuration file, by default configdata.cfg.
    returns a dict containing relevant config info.
    """

    config = ConfigParser()
    config.read(file)
    assert(os.path.isfile(config['Config']['csvfile'].strip()))
    return config

def reader(filename, delimiter=',', quotechar="\""):
    f = open(filename,'r')
    data = []
    for line in f:
        line  = ''.join(filter(lambda x:x in string.printable, line))
        line=line.replace(quotechar, "")
        data.append([item.strip() for item in line.split(delimiter)])
    header = data.pop(0)
    return [Student(dict(zip(header, item))) for item in data ]  

def reverse_lookup(dic, key):
    for k, v in dic.items():
        if v==key:
            return k
    raise KeyError(key)

cfg_dict = read_config()
aliases = cfg_dict['Column Headers']
assignment_map={}

def convert(string, char='?'):
    """
    this converts a messier header name to something neater.
    key formats specified in config file where identifiers notated by \'?\'

    example:
    in config file we specify:
    conc?  = Conclusion?blahblahblah 88458924532453

    in actual datafile we find Conclusion02blahblahblah 88458924532453
    which maps over to 
    conc02
    """
    

    #need to find a better, more general name to parse headers
    for key, value in cfg_dict["Assignments"].items():
        val=value.split(char)
        val[0] = val[0].strip()
        val[1] = val[1].strip()
        if val[0] in string:
            unique=string.replace(val[0],"")[0:2]
            ret_val = key.split(char)
            assignment_map[string]=ret_val[0]+unique 
            return ret_val[0]+unique 
    return None
    

class Student(object):
    def __init__(self, row,char='?'):
        """row is a dict"""
        aliases = cfg_dict['Column Headers']
        for k, v in aliases.items():  
            setattr(self,k,row[v])

        for key, val in row.items():
            key=key.strip()
            if not key in assignment_map.keys():
                key=convert(key)
                
            try:
                newkey=assignment_map[key]
                #print(newkey)
                setattr(self,newkey,val)
            except KeyError:
                pass

    def __str__(self):
        return self.firstname+' '+self.lastname

    def get_total(self):
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
        for key in list(self.__dict__.keys()):

            if key in assignment_map.values():
                try:
                    summ+=float(getattr(self,key))
                except:
                    if getattr(self,key)=='' or getattr(self,key)==None:
                        continue
                    else:
                        raise ValueError("cannot convert: "+str(getattr(self,key)))
        return summ
        
    @staticmethod
    def get_list(section, data):
        if type(data) is str:
            data=reader(data)
        return [Student(item) for item in data if item[aliases['section']]==section]            
    
    @staticmethod
    def get_column(studentlist, key):
        """get all values for all students in a section"""
        key=str(key)
        assert(not key is None)
        #try:
        #    key=reverse_lookup(assignment_map, key)   
        #    assert(not key is None)   
        #except KeyError:
        #    for key, val in assignment_map.items():
        #        print(key, val)
        #    raise
        try:
            return [getattr(item, key) for item in studentlist]
        except TypeError:
            print(key)
            raise
        except:
            print(assignment_map)
            print(key)
            print(dir(studentlist[0]))
            raise

    @staticmethod
    def getStats(assignment, studentlist):
        """
        input:    assignment name (str), section number
        output: tuple of (mean, stdev).    returns None on failure
        """
        try:
            assert(assignment in assignment_map.values())
        except:
            raise Exception(str(assignment)+" not in "+str(assignment_map.values()))
        col = Student.get_column(studentlist, assignment)
        for i in range(0,len(col)):
            try:
                col[i]=float(col[i])
            except ValueError:
                col[i]=0.
        return mean(col), std(col), col

    @staticmethod
    def get_all_stats(studentlist):
        lst = [item.get_total() for item in studentlist]
        return mean(lst), std(lst), lst

    @staticmethod
    def get_emails(studentlist, ext=cfg_dict["Email"]["emailext"]):
        return [item.username+'@'+ext for item in studentlist]

all_students=reader(cfg_dict["Config"]["csvfile"])

def get_section(section):
    return [item for item in all_students if item.section==section]
