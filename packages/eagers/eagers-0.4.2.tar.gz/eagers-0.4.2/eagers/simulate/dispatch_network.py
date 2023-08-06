from eagers.solver.ecos_qp import ecos_qp

def dispatch_network(subnet,production,demand,request,marginal,gen_capacity,building_capacity,constrained):
    '''Performs a quadratic optimization to find the shortage/excess of demand on the network
    and the most cost effective node to add energy production
    If constrained is true it treats any buildings as constant loads, otherwise it considers building flexibility'''
    n_b = len(request['nominal'])
    nn = len(subnet['nodes'])
    qp = build_net_optimization(subnet,production,demand,request,marginal,gen_capacity,building_capacity,constrained)
    x, feasible = ecos_qp(qp['h'], qp['f'], qp['a'], qp['b'], qp['a_eq'], qp['b_eq'], qp['ub'], qp['lb'], qp['x_keep'], qp['r_keep'], qp['req_keep'])
    
    if feasible == 0:
        thermal = [(x[j]+request['nominal'][j])*1000 for j in range(n_b)] #building thermal setpoints (amount of heating or cooling)
        node_production = [(x[j]+production[j+nn]) for j in range(-nn,0)]
        #imbalance = sum(x[-len(subnet['nodes']):]) #sum of slack nodes is the net energy imbalance on the network
    else:
        thermal = [j*1000 for j in request['nominal']] #stick with original guess from optimization (will result in imbalance somewhere)
        node_production = production
        print('Simulation error: Cannot find feasible network solution.')
    return thermal, node_production


def build_net_optimization(subnet,production,demand,request,marginal,gen_capacity,building_capacity,constrained):
    n_l = 0
    for i,s in enumerate(subnet['line']['dir']):
        if s == 'dual' and min(subnet['line']['eff'][i])<1:
            n_l +=2
        else:
            n_l +=1
    x_l = len(request['nominal']) + n_l + len(subnet['nodes']) #building thermal, line flow , and slack states
    nn = len(subnet['nodes'])
    ind = 0
    qp = {}
    qp['h'] = [0 for j in range(x_l)]
    qp['f'] = [0 for j in range(x_l)]
    qp['x_keep'] = [True for j in range(x_l)]
    qp['a'] = []
    qp['b'] = []
    qp['r_keep'] = []
    qp['a_eq'] = [[0 for j in range(x_l)] for i in range(nn)]
    qp['b_eq'] = [0 for i in range(nn)]
    qp['req_keep'] = [True for j in range(nn)]
    qp['lb'] = [0 for j in range(x_l)]
    qp['ub'] = [0 for j in range(x_l)]
    for n in range(nn):
        if 'buildings' in subnet and len(subnet['buildings'][n])>0:
            for j in subnet['buildings'][n]:
                qp['a_eq'][n][j] = -1 #building demand shows up as a load (negative on production side of equality)
                if not constrained:
                    qp['h'][j] = marginal[n]/max([1,(request['maximum'][j]-request['nominal'][j])]) #normalized so building state of 0 is equal to nominal request, penalize deviations from zero
                    qp['f'][j] = 0.5*marginal[n] #building flexibility is cheaper than generation
                    qp['lb'][j] = -request['nominal'][j]+request['minimum'][j] #normalized so building state of 0 is equal to nominal request, range is minimum to maximum, offset by the nominal request
                    qp['ub'][j] = -request['nominal'][j]+request['maximum'][j] #normalized so building state of 0 is equal to nominal request, range is minimum to maximum, offset by the nominal request
                ## add subtract flexible capacity in heating/cooling water loops
                qp['lb'][j] -= building_capacity[j][1] #how much additional cooling/heating could be extracted from the water loop capacity. If building request could be 10kW below normal, and 15kW could come from water capacity, then limit is 25kW below nominal
                qp['ub'][j] -= building_capacity[j][0] #how much additional cooling/heating could be put into the water loop capacity (negative number). If building request could be 20kW above normal, and 25kW could be put into water capacitance, then limit is 45kW above nominal
                qp['b_eq'][n] += request['nominal'][j] #normalized so building state of 0 is equal to nominal request, so generation and line transfer to node must equal this request when building flexibility is zero
                ind +=1

    
    #State equations for the energy transfer lines
    node_names = [subnet['nodes'][j][0] for j in range(nn)]
    for i in range(len(subnet['line']['dir'])):
        j = node_names.index(subnet['line']['node1'][i])
        k = node_names.index(subnet['line']['node2'][i])
        if subnet['line']['dir'][i] in ('dual','forward'):
            qp['a_eq'][j][ind] = -1 #energy leaving node 1
            qp['a_eq'][k][ind] = subnet['line']['eff'][i][0] #energy arriving at node 2
            qp['ub'][ind] = subnet['line']['limit'][i][0]
            ind += 1
        if subnet['line']['dir'][i] == 'dual' and min(subnet['line']['eff'][i])==1:
            qp['lb'][ind] = -subnet['line']['limit'][i][1]
        elif subnet['line']['dir'][i] == 'dual':
            qp['a_eq'][k][ind] = -1 #energy leaving node 2
            qp['a_eq'][j][ind] = subnet['line']['eff'][i][1] #energy arriving at node 1
            qp['ub'][ind] = subnet['line']['limit'][i][1]
            ind += 1
        elif subnet['line']['dir'] == 'reverse':
            qp['a_eq'][k][ind] = -1 #energy leaving node 2
            qp['a_eq'][j][ind] = subnet['line']['eff'][i][0] #energy arriving at node 1
            qp['ub'][ind] = subnet['line']['limit'][i][0]
            ind += 1

    # state variables for production from generators
    for n in range(nn):
        qp['a_eq'][n][ind] = 1 #variable for production at this node
        qp['b_eq'][n] -= production[n] #normalized so generation state of 0 is equal to nominal output
        if subnet['nodes'][n][0] in list(demand.keys()):
            qp['b_eq'][n] += demand[subnet['nodes'][n][0]]
        qp['f'][ind] = marginal[n]
        qp['h'][ind] = marginal[n]/max([1,(gen_capacity[n][1]-gen_capacity[n][0])]) #penalize deviations from the nominal production
        qp['lb'][ind] = gen_capacity[n][0]-production[n] #normalized so generation state of 0 is equal to nominal output
        qp['ub'][ind] = gen_capacity[n][1]-production[n] #normalized so generation state of 0 is equal to nominal output
        ind += 1
    return qp