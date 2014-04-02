import unittest
from teachingutils.classUtils import *
import os.path

class DataTest(unittest.TestCase):
  def setUp(self):
    path, _ = os.path.split(__file__)
    self.cfg_file = os.path.join(path,'config_test.cfg')
    assert(os.path.isfile(self.cfg_file))
    self.cfg_dict = read_config(filestream=open(self.cfg_file,'r'))
    self.csv_file = 'csv_test.csv'
  def tearDown(self):
    self.cfg_dict = None
    self.cfg_dict = None
    self.csv_file = None

  def test_config(self):
    test_dict = {  
      'some':'the',
      'header':'first',
      'data':'row',
      'test_$':'column_$',
      'csvfile':os.path.abspath(os.path.join('teachingutils', 'Tests', 'csv_test.csv'))}
    try:
      self.assertEqual(self.cfg_dict,test_dict)
    except:
      print("cfg_dtc")
      print((self.cfg_dict))
      print("\n\nnot equal to:")
      print(test_dict)
      raise
  
  def test_getData(self):
    testList = getData(cfg_dict=self.cfg_dict)  #hope it doesn't fail
    assert(testList is not None)
    try:
      self.assertEqual(len(testList),2)
    except:
      print(("list is:"+str(testList)))
      raise
    for item in testList:
      self.assertEqual(len(item._fields),6)

