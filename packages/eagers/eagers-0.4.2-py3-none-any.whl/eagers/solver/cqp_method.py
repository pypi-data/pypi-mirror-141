"""Complimentary Quadratic Programming method (not mcQP method).

Functions:
cqp_method
"""

from eagers.solver.ecos_qp import ecos_qp
from eagers.solver.sort_solution import sort_solution, sort_eh
from eagers.update.disable_gen import disable_gen


def cqp_method(names, gen, qp, first_disp, date):
    """Positional arguments:
    gen - (list of dict) Generator dictionary reperesentations.
    qp - (dict)
    first_disp - (2D list) First dispatch.
    date - (list of datetime)
    """
    n_s = len(date) - 1
    n_g = len(gen)
    locked = [[True for t in range(n_s+1)] for i in range(n_g)]
    for i in range(n_g):
        if not gen[i]['enabled']:
            locked[i] = [False for t in range(n_s+1)]
    lower_bound = [0 for i in range(n_g)]
    upper_bound = [0 for i in range(n_g)]
    dx = [[0 for t in range(n_s)] for i in range(n_g)]
    dt_seconds = [(date[t+1] - date[t]).total_seconds() for t in range(n_s)]
    dt = [dt_seconds[t]/3600 for t in range(n_s)]
    for i in range(n_g):
        if qp['organize']['dispatchable'][i]:
            states = gen[i]['states'][-1]
            for j in range(len(states)):
                lower_bound[i] += gen[i][states[j]]['lb'][-1]
                upper_bound[i] += gen[i][states[j]]['ub'][-1]
            # Default to off when initial dispatch is below lb.
            for t in range(n_s):
                if first_disp[i][t+1]<lower_bound[i]:
                    locked[i][t] = False
        if 'ramp' in gen[i]:
            dx[i] = [dt[t]*gen[i]['ramp'] for t in range(n_s)]
    # Make sure it can shut down in time from initial condition.
    for i in range(n_g):
        if qp['organize']['dispatchable'][i]:
            if first_disp[i][0] > 0 and not all(locked[i]):
                d = first_disp[i][0]
                t = 0
                while d > 0:
                    r = qp['organize']['ramp_down'][t]
                    d -= qp['b'][r]
                    if d > 0 and not locked[i][t]:
                        locked[i][t] = True
                    t += 1

    feasible = 1
    attempt = 0
    lb_relax = 1

    # attempt: Integer value describing the number of attempts before
    # reaching feasibility. This determines how close components must be to
    # their lower bound from below to be considered online.
    # 
    # n: Represents the percent of lower bounds on your first try. Just use
    # the locked matrix given, then do unit commitment based on
    # optimal_state > lb * perc_lb
    perc_lb = [0.9, 0.75, 0.5, 0.2, 0.1, 0, -1]
    while feasible != 0 and attempt < len(perc_lb):
        if attempt > 0:
            # Not the first try. Lower limit for online threshold.
            lb_relax = perc_lb[attempt-1]
            # Only change label for unit commitment gens, and don't change the
            # label for initial conditions.
            for i in range(n_g):
                if qp['organize']['dispatchable'][i]:
                    # Default to on unless offline in initial dispatch.
                    locked[i] = [True if first_disp[i][t] > (lower_bound[i] * lb_relax) else False for t in range(len(first_disp[i]))]
        disable_gen(qp, locked)
        x, feasible = ecos_qp(qp['h'], qp['f'], qp['a'], qp['b'], qp['a_eq'], qp['b_eq'], qp['ub'], qp['lb'], qp['x_keep'], qp['r_keep'], qp['req_keep'])
        attempt += 1


    if feasible == 0:
        v_h = [[True if j<1 else False for j in s_eh] for s_eh in sort_eh(x, qp)] #do you value heat generation, or is there tons of extra
        solution = sort_solution(x, qp, names, gen, date, v_h)
    solution['lb_relax'] = [lb_relax]
    
    return solution