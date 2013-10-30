import unittest
from TeachingUtils.classUtils import *

class DataTest(unittest.TestCase):
  def setUp(self):
    self.cfg_file = 'config_test.cfg'
    self.cfg_dict = read_config(filename=self.cfg_file)
    self.csv_file = 'csv_test.csv'
  def tearDown(self):
    self.cfg_dict = None
    self.cfg_dict = None
    self.csv_file = None

  def test_config(self):
    self.assertEqual(self.cfg_dict,{'some':'the','header':'first','data':'row','test_$':'column_$'})
  
  def test_getData(self):
    testList = getData(cfg_dict=self.cfg_dict)  #hope it doesn't fail
    self.assertEqual(len(testList),2)
    for item in testList:
      self.assertEqual(len(item._fields),6)
