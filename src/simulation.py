import numpy as np
import inspect
import src.rules.cell_rules as cr
import src.rules.env_rules as er
from src.environment import Environment

class Simulation:
    def __init__(self, envrule, cellrule):
        self.envrule = getattr(er, envrule)()
        self.cellrule = getattr(cr, cellrule)()
        self.env = Environment(self.envrule, self.cellrule) # Initialize the environment
        self.update_rules(new_envrule=self.envrule, new_cellrule=self.cellrule)
    
    def update_rules(self, new_params=None, new_envrule=None, new_cellrule=None):
        if new_params: 
            self.params.update_params(new_params)
            
        if new_envrule:
            envrules = inspect.getmembers(er, inspect.isclass) # Get all rules as functions
            self.envrule = next((r for r in envrules if r[0] == type(new_envrule).__name__), None) # Get the first object that matches the wanted envrule
            if not self.envrule: raise AttributeError(f"{new_envrule} is not a valid simulation ruleset. [{', '.join(r[0] for r in envrules)}]")
            setattr(self.env, self.envrule[0], self.envrule) # Bind the desired rule method to the environment
        
        if new_cellrule: 
            cellrules = inspect.getmembers(cr, inspect.isclass) 
            cellrule = next((r for r in cellrules if r[0] == type(new_cellrule).__name__), None)
            if not cellrule: raise AttributeError(f"{new_cellrule} is not a valid cell ruleset. [{', '.join(r[0] for r in cellrules)}]")
            self.env.cellrule = cellrule
            for c in self.env.cells:
                setattr(c, cellrule[0], cellrule)
                c.cellrule = cellrule

    def next(self):
        if np.any(self.env.cells):
            getattr(self.env, self.envrule[0])(self.env)
        else:
            exit()