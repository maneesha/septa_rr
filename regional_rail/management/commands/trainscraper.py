from django.core.management.base import BaseCommand, CommandError
from regional_rail.models import Trains
import simplejson
import urllib2
from datetime import date, datetime, time
import sys
import json

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
        
        scraped_date = datetime.date(datetime.now()) 
        scraped_time = datetime.time(datetime.now())
        for train in trainstatus:
            train["scraped_date"] = scraped_date
            train["scraped_time"] = scraped_time
            scrapedtrain = Trains()
            scrapedtrain.destination = train["dest"]
            scrapedtrain.source = train["SOURCE"]
            for t in "late, nextstop, scraped_time, service, lat, trainno, scraped_date, lon".split(", "):
                #setattr(scrapedtrain, t, train[t])
                print t, type(t), #train[t], type(train[t]),
            scrapedtrain.save()

        
