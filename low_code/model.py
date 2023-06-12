import operator

import pyomo.environ as pe
import pyomo.opt as po
import pandas as pd

from itertools import product

from indexes import Indexes
from parameter import Parameter

ops = {"+": operator.add,
       "-": operator.sub,
       '*': operator.mul,
       '<': operator.le,
       '<=': operator.eq,
       '=': operator.ne,
       '>': operator.gt,
       '>=': operator.ge,
       }


class Model:
    def __init__(self, data, name_indexes, name_parameters):
        self.data = data
        self.name_idx = name_indexes
        self.name_param = name_parameters
        self.indexes = []
        self.params = []

    def create(self, сonstraint_list):
        self.indexes = self.create_indexes()
        self.params = self.create_parameters()
        self.create_model(сonstraint_list)

    def create_indexes(self):
        return [Indexes(self.data, col).index() for col in self.name_idx]

    def create_parameters(self):
        return Parameter(self.name_idx, self.name_param, self.data).create()

    def create_model(self, сonstraint_list):
        model = pe.ConcreteModel()
        
        _ = [setattr(model, param, pe.Set(initialize=self.indexes[i]))
             for i, param in enumerate(self.name_idx)]

        # model.c[w, t] - время
        model.c = pe.Param(*[model.__getattribute__(name) for name in self.name_idx], initialize=self.params)
        # model.x[w, t] - пара индексов
        model.x = pe.Var(*[model.__getattribute__(name) for name in self.name_idx], domain=pe.Reals, bounds=(0, 1))

        # допустим, введена формула вида СУММА(param*idx)
        # целевая функция
        formula = 'time*все'
        f_split = self.proccess_string(formula)
        
        obj = []

        for word in f_split:
            if word == self.name_param:
                obj.append(model.c)
            if word == 'все':
                obj.append(model.x)
            if word.isdigit():
                obj.append(word)

        # не будет работать, если больше двух действий 
        pairs = list(product(*self.indexes))
        expr = sum(ops['*'](obj[0][p], obj[1][p]) for p in pairs)
        model.objective = pe.Objective(sense=pe.minimize, expr=expr)
 
        # ОГРАНИЧЕНИЯ
        сonstraint_list = сonstraint_list.split(';')
        model.cons = pe.ConstraintList()
        
        for constraint in сonstraint_list:
            string = constraint.split()

            new_idx = [i for i in self.name_idx]
            tmp = constraint.replace(" ", "").split(',')
            if tmp[1] in new_idx: 
                new_idx.remove(tmp[1].replace(' ', ''))
            
            idxes = [Indexes(self.data, col).index() for col in new_idx]
            new_pairs = list(product(*idxes))

            for i, symbol in enumerate(string):
                if (symbol == '=') or (symbol == '<=') or (symbol == '>=') or (symbol == '<') or (symbol == '>'):
                        for el in new_pairs:
                            rhs = int(string[i+1].replace(',', ''))
                            if '*' in string: 
                                lhs = sum(model.c[*el, t] * model.x[*el, t] for t in model.__getattribute__(tmp[1]))
                                model.cons.add(lhs <= rhs) # работает
                            else:
                                lhs = sum(model.x[t, *el] for t in model.__getattribute__(tmp[1])) # следить за порядком
                                model.cons.add(lhs == rhs) # работает
                            #model.cons.add(ops[symbol](lhs, rhs)) # не работает
        
        # СУММА ВОРК <= 40
        
        results = po.SolverFactory('gurobi').solve(model)
        #results.write()
        #if results.solver.status == 'ok':
        #    model.pprint()
        df = pd.DataFrame(index=pd.MultiIndex.from_tuples(model.x, names=self.name_idx))
        df['x'] = [pe.value(model.x[key]) for key in df.index]
        df[self.name_param] = [model.c[key] for key in df.index]
        self.model = df
        #print(df)
        #print((df['c'] * df['x']).groupby('w').sum().to_frame())
        #rint(df['x'].groupby('t').sum().to_frame().T)
        

    def proccess_string(self, formula):
        formula.replace(' ', '')
        pos_not_letter = [i for i, symbol in enumerate(formula) if not symbol.isalpha()]
        strip_symbol = [idx+1 for idx in pos_not_letter if idx < len(formula)-1]
        idx = sorted(pos_not_letter + strip_symbol)
        tmp = [0] + idx + [len(formula)]
        return [formula[tmp[i]:tmp[i+1]] for i in range(len(tmp) - 1)]