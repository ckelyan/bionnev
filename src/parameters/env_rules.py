import numpy as np
from classes.cell import Cell
from classes.rule_classes import EnvRule

class Rule0(EnvRule):
    def __init__(self):
        self.display_name = "dkjslfkjds"
        self.exp = """The cells each reproduce one new cell if they are a
                      subrectangle of the grid (can be chosen to be any).
                      Cells can have the same position. The new cells
                      inherit the exact same brain_dna as their parent.
                      Every new cell is then randomly put in the grid.
        """    
        self.params_dict = {
            "grid_size": {"val": 50, "exp": "Grid size."},
            "num_cells": {"val": 250, "exp": "Number of initial cells."},
            "regeneration_days": {"val": 10, "exp": "Frequency (in days) at which the cells reproduce."},
            "percent_grid": {"val": 0.6, "exp": "Number of."},
        }
        super().__init__()
        
    def env_func(_, env):
        reproduceable_cells = [cell for cell in env.cells if cell.pos[0] <= int(env.grid_size/4)]
        for cell in env.cells:
            cell.reproduceable = cell in reproduceable_cells

        if env.clock % env.params['regeneration_days'] == 0: 
            new_cells = env.create_cells(len(reproduceable_cells))
            
            for i,c in enumerate(new_cells):
                c.pos = np.random.uniform(0, env.grid_size-1,2) 
                c.brain_dna = reproduceable_cells[i].brain_dna 
                
            env.cells.extend(new_cells) 


class Rule1(EnvRule):
    def __init__(self):
        self.display_name = "Simple rectangle overlap"
        self.exp = """The cells each reproduce one new cell if they are a
                      subrectangle of the grid (can be chosen to be any).
                      Cells can have the same position. The new cells
                      inherit the exact same brain_dna as their parent.
                      Every new cell is then randomly put in the grid. 
        """    
        self.params_dict = {
            "grid_size": {"val": 30, "exp": "Grid size."},
            "num_cells": {"val": 10, "exp": "Number of initial cells."},
            "regeneration_days": {"val": 10, "exp": "Frequency (in days) at which the cells reproduce."},
            "horizontal": {"val": 1, "exp": "Variable that dicates if the zone is divided through an horizontal (1) or vertical(0) line."},
            "bottom": {"val": 1, "exp": "Variables that dictates if the zone is for the min of the coordinate (-1) or max(1)"},
        }
        super().__init__()
        
    def env_func(_, env):
        reproduceable_cells = [cell for cell in env.cells if env.params['bottom'] * cell.pos[env.params['horizontal']] >= env.params['bottom'] *int((env.grid_size-1)*env.params['percent_grid'])]
        for cell in env.cells:
            cell.reproduceable = cell in reproduceable_cells

        if env.clock % env.params['regeneration_days'] == 0: 
            new_cells = env.create_cells(len(reproduceable_cells))
            for i,c in enumerate(new_cells):
                c.pos = np.random.uniform(0, env.grid_size-1,2) 
                c.brain_dna = reproduceable_cells[i].brain_dna 
                
            env.cells.extend(new_cells) 

class Rule2(EnvRule):
    def __init__(self):
        self.display_name = "Rule2"
        self.exp = "The cells each reproduce one new cell if they are in a specific corner of the grid. Every new cell is then randomly put in the grid ."    
        self.params_dict = {
            "grid_size": {"val": 30, "exp": "Grid size."},
            "num_cells": {"val": 30, "exp": "Number of initial cells."},
            "regeneration_days": {"val": 10, "exp": "Frequency (in days) at which the cells reproduce."},
            "percent_grid": {"val": 0.5, "exp": "Number of."},
            "left": {"val": 1, "exp": "Variable that dicates if the corner is on the left(-1) or the right(1)."},
            "bottom": {"val": 1, "exp": "Variables that dictates if the zone is for the bottom(-1) or top (1)"},
        }
        super().__init__()

    def env_func(_, env):
        reproduceable_cells = [cell for cell in env.cells if ((-env.params['left']*cell.pos[1] -env.params['bottom']*cell.pos[0]) <= int((env.grid_size-1)*env.params['bottom']*env.params['left']*((env.params['percent_grid']-((env.params['bottom']>0) + (env.params['left']>0))))))]
        for cell in env.cells:
            cell.reproduceable = cell in reproduceable_cells

        if env.clock % env.params['regeneration_days'] == 0: 
            new_cells = env.create_cells(len(reproduceable_cells))
            
            for i,c in enumerate(new_cells):
                c.pos = np.random.uniform(0, env.grid_size-1,2) 
                c.brain_dna = reproduceable_cells[i].brain_dna 
                
            env.cells.extend(new_cells) 
        return 1
    
