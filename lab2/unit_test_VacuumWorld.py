from vacuum_world_classes_def import *
import unittest




class TestProblem1(unittest.TestCase):


 def test_vacuum_world(self):
     #state=["Dirty", "Dirty"]
     #location = 0
     #seq = []
     a = VacuumAgent() # a vacuum cleaner agent
     self.assertEqual(a.run(["Dirty", "Dirty"], 0, []), ["Suck", "Right", "Suck"])
     self.assertEqual(a.run(["Dirty", "Dirty"], 1, []), ["Suck","Left", "Suck"])
            
             

if __name__ == '__main__':
   unittest.main()

  
