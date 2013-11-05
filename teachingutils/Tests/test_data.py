import unittest
from teachingutils.classUtils import *
import os.path

class DataTest(unittest.TestCase):
  def setUp(self):
    path, _ = os.path.split(__file__)
    self.cfg_file = os.path.join(path,'config_test.cfg')
    try:
      self.cfg_dict = read_config(filestream=open(self.cfg_file,'r'))
    except:
      print(self.cfg_file)
      raise
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
    self.assertEqual(self.cfg_dict,test_dict)
  
  def test_getData(self):
    testList = getData(cfg_dict=self.cfg_dict)  #hope it doesn't fail
    self.assertEqual(len(testList),2)
    for item in testList:
      self.assertEqual(len(item._fields),6)
