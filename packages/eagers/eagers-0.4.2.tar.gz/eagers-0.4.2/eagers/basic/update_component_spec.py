import numpy as np

from eagers.basic.ss_response import ss_response

def update_component_spec(gen, param, value):
    """Update component specification."""
    ub = gen['size_kw']
    if 'type' in gen:
        gt = gen['type']
    elif '_type' in gen:
        gt = gen['_type']
    if gt in ['Electrolyzer']:
        lb = gen['startup']['hydrogen'][-1]
    elif gt in ['CombinedHeatPower','ElectricGenerator','HydrogenGenerator','ElecGeneratorAC', 'ElecGeneratorDC','CombHeatPowerAC', 'CombHeatPowerDC']:
        if 'electricity' in gen['output']:
            lb = gen['startup']['electricity'][-1]
        elif 'direct_current' in gen['output']:
            lb = gen['startup']['direct_current'][-1]
    elif gt in ['Heater']:
        lb = gen['startup']['heat'][-1]
    elif gt in ['Chiller']:
        lb = gen['startup']['cooling'][-1]
    elif gt in ['CoolingTower']:
        lb = gen['startup']['heat_reject'][-1]
    ramp_rate = gen['ramp_rate']
    p,_ = np.linalg.eig(gen['state_space']['a'])
    w_0 = float(np.sqrt(np.real(p[0])**2 + np.imag(p[0])**2))
    zeta = float(-np.real(p[0]+p[1])/(2*w_0)) # critical damping coefficient
    if param == 'ub':
        ub = value
    elif param == 'lb':
        lb = value
    elif param == 'ramp_rate':
        ramp_rate = value
    elif param == 'output':
        gen['output'] = value
    elif param == 'w_0':
        w_0 = value
    elif param == 'zeta':
        zeta = value
    scale = ub / gen['size_kw']
    lb *= scale
    ramp_rate *= scale
    t_peak = (ub - lb) / ramp_rate * 3600
    if param == 'w_0':
        new_ramp_rate = ss_response(gen)
    elif abs(zeta-1)<1e-3:
            w_0 = 1.5895 * np.pi / t_peak
            gen['state_space']['a'] = [[0, 1], [-(w_0**2), -2*zeta*w_0]]
            gen['state_space']['b'] = [[0], [w_0**2]]
            gen['state_space']['c'] = [1, 0]
            gen['state_space']['d'] = [0]
            new_ramp_rate = ss_response(gen)
    else:
        # find natural frequency which achieves desired ramp_rate
        error = 1
        last_error = 1
        while abs(error) > 1e-5:
            gen['state_space']['a'] = [[0, 1],[-(w_0**2), -2*zeta*w_0]]
            gen['state_space']['b'] = [[0],[w_0**2]]
            gen['state_space']['c'] = [1, 0]
            gen['state_space']['d'] = [0]
            new_ramp_rate = ss_response(gen)
            error = max(-0.5, (ramp_rate - new_ramp_rate) / ramp_rate)
            if (error>0 and last_error<0)  or (error<0 and last_error>0):
                w_0 *= 1 + 0.5 * error
            else:
                w_0 *= 1 + error
            last_error = error
    gen['ramp_rate'] = new_ramp_rate
    if 'start_cost' in gen:
        gen['start_cost'] *= scale
    gen['size_kw'] = ub
    if param == 'lb':
        gen['startup'] = []
        gen['shutdown'] = []
        gen['startup']['time'] = [0, 1e3]
        gen['shutdown']['time'] = [0, 1e3]
        if gt in ['CombinedHeatPower','CombHeatPowerAC', 'CombHeatPowerDC']:
            gen['startup']['electricity'] = [0, lb]
            gen['shutdown']['electricity'] = [lb, 0]
            if 'electricity' in gen['output']:
                eff = eff_interp(gen['output']['capacity'], gen['output']['electricity'],lb/ub)
            elif 'direct_current' in gen['output']:
                eff = eff_interp(gen['output']['capacity'], gen['output']['direct_current'],lb/ub)
            hlb = lb * eff_interp(gen['output']['capacity'], gen['output']['heat'],lb/ub) / eff
            gen['startup']['heat'] = [0, hlb]
            gen['shutdown']['heat'] = [hlb, 0]
        elif gt in ['ElectricGenerator','ElecGeneratorAC', 'ElecGeneratorDC',]:
            gen['startup']['electricity'] = [0, lb]
            gen['shutdown']['electricity'] = [lb, 0]
        elif gt in ['Heater']:
            gen['startup']['heat'] = [0, lb]
            gen['shutdown']['heat'] = [lb, 0]
        elif gt in ['Chiller']:
            gen['startup']['cool'] = [0, lb]
            gen['shutdown']['cool'] = [lb, 0]
        else:
            outs = list(gen['output'].keys())
            outs.pop('capacity')
            gen['startup'][outs[0]] = [0, lb]
            gen['shutdown'][outs[0]] = [lb, 0]
    if not '_input' in gen['shutdown']:
        if lb == 0:
            gen_input = 0
        else:
            if gt in ['CombinedHeatPower','CombHeatPowerAC', 'CombHeatPowerDC','ElectricGenerator','ElecGeneratorAC', 'ElecGeneratorDC']:
                if 'electricity' in gen['output']:
                    gen_input = lb / eff_interp(gen['output']['capacity'], gen['output']['electricity'],lb/ub)
                elif 'direct_current' in gen['output']:
                    gen_input = lb / eff_interp(gen['output']['capacity'], gen['output']['direct_current'],lb/ub)
            elif gt in ['Heater']:
                gen_input = lb / eff_interp(gen['output']['capacity'], gen['output']['heat'],lb/ub)
            elif gt in ['Chiller']:
                gen_input = lb / eff_interp(gen['output']['capacity'], gen['output']['cooling'],lb/ub)
            else:
                outs = list(gen['output'].keys())
                outs.remove('capacity')
                gen_input = lb / eff_interp(gen['output']['capacity'], gen['output'][outs[0]],lb/ub)
        gen['startup']['input_'] = [0, gen_input]
        gen['shutdown']['input_'] = [gen_input, 0]
    if gt in ['CombinedHeatPower','CombHeatPowerAC', 'CombHeatPowerDC']:
        heat = gen_input * eff_interp(gen['output']['capacity'], gen['output']['heat'],lb/ub)
        gen['startup']['heat'] = [0, heat]
        gen['shutdown']['heat'] = [heat, 0]
    return gen

def eff_interp(cap,eff,x):
    i = 1
    while i<len(cap)-1 and x>cap[i]:
        i+=1
    r = (x-cap[i-1])/(cap[i]-cap[i-1])
    eff_t = (1-r)*eff[i-1] + r*eff[i]
    return eff_t 