from eagers.simulate.adjust_acdc_converter import adjust_acdc_converter
from eagers.basic.gen_limit import find_acdc, inf_efficiency
from eagers.config.network import NETWORK_NAME_ABBR_MAP

def assign_disparity(net,gen,subnet,disparity,solution,dt,t,re_opt):
    #check if there is a utility (slack bus)
    #if not check if storage has enough capacity to be slack bus
    #if it is heating and cooling, assign disparity to buildings hot/cold water loops
    #otherwise re-optimize
    i_utility, i_storage, ac_dc = identify_storage_and_utility(gen,net)
    if len(i_utility)==0 and len(i_storage)==0:
        re_opt = True
    elif len(i_storage)==0:  #no storage, grid handles error
        assign2utility(i_utility[0],gen,subnet,ac_dc,net,disparity,solution)
    else: # add up storage capacity to meet error & split proportional to available capacity            
        cap = [0 for i in range(len(i_storage))]
        for i in range(len(i_storage)):
            k = i_storage[i]
            gs = gen[k]['stor']
            if disparity>0: #extra demand, what stored charge can be called upon
                cap[i] = min(gs['peak_disch'],gs['disch_eff']*(gs['usable_size'] - solution['dispatch'][k][1])/dt)
            else: #less demand, what remaining storage capacity can be called upon
                cap[i] = -min(gs['peak_charge'],(1/gs['charge_eff'])*solution['dispatch'][k][1]/dt)
            if subnet['abbreviation'] not in gen[i]['output'] and not ac_dc is None:
                inverter_eff, inverter_capacity, inverter_index = inf_efficiency(gen[k],ac_dc,NETWORK_NAME_ABBR_MAP[net])
                cap[i] = cap[i]*inverter_eff
        if len(i_utility)==0: #no grid, all error is absorbed by storage (if possible? otherwise re-optimize)
            if abs(sum(cap))<abs(disparity): #if unable to meet error, re-optimize
                re_opt = True
            else:
                r = abs(disparity)/abs(sum(cap))
                if disparity>0: #extra demand, what stored charge can be called upon
                    power = -r*cap[i]/gs['disch_eff']
                else: #less demand, what remaining storage capacity can be called upon
                    power = r*cap[i]*gs['charge_eff']
                if subnet['abbreviation'] not in gen[i]['output'] and not ac_dc is None:
                    if net == 'electrical':
                        power = adjust_acdc_converter(gen,solution,None,power,0)
                    elif net == 'direct_current':
                        power = adjust_acdc_converter(gen,solution,power,None,0)
                solution['generator_state'][gen[k]['name']][0] += power
                n_s = len(solution['generator_state'][gen[i]['name']])
                for ti in range(t,n_s):
                    solution['dispatch'][k][ti+1] -= power*dt
                    solution['storage_state'][gen[k]['name']][ti] -= power*dt
        else: #split the error between utility and energy storage based on storage behavior
            charging = []
            discharging = []
            for k in i_storage:
                ##TODO factor in loss term
                if solution['dispatch'][k][1]>solution['dispatch'][k][0]: #charging
                    charging.append((1/gen[k]['stor']['charge_eff'])*(solution['dispatch'][k][1] - solution['dispatch'][k][0])/dt)
                    discharging.append(0)
                else:
                    charging.append(0)
                    discharging.append(gen[k]['stor']['disch_eff']*(solution['dispatch'][k][0] - solution['dispatch'][k][1])/dt)
            r = None
            if disparity>0 and sum(charging)>0: #If more demand than anticipated, reduce all storage charging, otherwise resort to grid
                r = 1 - max([0,(sum(charging)-disparity)])/sum(charging)
            elif disparity<0 and sum(discharging)>0: #if discharging and less demand than anticipated reduce discharging
                r = 1 - max([0,(sum(discharging) + disparity)])/sum(discharging)
                
            if not r is None:
                for i,k in enumerate(i_storage):
                    if disparity>0:
                        power = r*charging[i]*gen[k]['stor']['charge_eff'] # amount additional power available because charging was reduced
                        disparity -= r*sum(charging)
                    else:
                        power = -r*discharging[i]/gen[k]['stor']['disch_eff'] #amount additional power from discharging less
                        disparity += r*sum(discharging)
                    if subnet['abbreviation'] not in gen[k]['output'] and not ac_dc is None:
                        if net == 'electrical':
                            power = adjust_acdc_converter(gen,solution,None,power,0)
                        elif net == 'direct_current': #An AC battery supplying a DC bus (unlikely but here for completion)
                            power = adjust_acdc_converter(gen,solution,power,None,0)
                    solution['generator_state'][gen[k]['name']][0] += power
                    n_s = len(solution['generator_state'][gen[i]['name']])
                    for ti in range(t,n_s):
                        solution['dispatch'][k][ti+1] -= power*dt
                        solution['storage_state'][gen[k]['name']][ti] -= power*dt

            #Utility makes up the difference
            assign2utility(i_utility[0],gen,subnet,ac_dc,net,disparity,solution)
    return re_opt

def identify_storage_and_utility(gen,net):
    i_utility = []
    i_storage = []
    ac_dc = find_acdc(gen)
    for i in range(len(gen)):
        if NETWORK_NAME_ABBR_MAP[net] in gen[i]['output']:
            if gen[i]['type'] == 'Utility':
                    i_utility.append(i)
            elif gen[i]['type'] in ['ThermalStorage', 'ElectricStorage','HydroStorage','HydrogenStorage']:
                    i_storage.append(i)
        if not ac_dc is None:
            if (net == 'electrical' and 'dc' in gen[i]['output']) or (net == 'direct_current' and 'e' in gen[i]['output']):
                if gen[i]['type'] == 'ElectricStorage':
                    i_storage.append(i)
                if gen[i]['type'] == 'Utility':
                    i_utility.append(i)
    return i_utility, i_storage, ac_dc

def assign2utility(i,gen,subnet,ac_dc,net,disparity,solution):
    if subnet['abbreviation'] in gen[i]['output']:
        solution['dispatch'][i][1] += disparity
    elif not ac_dc is None:
        inverter_eff, inverter_capacity, inverter_index = inf_efficiency(gen[i],ac_dc,NETWORK_NAME_ABBR_MAP[net])
        solution['dispatch'][i][1] += disparity/inverter_eff
        if net == 'electrical':
            solution['dispatch'][inverter_index][1] -= disparity/inverter_eff
        elif net == 'direct_current':
            solution['dispatch'][inverter_index][1] += disparity/inverter_eff
    solution['generator_state'][gen[i]['name']][0] = solution['dispatch'][i][1]
    