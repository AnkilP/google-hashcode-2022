import sys
from ortools.linear_solver import pywraplp

class Contributor:
    def __init__(self, name):
        self.name = name
        self.skill = {}
        self.busy = False
    
    def add_skill(self, skill_name, level):
        self.skill[skill_name] = level

    def busy(self, busy):
        selfbusy = busy

class Project:
    def __init__(self, name):
        self.name = name
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def add_info(self, days, score, best_before, number_of_roles):
        self.days = days
        self.score = score
        self.best_before = best_before
        self.number_of_roles = number_of_roles

class Task:
    def __init__(self):
        self.name = name
        self.skill = ""
        self.level = 0
        self.done = False
    
    def add_info(self, days, score, best_before, number_of_roles):
        self.days = days
        self.score = score
        self.best_before = best_before
        self.number_of_roles = number_of_roles

    def add_role(self, skill, level):
        self.skill = skill
        self.level = level
    
    def done(self):
        self.done = True

def solve(contributors, tasks, day):
    # Data
    num_workers = len(contributors)
    num_tasks = len(tasks)

    # Solver
    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Variables
    # x[i, j] is an array of 0-1 variables, which will be 1
    # if worker i is assigned to task j.
    x = {}
    for worker in range(num_workers):
        for task in range(num_tasks):
            x[worker, task] = solver.BoolVar(f'x[{worker},{task}]')

    # # Constraints
    # # The total size of the tasks each worker takes on is at most total_size_max.
    # for worker in range(num_workers):
    #     solver.Add(
    #         solver.Sum([
    #             task_sizes[task] * x[worker, task] for task in range(num_tasks)
    #         ]) <= total_size_max)

    # Each task is assigned to at most one worker.
    for task in range(num_tasks):
        solver.Add(
            solver.Sum([x[worker, task] for worker in range(num_workers)]) <= 1)

    # contribtor skill >= task skill
    for task in range(num_tasks):
        skill = tasks[task].skill
        solver.Add(x[worker, task]*)

    # Objective
    objective_terms = []
    for worker in range(num_workers):
        for task in range(len(projects)):
            latedays = max(0, day - projects[task].best_before)
            objective_terms.append(projects[task].score - latedays * x[worker, task])
    solver.Maximize(solver.Sum(objective_terms))

    # Solve
    status = solver.Solve()

    solution = []
    # Print solution.
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print(f'Total cost = {solver.Objective().Value()}\n')
        for worker in range(num_workers):
            for task in range(num_tasks):
                if x[worker, task].solution_value() > 0.5:
                    solution.append((contributors[worker], tasks[task]))
    else:
        print('No solution found.')
    
if __name__ == "__main__":
    filename = 'a_an_example.in.txt'
    fp = 'input_data/'
    data = []
    with open(fp + filename, 'r') as f:
        data = f.read().split('\n')
    input = iter(data)
    n_contributors, n_projects = map(int, next(input).split())
    conts = {}
    projects = {}
    experts = {}
    tasks = []
    lastday = 0
    for cont in range(n_contributors):
        inp = next(input).split()
        name = inp[0]
        skills = int(inp[1])
        conts[cont] = Contributor(name)
        for skill in range(skills):
            inp = next(input).split()
            skill_name = inp[0]
            level = int(inp[1])
            conts[cont].add_skill(skill_name, level)
            if skill_name in experts:
                experts[skill_name].append(conts[cont])
            else:
                experts[skill_name] = []
                experts[skill_name].append(conts[cont])

    for s, x in experts.items():
        x.sort(key=lambda x: x.skill[s], reverse=True)

    for project in range(n_projects):
        inp = next(input).split()
        name = inp[0]
        projects[project] = Project(name)
        days, score, bb, num_roles = map(int, inp[1:])
        projects[project].add_info(days, score, bb, num_roles)
        lastday = max(lastday, days + bb)
        for role in range(num_roles):
            inp = next(input).split()
            x_k = inp[0]
            l_k = int(inp[1])
            t = Task()
            t.add_info(days, score, bb, num_roles)
            t.add_role(x_k, l_k)
            tasks.append(t)
            projects[project].add_task(t)
    
    pp = []
    for xx, xy in projects.items():
        pp.append(xy)

    pp.sort(key=lambda x: x.best_before)

    day = 0
    output = []
    while day <= lastday:
        proj = pp[0]
        for t in proj.tasks:
            
        day += 1
