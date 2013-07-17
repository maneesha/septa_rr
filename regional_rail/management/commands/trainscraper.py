#creates manage.py command to run scraper, 
#integrating it into the django project

from django.core.management.base import BaseCommand, CommandError
from regional_rail.models import Trains
import simplejson
import urllib2
from datetime import date, datetime, time
import sys
import json
import psycopg2

class Command(BaseCommand):
    def handle(self, *args, **options):
        print "hello"
        #identify url 
        url = "http://www3.septa.org/hackathon/TrainView/"

        #read text from url as json data set
        #septa_json = urllib2.urlopen(url).read()  
        trainstatus = json.load(urllib2.urlopen(url)) #returns a file - like object
        #convert to a python-readable format (a list of dictionaries)
        #trainstatus = json.loads(septa_json)  #returns a string
        
        scraped_date = str(datetime.date(datetime.now())) 
        scraped_time = str(datetime.time(datetime.now()))
        ts = []
        for train in trainstatus:
            train["scraped_date"] = scraped_date
            train["scraped_time"] = scraped_time
            scrapedtrain = Trains()

            scrapedtrain.destination = train["dest"]
            scrapedtrain.source = train["SOURCE"]
            scrapedtrain.late = train["late"]
            scrapedtrain.lat = train["lat"]
            scrapedtrain.lon = train["lon"]
            scrapedtrain.trainno = train["trainno"]
            scrapedtrain.service = train["service"]
            scrapedtrain.nextstop = train["nextstop"]
            scrapedtrain.scraped_time = train["scraped_time"]
            scrapedtrain.scraped_date = train["scraped_date"]


            #trying to collapse above lines into one loop:
            #for t in "late, nextstop, scraped_time, service, lat, trainno, scraped_date, lon".split(", "):
                #setattr(scrapedtrain, t, train[t])
                #print t, type(t), #train[t], type(train[t]),
            scrapedtrain.save()
            #print scrapedtrain
            #print "----"
            ts.append(train.values())
            print scraped_time, scraped_date

        #for t in ts:
            #print t
        conn = psycopg2.connect(database = "regional_rail", user = "maneesha", host = "/tmp/")
        c = conn.cursor()
        query = "INSERT INTO regional_rail_trains(nextstop, scraped_time, service, destination, lat, trainno, late, source, scraped_date, lon) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        c.executemany(query, ts)
        conn.commit()
        c.close()




