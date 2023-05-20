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
        result = self.create_model()
        return result

    def create_indexes(self):
        return [Indexes(self.data, col).index() for col in self.name_idx]

    def create_parameters(self):
        return Parameter(self.name_idx, self.name_param, self.data).create()

    def create_model(self):
        model = pe.ConcreteModel()
        _ = [setattr(model, param, pe.Set(initialize=self.indexes[i]))
             for i, param in enumerate(self.name_idx)]
        idxs = ['model.' + str(name) for name in self.name_idx]
        model.max_hours = pe.Param(initialize=40)
        model.c = pe.Param(model.workers, model.tasks, initialize=self.params, default=1000)
        model.x = pe.Var(model.workers, model.tasks, domain=pe.Reals, bounds=(0, 1))

        expr = sum(model.c[w, t] * model.x[w, t]
                   for w in model.workers for t in model.tasks)
        model.objective = pe.Objective(sense=pe.minimize, expr=expr)

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
