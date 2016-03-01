#import feedparser
from __future__ import division
import urllib
import pickle
import json
from lxml import html
import requests
import time
import math

#Time to wait between queries
wait_time = 3

#Form query - includes publisher ID
base_url = 'http://api.indeed.com/ads/apisearch?publisher=9774998588751407'
#Search for 'data scientist' in job title and exclude senior type positions
search_terms = 'title:(data scientist) -senior, -manager, -chief, -lead, -director, -principal'
#Search in SF area (note country defaults to US)
radius = 25
location = 'San+Francisco%2C+CA'
#Consider all job types (eg: FT, PT, etc...)
job_type = 'all'
#User agent (type of browser) and IP. Required
user_agent = 'Mozilla/%2F4.0%28Firefox%29'
user_ip = 'userip=1.2.3.4'
#Format (can be xml or json - defaults to xml)
form_format = 'json'
#Start result number and limit of how many to show
start_num = 0
limit_num = 25
#Version of api to use. Required
api_version = 2

#Do initial query to find total number of results
query = '&q=%s&radius=%i&l=%s&jt=%s&useragent=%s&userip=%s&format=%s&start=%i&limit=%i&v=%i' %(search_terms,radius,location,job_type,user_agent,user_ip,form_format,start_num,limit_num,api_version)
#GET response with constructed URL query
response = urllib.urlopen(base_url+query)
data = json.load(response)
total_results = data["totalResults"]
print 'TOTAL RESULTS = %i' % total_results

#Determine how many api calls needed (25 results each)
num_loops = int(math.ceil(total_results/25))

#Indeed API limits requests to 25, so loop to retrieve
feed_array = []
for i in range(0,num_loops):
    start_num = i*25
    limit_num = 25

    #Form query
    query = '&q=%s&radius=%i&l=%s&jt=%s&useragent=%s&userip=%s&format=%s&start=%i&limit=%i&v=%i' %(search_terms,radius,location,job_type,user_agent,user_ip,form_format,start_num,limit_num,api_version)

    #GET response with constructed URL query
    response = urllib.urlopen(base_url+query)
    data = json.load(response)
    #De-serialize JSON
    feed_array.append(data)


    print "Loop %i" %i
    print "Number of entries retrieved: %i" %len(data["results"])
    #Be nice and wait between queries
    print 'Sleeping for %i seconds' % wait_time
    time.sleep(wait_time)


#NEED TO CHECK JOB IDS FROM PICKLED LIST TO SEE WHETHER HAVE ALREADY GOT THESE JOBS "jobkey" of each entry.


#Scrape job info from URLs for each job ad and store data in dict
for entry in feed_array:

    for jobad in entry["results"]:

        '''
        #Get data from page
        page = requests.get(jobad["url"])
        #Load into tree
        job_info_tree = html.fromstring(page.text)
        #Extract and combine relevant fields
        job_info = job_info_tree.xpath('//span[@class="summary"]/text()') + job_info_tree.xpath('//span[@class="summary"]/ul//li/text()')
        '''
        print jobad["jobtitle"]
        #print jobad["url"]
        #print job_info
        #print ''
        #print ''

