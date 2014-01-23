#creates manage.py command to run scraper, 
#integrating it into the django project

from django.core.management.base import BaseCommand, CommandError

from regional_rail.models import Trains
import urllib2
from datetime import date, datetime, time
from django.utils.timezone import utc
import json
import psycopg2
import my_settings

class Command(BaseCommand):
    def handle(self, *args, **options):
        #identify url 
        url = "http://www3.septa.org/hackathon/TrainView/"

        #get the scraped date & time since that's not part of the json feed

        #IF NO INTERNET CONNECTION, HOW TO GET DATE & TIME??  GETS SYSTEM TIME BUT TIMEZONE PART DOES NOT WORK??
        scraped_date = datetime.date(datetime.now()) 
        scraped_time = datetime.time(datetime.now())
        
        ## Below: the timezone thing that I don't know if I need or how to work        
        ## x = datetime.utcnow().replace(tzinfo=utc)

        try:

            #current_trains will be a list of dictionaries
            #each dictionary is one currently running train
            current_trains = json.load(urllib2.urlopen(url))         

            for train in current_trains:
                #complete the data set by adding date / time 
                train["scraped_date"] = scraped_date
                train["scraped_time"] = scraped_time
               
                #scrapedtrain is based on the Trains model defined in models.py    
                #scraped train is an object based on class regional_rail.models.Trains
                scrapedtrain = Trains()

                #There is probably an easier & shorter way to do this.
                #Maybe with setattr()
                #This is like performing a SQL INSERT statement.
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

                #Saves to database as defined in django settings
                scrapedtrain.save()
                
        except:
            print "no connection"
            conn = psycopg2.connect(database = my_settings.db, user = my_settings.user, host = my_settings.host)
            c = conn.cursor()
            e = "Conn/Data Error"
            #error_log = (e, e, 9999, 9999, 9999, e, e, e, scraped_time, scraped_date, e, e, e)
            error_log = (e, e, 9999, 9999, 9999, e, e, e, e, e, scraped_time, scraped_date)
            query = "INSERT INTO regional_rail_trains (destination, source, late, lat, lon, trainno, service, nextstop, scraped_time, scraped_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            c.execute(query, error_log)
            conn.commit()
            c.close()



           
