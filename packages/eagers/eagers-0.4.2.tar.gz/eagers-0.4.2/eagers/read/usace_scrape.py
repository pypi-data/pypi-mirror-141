'''
 https://www.nwd.usace.army.mil/CRWM/
https://www.nwd.usace.army.mil/CRWM/Water-Control-Data/   list of dams they might have data for
https://www.nwd.usace.army.mil/CRWM/Water-Control-Data/Project-Data/

process:
go to dataquery site:  https://www.nwd-wc.usace.army.mil/dd/common/dataquery/www/
need to search for installation by name, then can view what data is available at that installation

'''

import urllib.request
import shutil
import time
from datetime import datetime

from eagers.config.path_spec import USER_DIR_DATA_RETRIEVAL
def usace_scrape():
    save_dir = USER_DIR_DATA_RETRIEVAL
    start_date = datetime(2016, 10, 1)
    end_date = datetime(2020, 9, 30)
    flow_unit = '%3Aunits%3Dkcfs'
    power_unit = '%3Aunits%3DMW'
    height_unit = '%3Aunits%3Dft'
    stor_unit = '%3Aunits%3Dkaf'
    sites = {}

    
    sites['names'] = ['albeni_falls','bonnevile', 'chief_joseph','dalles', 
                     'dworshak', 'grand_coulee', 'ice_harbor', 'john_day', 
                     'libby', 'little_goose', 'lower_granite', 'lower_monumental', 
                     'mcnary', 'priest_rapids', 'rock_island', 'rocky_reach', 'wanapum', 'wells']
    sites['abbrev'] = ['ALF', 'BON', 'CHJ','TDA', 'DWR', 'GCL',  'IHR', 'JDA', 
                       'LIB', 'LGS', 'LWG', 'LMN', 'MCN', 'PRD', 'RIS', 'RRH', 'WAN', 'WEL']
    param = ['.Power.Total.1Hour.1Hour.CBT-RAW',
             '.Flow-Gen.Ave.1Hour.1Hour.CBT-REV',
             '.Flow-Spill.Ave.1Hour.1Hour.CBT-REV',
             '.Elev-Forebay.Inst.1Hour.0.CBT-REV',
             '.Elev-Tailwater.Inst.1Hour.0.CBT-REV',
             '.Flow-In.Ave.~1Day.1Day.CBT-REV',
             '.Flow-Out.Ave.1Hour.1Hour.CBT-REV',
             '.Stor.Inst.1Hour.0.CBT-REV']
    units = [ power_unit + '%7C', flow_unit + '%7C', flow_unit + '%7C', height_unit + '%7C', height_unit + '%7C', flow_unit + '%7C', flow_unit + '%7C', stor_unit]
    html_list,file_list = build_lists(sites,param,units,save_dir,start_date,end_date)
    query_web(html_list,file_list)#query website

    # Additional data from USACE

    sites['names'] = ['hungry_horse']
    sites['abbrev'] = ['HGH']
    param = ['.Power.Total.1Hour.1Hour.CBT-REV', # REV instead of RAW like others
             '.Flow-Gen.Ave.1Hour.1Hour.CBT-REV',
             '.Flow-Spill.Ave.1Hour.1Hour.CBT-REV',
             '.Elev-Forebay.Inst.1Hour.0.CBT-REV',
             '.Elev-Tailwater.Inst.1Hour.0.CBT-REV',
             '.Flow-In.Ave.~1Day.1Day.CBT-REV',
             '.Flow-Out.Ave.1Hour.1Hour.CBT-REV',
             '.Stor.Inst.1Hour.0.CBT-REV']
    units = [ power_unit + '%7C', flow_unit + '%7C', flow_unit + '%7C', height_unit + '%7C', height_unit + '%7C', flow_unit + '%7C', flow_unit + '%7C', stor_unit]
    html_list,file_list = build_lists(sites,param,units,save_dir,start_date,end_date)
    query_web(html_list,file_list)#query website


    sites['names'] = ['cabinet_gorge']
    sites['abbrev'] = ['CAB']
    param = ['.Elev-Forebay.Inst.1Hour.0.CBT-REV',
             '.Elev-Tailwater.Inst.1Hour.0.CBT-RAW',
             '.Flow-In.Ave.1Hour.0.CENWS-COMPUTED-RAW',
             '.Flow-Out.Ave.1Hour.1Hour.CBT-REV',
             '.Stor.Inst.1Hour.0.CBT-REV']
    units = [height_unit + '%7C', height_unit + '%7C', flow_unit + '%7C', flow_unit + '%7C', stor_unit]
    html_list,file_list = build_lists(sites,param,units,save_dir,start_date,end_date)
    query_web(html_list,file_list)#query website



    sites['names'] = ['hells_canyon']
    sites['abbrev'] = ['HCD']
    param = ['Flow-In.Ave.~1Day.1Day.IDP-COMPUTED-REV','Flow-Out.Ave.~1Day.1Day.IDP-REV']
    units = [flow_unit + '%7C', flow_unit]
    html_list,file_list = build_lists(sites,param,units,save_dir,start_date,end_date)
    query_web(html_list,file_list)#query website

    sites['names'] = ['noxon']
    sites['abbrev'] = ['NOX']
    param = ['.Elev-Forebay.Inst.1Hour.0.CBT-REV',
             '.Elev-Tailwater.Inst.1Hour.0.CBT-RAW',
             '.Flow-Out.Ave.1Hour.1Hour.CBT-REV',
             '.Stor.Inst.1Hour.0.CBT-REV']
    units = [height_unit + '%7C', height_unit + '%7C', flow_unit + '%7C', stor_unit]
    html_list,file_list = build_lists(sites,param,units,save_dir,start_date,end_date)
    query_web(html_list,file_list)#query website

    sites['names'] = ['brownlee']
    sites['abbrev'] = ['BRN']
    param = ['.Elev-Forebay.Inst.~1Day.0.IDP-REV',
             '.Flow-In.Inst.~1Day.0.IDP-REV',
             '.Flow-Out.Inst.~1Day.0.IDP-COMPUTED-REV',
             '.Stor-Total.Inst.~1Day.0.IDP-COMPUTED-REV']
    units = [height_unit + '%7C', flow_unit + '%7C', flow_unit + '%7C', stor_unit]
    html_list,file_list = build_lists(sites,param,units,save_dir,start_date,end_date)
    query_web(html_list,file_list)#query website

    
    #Box Canyon: BOX.Elev-Forebay.Ave.~1Day.1Day.CBT-REV
    # BOX.Flow-Out.Ave.~1Day.1Day.CBT-REV

    #Columbia river at boundary (downstream of waneta, Keenleyside Dam and brilliant dam): CIBW.Flow.Inst.15Minutes.0.GOES-REV

    #Owyhee: OWY.Elev-Forebay.Inst.~1Day.0.USBR-COMPUTED-REV   OWY.Stor-Total.Inst.0.0.USBR-COMPUTED-REV

    #upstream of brownlee WEII.Flow.Ave.~1Day.1Day.GOES-COMPUTED-REV
    # Flow upstream of American Falls on Snake: BFTI.Flow.Inst.0.0.USBR-RAW
    # a bit more upstream SHYI.Flow.Ave.~1Day.1Day.USBR-RAW
    # further upstream than henry's fork, LORI.Flow.Ave.~1Day.1Day.USBR-RAW
    # Even further upstream  HEII.Flow.Ave.~1Day.1Day.USBR-RAW
    # further upstream but before pallisades reservoir PALI.Flow.Ave.~1Day.1Day.USBR-RAW
    #Flow out of hells canyon dam: HCDI.Flow.Inst.15Minutes.0.USGS-REV
    #Flow downstream of hells canyon (Oregon WA border, after salmon river enters): CHGI.Flow.Ave.~1Day.1Day.USGS-COMPUTED-REV

    #storage reservoir (Owyhee only has daily forebay height(.Elev-Forebay.Inst.~1Day.0.USBR-COMPUTED-REV))

    '''Idaho Power data'''
    'https://idastream.idahopower.com/Data/List/Parameter/Flow/Statistic/LATEST%20Flow/Interval/Latest'
    'https://www.idahopower.com/community-recreation/recreation/water-information/stream-flow-data/'

    ''' BC Hydro'''
    'https://wateroffice.ec.gc.ca/google_map/google_map_e.html?map_type=historical&search_type=region&region=PYR'

