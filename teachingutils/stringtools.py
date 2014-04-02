import re
from teachingutils.error import EmptyString
from string import printable


"""
this module includes various functions for taking data from csv into a usable 
form for the rest of this code.    the core thing here is getData() which parses 
data into a list of students.
"""

def extraComma(string):
    for item in string.split('\",\"'):
        if ',' in item:    
            return True
    return False

def stripExtraCommas(filename):
    """
    since we are using csv data with the delimiter:    
        "value","newvalue"

    we need to strip off excess commas in the case where the data is like:
        "value","value,with a comma"

    input:
    ---------------------------
    a filename of csv data delimited with ","

    output:
    ---------------------------
    None
    """
    f = open(filename,'r')
    data = f.readlines()
    newdata = []

    for string in data:
        string = string.replace(',\"\n\"',',\"\"\n\"')
        strlist = string.split('\",\"')
        for i in range(0,len(strlist)):
            strlist[i] = strlist[i].replace(',','')
        newdata.append('\",\"'.join(strlist))
    f.close()

    f = open(filename,'w')
    f.writelines(newdata)
    f.close()
    return

def non_blank(filestream):
    """return lines which are neither empty, nor contain any # symbols"""
    for line in filestream:
        lines = line.rstrip()
        if lines and lines[0]!='#':
            yield lines 

def sanitize(string,ishead=False):        #issue maybe with stray quotes....maybenot.
    """
    erase all text that is not alphanumeric text or underscores.
    
    head is True if the input string will be used as a head item
    if true, then only '_' and alphanumeric characters are allowed.
    otherwise, a wider range of chars are permitted.

    also, due to restrictions of named_tuple, head cannot start with number:
    to fix this, append 'N' to front.    (name doesn't matter since this item)
    will never get used anyway.
    """

    if type(string) is list:
        return[sanitize(item,ishead) for item in string]

    if string == '': return '' if not ishead else 'NULL'
    

    string = re.sub("[^{}]+".format(printable), "", string)
    string = re.sub(r'\s+','_',((string.lower()).strip())) #replace whitespace w _
    if ishead:
        string = re.sub(r'[^0-9a-zA-Z_\?]+','_',string)
        if string[0].isdigit() or string[0]=='_':
            string = 'N'+string
    else:
        string = re.sub(r'[^0-9a-zA-Z_\.\?]+','_',string)
    return re.sub(r'_+','_',string)     #    replace recurring instances of _ 

def sanitizeDict(a_dict,ishead=True):
    vals = []
    keys = []
    new_dict = {}
    for key, val in a_dict.items():
        keys.append(sanitize(key,ishead))
        vals.append(sanitize(val,ishead))
    
    for i in range(0,len(keys)):
        if keys[i]=='':    keys[i]=='NULL'
        if vals[i]=='':    vals[i]=='NULL'
        new_dict[keys[i]] = vals[i]
    return new_dict    


def indices(lst,value):
    for i, x in enumerate(lst):
        value = str(value)
        x = str(x)
        y = x[:len(str(value))] if len(str(value)) < len(str(x)) else x  #truncate if necessary
        if sanitize(rm_nums(y))==sanitize(rm_nums(value)):
            yield i, y
        
def sanitizeKeys(cfg_dict,lst):
    """
    sanitize all strings to pure alphanumeric or underscores.
    lst is incoming header data
    replace ? by appropriate number
    """
    cfg_dict = sanitizeDict(cfg_dict,True)
    lst = sanitize(lst,True)

    for key, value in cfg_dict.items():    #map fieldnames to list of keys
        if not '?' in key:    
            if value in lst:
                lst[lst.index(value)] = key
            else:
                continue
        else:
            for j, y in indices(lst,value):  #for every element of the header that we care about replace ? with number            
                num = get_nums(value,y)
                if num is None: 
                    continue
                newKey = key.replace('?',str(num))
                lst[j] = newKey
    return lst

def rm_nums(string,specialChar='?'):
    """
    rm digits and any other special chars
    """
    return re.sub(r'[0-9]+|\?+','',string)

def rm_nums_replace(string):
    """
    replace nums with ?
    """
    return re.sub('[0-9]+','?',string)

def get_nums(var,raw):
    """
    find num in raw to replace specialChar in var with first number
    """
    #in case the order gets messed up:
    var = sanitize(var)
    raw = sanitize(raw)

    result1 = re.findall(r'[0-9]+|\?+',var)
    result2 = re.findall(r'[0-9]+|\?+',raw)
    assert(len(result1)==len(result2))
    try:
        ind= result1.index('?')     #worries about this if #digits don't mach string digit number
        return result2[ind]
    except ValueError:
        return None

def numConvert(string):
    """
    for a string that should be an int, remove any weird chars and strip off 
    everything right of the decimal.    Do not use if not head

    for example:    section number    written as 84455.0 will be 84455

    """
    string = re.sub(r'[^0-9\.]','',string)
    return string.split('.')[0]


