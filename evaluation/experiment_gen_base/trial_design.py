from copy import deepcopy
import functools
from typing import List, Tuple
from collections.abc import MutableMapping
from utils.to_string import obj_to_string

class TrialDesign(dict):
    ''''
    Dict of factor:level with two fields
    id: a code of levels selected
    factors_map: a map with the levels selected
    '''
    def __init__(self):
        self._code = None
        self._factors_list = []

    def add_factor(self, factor, level, level_code):
        self[factor] = level
        self._factors_list.append((factor, level_code))
    
    @property
    def code(self) -> str:
        if self._code == None:
            code = ''
            for _, level_code in self._factors_list:
                code += level_code
            self._code = code
        return self._code
    
    @property
    def factors_map(self):
        def set_pair_on_map(map, elem):
            map[ elem[0] ] = elem[1]; 
            return map
        return functools.reduce(set_pair_on_map,self._factors_list,{})

class Factor:
    def __init__(self, property, levels):
        self.property, self.levels = property, levels

def flatten(d, parent_key='', sep='_'):
    ''' 
    Transform a nested dictionary into a flat one
    '''
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def total_combinations(factors) -> Tuple[List[TrialDesign], dict]:
    # starting with a empty 'seed_trial' that is further 'forked'
    # with possible levels of factors
    #factors = flatten(factors)
    seed_trial = TrialDesign()

    all_combinations = [seed_trial]

    code_map = {}
    next_code_index = 0
    for factor, levels in factors:
        # for each factor, recombine the combinations up to now
        # with each level of the here selected factor
        last_combination = all_combinations
        all_combinations = []
        code_map[next_code_index] = {'factor': factor}
        for trial in last_combination:
            level_code = 'a'
            for level in levels:
                code_map[next_code_index][level_code] = list(map(obj_to_string, level))
                new_trial = deepcopy(trial)
                new_trial.add_factor(factor, level, level_code)
                all_combinations.append(new_trial)
                level_code = chr(ord(level_code) + 1) # increment code
        next_code_index = next_code_index + 1

    code_map[next_code_index] = {
        "b": "baseline",
        "p": "planned",
        "factor": "treatment"
    } # finally, append 'factor' related to the treatment
    return all_combinations, code_map
        

def draw_without_repetition(source: List, number_of_draw:int, rand):
    drawn = rand.choice(source)
    if number_of_draw > 1:
        new_source = [ element for element in  source if element is not drawn ]
        return [drawn] + draw_without_repetition(new_source, number_of_draw - 1, rand)
    else:
        return [drawn]

def draw_with_repetition(source: List, number_of_draw:int, rand):
    drawn = rand.choice(source)
    if number_of_draw > 1:
        return [drawn] + draw_with_repetition(source, number_of_draw - 1, rand)
    else:
        return [drawn]