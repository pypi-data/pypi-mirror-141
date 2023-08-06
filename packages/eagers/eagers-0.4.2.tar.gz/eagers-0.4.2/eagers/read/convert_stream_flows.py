''' this function takes stream flow measurements and produces 
net tributary additions between specified points, e.g. dams.
How it does this depends on available data
1) if outflow of upstream dam and inflow to reservoir are both available, 
the difference (accounting for run of river time) becomes the net tributary.
Reservoir losses (irrigation withdrawls and evaporation) are treated separately
2) if only outflows are known, it uses forebay height if available to estimate 
the storage flow, otherwise it is run-of river dam, the difference between 
subsequent outflows are used
** if downstream data is daily, tributary will be daily
'''

import datetime
from eagers.read.excel_interface import ProjectTemplateReader

def convert_stream_flows(dam_info_file):
    dams,data = read_hydro_data(dam_info_file)
    tributary_flows = find_tributary_equivelants(dams,data)
    write_hydro_data(dam_info_file+'_tributary',dams,tributary_flows)


def find_tributary_equivelants(dams,data):
    tributary_flows= {}
    river_speed = 2 #m/s 
    meter_per_mile = 1609.344
    d_names = list(dams.keys())
    for d in d_names:
        ud = dams[d]['upstream']
        if ud == 'Source':
            if not data[d]['inflows'] is None:
                tributary_flows[d] = data[d]['inflows']
        else:
            rivertime = (dams[ud]['river_mile']-dams[d]['river_mile'])*meter_per_mile/river_speed
            if not data[d]['inflows'] is None:          
                tributary_flows[d] = in_out_flow(data[d]['inflows'],data[ud]['outflows'],None,rivertime)
            else:
                tributary_flows[d] = out_out_flow(data[d]['outflows'],data[d]['forebay'],dams[d]['reservoir_area'],data[ud]['outflows'],rivertime)
    return tributary_flows

def in_out_flow(downstream,upstream,storage,rivertime):
    '''subtract inflow from upstream outflow'''
    trib = dict(flow=[],time=[])
    for t,dflow in enumerate(downstream):
        t2 = downstream['time'][t]-datetime.timedelta(seconds=rivertime)
        if t == 0:
            t1 = downstream['time'][t] - (downstream['time'][t+1]-downstream['time'][t])-datetime.timedelta(seconds=rivertime)
        else:
            t1 = downstream['time'][t-1] - datetime.timedelta(seconds=rivertime)
        uflow,_ = get_data_range(upstream['flow'],upstream['time'],t1,t2)
        if storage is None:
            trib['flow'].append(dflow-sum(uflow)/len(uflow))
        else:
            trib['flow'].append(dflow+storage[t]-sum(uflow)/len(uflow))
        trib['time'].append(downstream['time'][t])
    return trib

def out_out_flow(downstream,forebay,area,upstream,rivertime):
    '''subtract outflow from upstream outflow'''
    if not forebay is None:
        # account for changing forebay height
        storage = []
        for t in range(len(downstream)):
            t2 = downstream['time'][t]
            if t == 0:
                t1 = downstream['time'][t] - (downstream['time'][t+1]-downstream['time'][t])
            else:
                t1 = downstream['time'][t-1]
            height,_ = get_data_range(forebay['height'],forebay['time'],t1,t2)
            # height change in ft * area in ft^2 divided by 1000 and time in seconds to get kcfs
            storage.append([(height[-1]-height[0])*area/(1000*(t2-t1).seconds)])
    else:
        storage = None
    trib = in_out_flow(downstream,upstream,storage,rivertime)
    return trib

def get_data_range(data,time,t1,t2):
    '''get flow data in a specific time window'''
    select_data = []
    select_time = []
    i = 0
    while time[i]<t1 and i<len(time):
        i +=1
    j = i+0
    while time[j]<t2 and j<len(time):
        j+=1
    
    #first returned value is interpolation at t1
    if (time[i]-t1).seconds>60 and i>0:
        r = (time[i]-t1).seconds/(time[i]-time[i-1]).seconds
        select_data.append(r*data[i-1]+(1-r)*data[i])
        select_time.append(t1)
    #intermediate data between t1 and t2
    while i<j:
        select_data.append(data[i])
        select_time.append(time[i])
        i+=1
    #final value is interpolation at t2
    if (t2-time[j-1]).seconds>60 and j<len(time):
        r = (t2-time[j-1]).seconds/(time[j]-time[j-1]).seconds
        select_data.append(r*data[j]+(1-r)*data[j-1])
        select_time.append(t2)

def read_hydro_data(dam_info_file):
    ''' reads an excel file with reservoir information'''
    dams = ProjectTemplateReader.read_userfile(dam_info_file)
    data = {}
    for d in dams:
        data[d['name']] = read_dam_data(d['data_file'])
    return dams, data

def read_dam_data(filename):
    ''' reads a txt file with data from web'''
    #convert headers to apropriate names to aligh data sets from different sources
    pass

def write_hydro_data(file_name,dams,tributary_flow):
    pass



''' This function estimates the turbine efficiency vs head from available data'''