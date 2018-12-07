

class VacuumAgent:

  def goal_test(self, state):
              if state==["Clean", "Clean"]:
                            return True
              else:
                            return False
       
  def action(self, state, location):
              if state[location] == "Dirty":
                            action = "Suck"
              elif location == 0:
                            action = "Right"
              else:
                            action = "Left"
              return action

       
       
 
  def update_state(self, state, action, location):
              if action=="Suck":
                     state[location] = "Clean"
                                      
              elif action=="Left":
                   location = 0
              else:
                   location = 1             
              return state, location
       

  def run(self, state, location, seq):

       
              
       while True:
              if self.goal_test(state):
                            return seq
              action = self.action(state, location)
              seq.append(action)
              state, location = self.update_state(state, action, location)

       

       
  
                            
