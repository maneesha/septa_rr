#!/usr/bin/python
#successfully writes data to postgres db called regional_rail ( ?? and logs errors to txt file ??  NOT SURE ) 

import simplejson
import urllib2
from datetime import date, datetime, time
import psycopg2
import sys
import my_settings


#identify url 
url = "http://www3.septa.org/hackathon/TrainView/"

#read text from url as json data set
json = urllib2.urlopen(url).read()

#convert to a python-readable format (a list of dictionaries)
trainstatus = eval(json)

#add current date & time to each dictionary
#only works if these are converted to strings; does not work if they stay date/time types
scraped_date = datetime.date(datetime.now()) 
scraped_time = datetime.time(datetime.now())
for train in trainstatus:
	train["scraped_date"] = scraped_date
	train["scraped_time"] = scraped_time

#print trainstatus[0] #test to see if this can connect to db

#initialize conn to none so that an error will come up if we can't connect to db
conn = None

try:

    #establish database connection    
    conn = psycopg2.connect(database = my_settings.db, user= my_settings.user, host = my_settings.host)
    c = conn.cursor()

    #store values in list
    ts = []

    for t in trainstatus:
        ts.append(t.values())

    #create table if necessary   
    c.execute("CREATE TABLE IF NOT EXISTS regional_rail_trains (id SERIAL PRIMARY KEY, late INT, destination TEXT, scraped_date TEXT, nextstop TEXT, service TEXT, source TEXT, lat REAL, trainno TEXT, scraped_time TEXT, lon REAL)")
    
    #insert values into table if trains are running, null if not
    if trainstatus:
        query = "INSERT INTO regional_rail_trains (late, destination, nextstop, scraped_time, service, source, lat, trainno, scraped_date, lon) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        
        
        c.executemany(query, ts)

    else:
        error_log = open(my_settings.error_log, 'a')
        error = (str(scraped_date) + ", " + str(scraped_time) + ", " + "No data\n")
        error_log.write(error)


    #save changes
    conn.commit()   

except:
    #save to error log
    error_log = open(my_settings.error_log, 'a')
    error = (str(scraped_date) + ", " + str(scraped_time) + ", " + "Connection Error\n")
    error_log.write(error)


finally:
    #close db connection if necessary
    if conn:
        c.close()