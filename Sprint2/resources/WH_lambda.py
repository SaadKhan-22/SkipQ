#check 2
import urllib3
import datetime as dt
from cloudWatch_putMetrics import CloudWatchPutMetric
from constants import *


def lambda_handler(event, context):
    #Latency and availability metrics for web resource
    val = dict()
    
    cw = CloudWatchPutMetric()

      

    
    for url in URLS_TO_MONITOR:

        a = getAvailability(url)
        
        l = getLatency(url)
        

        dims =  {'Name': 'URL', 'Value': url} 


        responseAvb = cw.put_data(URL_MONITOR_NAMESPACE, 
            URL_MONITOR_METRIC_NAME_AVAILABILITY, 
            dims,  a)
    
        responseLat = cw.put_data(URL_MONITOR_NAMESPACE,
            URL_MONITOR_METRIC_NAME_LATENCY,
            dims, l)


        val.update({url: {'availability': a, 'latency': l}})

    return val


def getAvailability(url):
    #checks whether the resource is available(true) or not(false)
    http = urllib3.PoolManager()
    response = http.request('GET', url)

    if response.status == 200:
        return 1
    else:
        return 0


def getLatency(url):
    #returns the latency of the resource in seconds
    http = urllib3.PoolManager()

    start = dt.datetime.now()
    resp = http.request('GET', url)
    end = dt.datetime.now()

    delta = (end - start).microseconds
    latency = round(delta * 0.000001, 6)

    return latency
