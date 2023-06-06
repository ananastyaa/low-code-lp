import pyomo.environ as pe
import pyomo.opt as po
import pandas as pd
from indexes import Indexes
from parameter import Parameter


class Model:
    def __init__(self, data, name_indexes, name_parameters):
        self.data = data
        self.name_idx = name_indexes
        self.name_param = name_parameters
        self.indexes = []
        self.params = []

    def create(self):
        self.indexes = self.create_indexes()
        self.params = self.create_parameters()
        self.create_model()

    def create_indexes(self):
        return [Indexes(self.data, col).index() for col in self.name_idx]

    def create_parameters(self):
        return Parameter(self.name_idx, self.name_param, self.data).create()

    def create_model(self):
        model = pe.ConcreteModel()

        _ = [setattr(model, param, pe.Set(initialize=self.indexes[i]))
             for i, param in enumerate(self.name_idx)]

        # model.c[w, t] - время
        model.c = pe.Param(*[model.__getattribute__(name) for name in self.name_idx], initialize=self.params)
        # model.c[w, t] - пара индексов
        model.x = pe.Var(*[model.__getattribute__(name) for name in self.name_idx], domain=pe.Reals, bounds=(0, 1))

        # допустим, введена формула вида СУММА(param*idx)
        pairs = list(product(*self.indexes))
        expr = sum(model.c[p] * model.x[p] for p in pairs)
        model.objective = pe.Objective(sense=pe.minimize, expr=expr)
 
        # ограничения я не придумала пока че с ними сделать
        model.tasks_done = pe.ConstraintList()
        for t in model.tasks:
            lhs = sum(model.x[w, t] for w in model.workers)
            rhs = 1
            model.tasks_done.add(lhs == rhs)

        model.hour_limit = pe.ConstraintList()
        for w in model.workers:
            lhs = sum(model.c[w, t] * model.x[w, t] for t in model.tasks)
            rhs = model.max_hours
            model.hour_limit.add(lhs <= rhs)

        solver = po.SolverFactory('gurobi')
        results = solver.solve(model, tee=True)
        df = pd.DataFrame(index=pd.MultiIndex.from_tuples(model.x, names=['w', 't']))
        df['x'] = [pe.value(model.x[key]) for key in df.index]
        df['c'] = [model.c[key] for key in df.index]
        #print(df)
        #print((df['c'] * df['x']).groupby('w').sum().to_frame())
        #print(df['x'].groupby('t').sum().to_frame().T)
        return ((df['c'] * df['x']).groupby('w').sum().to_frame())