def query_web(html_list,file_list):
    for i in range(len(html_list)):
        # Download the file from `url` and save it locally under `file_name`:
        with urllib.request.urlopen(html_list[i],timeout=60) as response, open(file_list[i], 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        time.sleep(1)

def build_lists(sites,param,units,save_dir,d1,d2):
    #build list of URL's and file names
    # Note that electric data only available older than 6 days
    base = 'https://www.nwd-wc.usace.army.mil/dd/common/web_service/webexec/ecsv?id='
    d_now = datetime.now()
    days = (d_now - d1).days
    if d_now.minute>30:
        tod = 'd' + str(d_now.hour) + 'h' + str(d_now.minute-30) + 'm'
    else:
        tod = 'd' + str(d_now.hour-1) + 'h' + str(d_now.minute+30) + 'm'
    weeks = int(days/7)
    days -= 7*weeks
    lookback = '&headers=true&filename=&timezone=PST&lookback=' + str(weeks) + 'w' + str(days) + tod
    days = (d_now - d2).days
    weeks = int(days/7)
    days -= 7*weeks
    lookforward = '&lookforward=' + '-' + str(weeks) + 'w' + str(days) + tod
    m = d1.month
    if m<10:
        m = '0' + str(m)
    else:
        m = str(m)
    day = d1.day
    if day<10:
        day = '0' + str(day)
    else:
        day = str(day)
    start_date = '&startdate=' + m + '%2F' + day + '%2F' + str(d1.year) + '+07%3A00'
    m = d2.month
    if m<10:
        m = '0' + str(m)
    else:
        m = str(m)
    day = d2.day
    if day<10:
        day = '0' + str(day)
    else:
        day = str(day)
    end_date = '&enddate=' + m + '%2F' + day + '%2F' + str(d2.year) + '+07%3A00'
    html_list = []
    file_list = []    
    for k in range(len(sites['names'])):
        code = sites['abbrev'][k]
        tags = ''
        for j in range(len(param)):
            tags = tags + code + param[j] + units[j]
        url = base + tags + lookback + lookforward + start_date + end_date
        f_name = save_dir / (sites['names'][k]  + '.txt')
        html_list.append(url)
        file_list.append(f_name)
    return html_list, file_list