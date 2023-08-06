'''Defines functionality for calculating generator limits.

Functions:
gen_limit
chp_heat
determine_locked
'''


from sqlalchemy import Constraint


def gen_limit(gen, gen_output, binary, dt, s):
    '''Return the generator limit.'''
    n_g = len(gen)
    n_s = len(dt)
    ramp_up, ramp_down, upper_bound, lower_bound = ramp_rates(gen,binary,dt)
    constraint = [[None for t in range(n_s)] for i in range(n_g)]
    acdc = find_acdc(gen)
    if len(s) == 1 and (s[0] == 'e' or s[0] == 'dc') and any([g['type']== 'CombinedHeatPower' for g in gen]):
        # For combined heat and power cases.
        s.append('h')
    if not acdc is None and not 'dc' in s:
        s.append('dc')
    if not acdc is None and not 'e' in s:
        s.append('e')
    if 'h' in s:
        elec = False
        direct = False
        for i in range(n_g):
            if gen[i]['type'] == 'CombinedHeatPower':
                if 'e' in gen[i]['output']:
                    elec = True
                if 'dc' in gen[i]['output']:
                    direct = True
        if not 'e' in s and elec:
            s.append('e')
        if not 'dc' in s and direct:
            s.append('dc')

    spare_gen = {}
    max_out = {}
    min_out = {}
    heat_output = [[] for i in range(n_g)]
    spare_capacity = {}
    for net_abbrev in s:
        inverter_eff, inverter_capacity = check_acdc(gen,net_abbrev)
        utility_spare_capacity = [0 for i in range(n_s)]
        spare_gen[net_abbrev] = [0 for i in range(n_s)]
        max_out[net_abbrev] = [[0 for t in range(n_s + 1)] for i in range(n_g)]
        min_out[net_abbrev] = [[0 for t in range(n_s + 1)] for i in range(n_g)]
        for i in range(n_g):
            if generation_equip_on_net(gen[i],net_abbrev):
                min_out[net_abbrev][i], max_out[net_abbrev][i], constraint[i] = constrained_min_max_out(gen_output[i],binary[i],ramp_up[i],ramp_down[i],upper_bound[i],lower_bound[i])
                
                # Convert GenOutput to heatOutput.
                if net_abbrev == 'h' and gen[i]['type'] == 'CombinedHeatPower':
                    heat_output[i] = chp_heat(gen[i], gen_output[i])
                    if 'e' in gen[i]['output']:
                        max_out['h'][i] = chp_heat(gen[i], max_out[net_abbrev][i])
                    else:
                        max_out['h'][i] = chp_heat(gen[i], max_out[net_abbrev][i])
                    spare_gen[net_abbrev] = [spare_gen[net_abbrev][t] + (max_out[net_abbrev][i][t + 1] - heat_output[i][t + 1]) for t in range(n_s)]
                else:
                    spare_gen[net_abbrev] = [spare_gen[net_abbrev][t] + (max_out[net_abbrev][i][t + 1] - gen_output[i][t + 1]) for t in range(n_s)]

                # Assume net heat production remains the same, so do not count spare absorption chiller capacity.
                if gen[i]['type'] == 'Chiller' and gen[i]['source'] == 'heat':
                    max_out[net_abbrev][i] = gen_output[i]

            
            if not inverter_eff[i] is None:
                min_pre_inversion, max_pre_inversion, constraint[i] = constrained_min_max_out(gen_output[i],binary[i],ramp_up[i],ramp_down[i],upper_bound[i],lower_bound[i])
                max_out[net_abbrev][i] = [min(z * inverter_eff[i], inverter_capacity[i]) for z in max_pre_inversion]
                min_out[net_abbrev][i] = [min(z * inverter_eff[i], inverter_capacity[i]) for z in min_pre_inversion]
                spare_gen[net_abbrev] = [spare_gen[net_abbrev][t] + (max_pre_inversion[t + 1] - gen_output[i][t + 1]) * inverter_eff[i] for t in range(n_s)]

            if gen[i]['type'] == 'Utility' and net_abbrev in gen[i]['output']:
                max_out[net_abbrev][i] = ([gen[i]['x']['ub'] for j in range(n_s+1)])
                min_out[net_abbrev][i] = ([gen[i]['x']['lb'] for j in range(n_s+1)])
                if 'y' in gen[i]: #sellback
                    min_out[net_abbrev][i] = ([z - gen[i]['y']['ub'] for z in min_out[net_abbrev][i]])
                utility_spare_capacity = [utility_spare_capacity[t] + (gen[i]['x']['ub'] - gen_output[i][t + 1]) for t in range(n_s)]
            #TODO add Market capcity

        spare_capacity[net_abbrev] = [spare_gen[net_abbrev][t] + utility_spare_capacity[t] for t in range(n_s)]
    return min_out, max_out, constraint, spare_capacity, spare_gen