class Rule3(EnvRule):
    def __init__(self):
        self.display_name = "Rule3"
        self.exp = ""
        self.params_dict = {
            "grid_size": {"val": 30, "exp": "Grid size."},
            "num_cells": {"val": 30, "exp": "Number of initial cells."},
            "regeneration_days": {"val": 10, "exp": "Frequency (in days) at which the cells reproduce."},
            "min_strength" : {"val": 5, "exp": "Minimal stregth to reproduce."}
        }
        super().__init__()
        
    def env_func(_, env):
        reproduceable_cells = [cell for cell in env.cells if cell.strength >= env.params['min_strength']]
        
        for cell in env.cells:
            cell.reproduceable = cell in reproduceable_cells
            
        if env.clock % env.params['regeneration_days'] == 0:
            new_cells = env.create_cells(len(reproduceable_cells))
            
            for i, c in enumerate(new_cells):
                # c.pos = np.array([(env.grid_size / 2), (env.grid_size / 2)])
                c.pos = np.random.uniform(0, env.grid_size - 1, 2)
                c.brain_dna = reproduceable_cells[i].brain_dna
                
            env.cells.extend(new_cells)
            
        return 1

class Rule4(EnvRule):
    def __init__(self):
        self.display_name = "Oui!"
        self.exp = ""
        self.params_dict = {
            "grid_size": {"val": 30, "exp": "Grid size."},
            "num_cells": {"val": 10, "exp": "Number of initial cells."},
            "regeneration_days": {"val": 1000, "exp": "Frequency (in days) at which the cells reproduce."},
            "min_strength" : {"val": 0, "exp": "Minimal stregth to reproduce."},
            "min_strength" : {"val": 0, "exp": "Minimal stregth to reproduce."},
        }
        super().__init__()
        
    def env_func(_, env):
        reproduceable_cells = [cell for cell in env.cells if cell.strength >= env.params['min_strength']]

        for cell in env.cells:
            cell.reproduceable = cell in reproduceable_cells
            
        if env.clock % env.params['regeneration_days'] == 0:
            new_cells = env.create_cells(len(reproduceable_cells))
            
            for i, c in enumerate(new_cells):
                c.pos = np.rint(np.random.uniform(0, env.grid_size - 1, 2))
                c.brain_dna = reproduceable_cells[i].brain_dna
                
            env.cells.extend(new_cells)
            
        return 1
    
class Rule5(EnvRule):
    def __init__(self):
        self.display_name = "Clusters"
        self.exp = "The cells can reproduce if they are in a \"cluster\" of cells"
        self.params_dict = {
            "grid_size": {"val": 200, "exp": "Grid size."},
            "num_cells": {"val": 50, "exp": "Number of initial cells."},
            "num_safe_frames": {"val": 10, "exp": "Number of safe frames a cell has to have been in to be able to reproduce."},
            "req_neighbors": {"val": 1, "exp": "Amount of neighbors (other cells around it) the cells need to be able to reproduce."},
        }
        super().__init__()
        
    def env_func(_, env):
        candidate_cells = [cell for cell in env.cells if cell.neighbors >= env.params['req_neighbors']]
        reproduceable_cells = []
        
        for cell in env.cells:
            if cell in candidate_cells:
                cell.safe_frame_count += 1
            else:
                cell.safe_frame_count = 0

            cell.reproduceable = cell.safe_frame_count >= env.params['num_safe_frames']

            if cell.reproduceable:
                reproduceable_cells.append(cell)
                cell.reproduceable = False
                cell.safe_frame_count = 0

        new_cells = env.create_cells(len(reproduceable_cells))
        env.add_cells(new_cells, reproduceable_cells)
            
        return 1

class Rule6(EnvRule):
    def __init__(self):
        self.display_name = "Delayed subrec"
        self.exp = """The cells can reproduce after staying n frames inside
                      a subrectangle.
        """    
        self.params_dict = {
            "grid_size": {"val": 100, "exp": "Grid size."},
            "num_cells": {"val": 100, "exp": "Number of initial cells."},
            "num_safe_frames": {"val": 50, "exp": "Number of safe frames a cell has to have been in to be able to reproduce."}
        }
        self.cell_attributes = {
            "safe_frame_count": {"initial_val": 0, "exp": "Number of consecutive frames a cell has been safe"}
        }
        super().__init__()
        
    def env_func(_, env):
        candidate_cells = [cell for cell in env.cells if cell.pos[0] <= int(env.grid_size/4)]
        reproduceable_cells = []
        
        for cell in env.cells:
            if cell in candidate_cells:
                cell.safe_frame_count += 1
            else:
                cell.safe_frame_count = 0

            cell.reproduceable = cell.safe_frame_count >= env.params['num_safe_frames']
            
            if cell.reproduceable:
                reproduceable_cells.append(cell)
                cell.reproduceable = False
                cell.safe_frame_count = 0
 
        new_cells = env.create_cells(len(reproduceable_cells))
        
        for i,c in enumerate(new_cells):
            c.pos = np.random.uniform(0, env.grid_size, 2)
            c.brain_dna = reproduceable_cells[i].brain_dna

        env.cells.extend(new_cells)