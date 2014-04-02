import unittest
from teachingutils.stringtools import *
import re

class stringTest(unittest.TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_sanitize(self):

    test1 = sanitize("\",\"     + ...   *LAst     nAME \"\'##$",True)    
    test2 = sanitize("\",\"     + ...   *LAst  .   nA.ME \"\'##$",False)
    test3 = sanitize("\r\n\n\n  lastNaMe  \t\"\"\"")
    test4 = sanitize(["a","list","he%%re"],True)

    self.assertTrue(test1=='N_last_name_$',test1)  #prepend with N, replace weird chars with _ except for $
    self.assertTrue(test2=='_..._last_._na.me_$',test2) #all weird chars replaced except . and $
    self.assertTrue(test3=='lastname',test3)  #check special line characteristic chars
    self.assertTrue(test4==['a','list','he_re'],test4)
    self.assertTrue(sanitize('\n')=='')
    self.assertTrue(sanitize('\ntest')=='test')
    self.assertTrue(sanitize('',False)=='')
    self.assertTrue(sanitize('',True)=='NULL')

  def test_generator(self):
    lst = [0,'hey','dont','test','include','test','test','me',True,False,1.2,'test']
    value = "test"

    newlst = [lst[i] for i in indices(lst,value)]
    testlst= ['test','test','test','test']

    indexlst=[i for i in indices(lst,value)]
    testindex=[3,5,6,11]

    self.assertTrue(newlst==testlst)       #test the correct values passed
    self.assertTrue(testindex==indexlst)  #test the correct indices

  def test_keys(self):
    cfg_dict = {'test':'  [2345234 ;; value',
                'must test$':'the \"\" value  $',
                'ok.test $  this $':'this (  $  value$'}

    lstt = ['  [2345234 ;; value',  
            '  [2345234 ;; value', 
            'the \"\"\n\r value 4',
            'the \"\" value   5',
            'the \"\"{ value  6',
            'this (  12  value3',
            'this (  14  value5', 
            'this_should not+be in the list' ]

#get_nums only returns first instance of a number.
    result=[ 'test','test', 'must_test4', 'must_test5', 'must_test6',  \
          'ok_test_12_this_12', 'ok_test_14_this_14',  \
          'this_should_not_be_in_the_list' ]

    try:
      self.assertTrue(result==sanitizeKeys(cfg_dict,lstt))
    except AssertionError:
      print("\nlstt:")
      print(lstt)
      print("\ncfg_dict")
      print(cfg_dict)
      print("\nresult:")
      print(result)
      print("\nsanitized dict:")
      print((sanitizeKeys(cfg_dict,lstt)))
      raise

  def test_get_nums(self):
    self.assertTrue(get_nums('  hi \n\n \" $','  hi  5')=='5')  


######got it!!!  extra \" breaks the csv file!!!! arg!!!