def chp_heat(gen, output):
    n_s = len(output)
    # Assuming all outputs are nx1.
    heat_out = [
        -gen['const_demand']['district_heat'] * int(output[t] > 0)
        for t in range(n_s)
    ]
    states = gen['states'][-1]
    for t in range(n_s):
        net_out = 0
        j = 0
        # Use < instead of <= because index is 1 less than number of
        # states.
        while (j < len(states) and net_out < output[t]):
            seg = min([output[t] - net_out, gen[states[j]]['ub'][1]])
            net_out += seg
            heat_out[t] += seg * gen['output']['h'][-1][j]
            j += 1

    return heat_out

def determine_locked(gen,dispatch):
    n_s = len(dispatch[0])-1
    n_g = len(gen)
    include = ['ElectricGenerator','CombinedHeatPower','Heater','Electrolyzer','HydrogenGenerator','CoolingTower','Chiller']
    locked = [[True for j in range(n_s+1)] for i in range(n_g)]
    for i in range(n_g):
        if gen[i]['type'] in include:
            locked[i] = [dispatch[i][t]>0 for t in range(n_s+1)]
    return locked

def ramp_rates(gen,binary,dt):
    n_g = len(gen)
    n_s = len(dt)
    ramp_up = [[] for i in range(n_g)]
    ramp_down = [[] for i in range(n_g)]
    upper_bound = [0 for i in range(n_g)]
    lower_bound = [0 for i in range(n_g)]
    for i in range(n_g):
        if 'ramp' in gen[i] and not 'stor' in gen[i]:
            ramp_up[i] = [gen[i]['ramp']['b'][0] * dt[t] for t in range(n_s)]
            ramp_down[i] = [gen[i]['ramp']['b'][1] * dt[t] for t in range(n_s)]
            starts = [t for t in range(n_s) if binary[i][t + 1] and not binary[i][t]]
            stops = [t for t in range(n_s) if not binary[i][t + 1] and binary[i][t]]
            lower_bound[i] = gen[i][gen[i]['states'][0][0]]['lb'][-1]
            for st in starts:
                # If the ramp rate is less than the lb, increase ramp
                # rate at moment of startup.
                ramp_up[i][st] = max(ramp_up[i][st], lower_bound[i])
            for st in stops:
                # If the ramp rate is less than the lb, increase ramp
                # rate at moment of shutdown.
                ramp_down[i][st] = max(ramp_down[i][st], lower_bound[i])
            upper_bound[i] = gen[i]['ub']
    return ramp_up, ramp_down, upper_bound, lower_bound

def find_acdc(gen):
    acdc = None
    for i in range(len(gen)):
        if gen[i]['type'] == 'ACDCConverter':
            if not acdc: 
                acdc = {}
                acdc['dc_to_ac_eff'] = []
                acdc['ac_to_dc_eff'] = []
                acdc['ac_node'] = []
                acdc['dc_node'] = []
                acdc['capacity'] = []
            acdc['dc_to_ac_eff'].append(abs(gen[i]['output']['e'][0][-1]))
            acdc['ac_to_dc_eff'].append(gen[i]['output']['dc'][0][0])
            acdc['ac_node'].append(gen[i]['subnet_node']['e'])
            acdc['dc_node'].append(gen[i]['subnet_node']['dc'])
            acdc['capacity'].append(gen[i]['capacity'])
    return acdc

