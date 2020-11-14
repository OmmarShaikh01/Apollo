import unittest

from apollo.utils import ConfigManager

class TestConfigManager(unittest.TestCase):
    
    def setUp(self):
        self.config_manager = ConfigManager()
        self.jsondict = {
            "destination_addresses": [
              "Philadelphia, PA, USA"
            ],
            "origin_addresses": [
              "New York, NY, USA"
            ],
            
            "rows": {
              "elements": {
                "distance": {
                  "text": "94.6 mi",
                  "value": 152193
                },
                "duration": {
                  "text": "1 hour 44 mins",
                  "value": [6227, 1324]
                },
                "status": "OK"
              }
            },
            "status": "OK"
          }
               
                  
    def test_Getvalue(self):
        
        # tests the handling of an empty path argument
        self.assertEqual(self.jsondict, self.config_manager.Getvalue(self.jsondict, ""))
        
        # tests for existance of data value
        self.assertEqual("94.6 mi", self.config_manager.Getvalue(self.jsondict, "rows/elements/distance/text"))
        self.assertEqual([6227, 1324], self.config_manager.Getvalue(self.jsondict, "rows/elements/duration/value"))
        
        
        # tests for handling non existance keys indexing
        self.assertEqual(None, self.config_manager.Getvalue(self.jsondict, "rows/elements/distance/text_NONE"))
        
        
    def test_Setvalue(self):
        # tests the handling of an empty path argument
        self.assertEqual(None, self.config_manager.Setvalue("TEST", self.jsondict, ""))
        
        # tests for updation of data value
        self.config_manager.Setvalue("TEST", self.jsondict, "rows/elements/distance/text")
        self.assertEqual("TEST", self.config_manager.Getvalue(self.jsondict, "rows/elements/distance/text"))
        
        self.config_manager.Setvalue("TEST", self.jsondict, "rows/elements/duration/value")
        self.assertEqual([6227, 1324, "TEST"], self.config_manager.Getvalue(self.jsondict, "rows/elements/duration/value"))
        
        # tests for handling non existance keys indexing
        self.config_manager.Setvalue("TEST", self.jsondict, "rows/elements/distance/text_NONE")
        self.assertEqual("TEST", self.config_manager.Getvalue(self.jsondict, "rows/elements/distance/text_NONE"))
        
        
if __name__ == '__main__':
    unittest.main()