def generation_equip_on_net(gen,net_abbrev):
    ##TODO complete water and hydrogen
    include = False
    on_net = {'e':['CombinedHeatPower', 'ElectricGenerator', 'HydrogenGenerator'],
              'dc':['CombinedHeatPower', 'ElectricGenerator', 'HydrogenGenerator'],
              'h':['CombinedHeatPower', 'Heater'],
              'c':['Chiller'],
              'cw':['CoolingTower'],
              'w':[], #['HydroStorage'],
              'hy':[],#['Electrolyzer','HydrogenGenerator']
              }
    if gen['type'] in on_net[net_abbrev] and net_abbrev in gen['output'] and gen['enabled']:
        include = True
    return include

def check_acdc(gen,net_abbrev):
    need_ac_dc = False
    inverter_eff = [None for i in range(len(gen))]
    inverter_capacity = [None for i in range(len(gen))]
    ac_dc = None
    if net_abbrev in ('e', 'dc'):
        for gen_i in gen:
            if ('e' in gen_i['output'] and net_abbrev == 'dc') or ('dc' in gen_i['output'] and net_abbrev == 'e'):
                need_ac_dc = True
                break
        ac_dc = find_acdc(gen)
        if need_ac_dc and not ac_dc is None:
            if not ac_dc is None:
                for i in range(len(gen)):
                    if gen[i]['enabled'] and gen[i]['type'] in ('CombinedHeatPower', 'ElectricGenerator', 'HydrogenGenerator'):
                        inverter_eff[i], inverter_capacity[i],_ = inf_efficiency(gen[i],ac_dc,net_abbrev)
    return inverter_eff, inverter_capacity

def inf_efficiency(gen,ac_dc,net_abbrev):
    #TODO update to find line efficiency on connected nodes
    if net_abbrev == 'e' and 'dc' in gen['output']:
        ac_dc_str = {'node':'dc_node', 'abbrev':'dc','eff': 'dc_to_ac_eff'}
    if net_abbrev == 'dc' and 'e' in gen['output']:
        ac_dc_str = {'node':'ac_node', 'abbrev':'e','eff': 'ac_to_dc_eff'}
    inverter_on_node = []
    if 'subnet_node' in gen:
        inverter_on_node = [j for j in range(len(ac_dc['capacity'])) if gen['subnet_node'][ac_dc_str['abbrev']] == ac_dc[ac_dc_str['node'][j]]]
    inverter_eff = 0
    inverter_capacity = 0
    inv_ind = 0
    for j in range(len(ac_dc['capacity'])):
        if len(inverter_on_node) == 0 or j in inverter_on_node:
            inverter_capacity += ac_dc['capacity'][j]
            if ac_dc[ac_dc_str['eff']]>inverter_eff:
                inv_ind = j
                inverter_eff = ac_dc[ac_dc_str['eff']][j]
    return inverter_eff,inverter_capacity, inv_ind

def constrained_min_max_out(gen_output,binary,ramp_up,ramp_down,upper_bound,lower_bound):
    n_s = len(ramp_up)
    constraint = [None for t in range(n_s)] 
    max_out = [0 for t in range(n_s+1)]
    min_out = [0 for t in range(n_s+1)]
    max_out[0] = gen_output[0] # Constrained by initial condition (can't do anything).
    min_out[0] = gen_output[0] # Constrained by initial condition (can't do anything).
    start = None
    for t in range(n_s):
        if binary[t + 1]:
            if not binary[t]:
                start = t  # Just turned on.
            if not start is None:
                # Last index (0->n_s-1) when gen was off where it could be turned on early if neccesary to satisfy ramping constraint.
                constraint[t] = start - 1
            if upper_bound <= max_out[t] + ramp_up[t]:
                max_out[t + 1] = upper_bound
            else:
                max_out[t + 1] = max_out[t] + ramp_up[t]
            if lower_bound >= min_out[t] - ramp_down[t]:
                min_out[t + 1] = lower_bound
            else:
                min_out[t + 1] = min_out[t] - ramp_down[t]

    for t in range(n_s - 1, 0, -1):
        if (max_out[t] - ramp_down[t]) > max_out[t+1]:
            # Constrained by shutdown.
            max_out[t] = min([upper_bound,(max_out[t + 1] + ramp_down[t])])
            if constraint[t - 1] is None:
                # First index (0-->n_s-1) where gen has shut down, where it could be left on to satisfy ramping constraint.
                constraint[t - 1] = min([z - 1 for z in range(t + 1, n_s + 1) if max_out[z] == 0])
    return min_out, max_out, constraint
    