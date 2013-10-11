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
        scraped_date = str(datetime.date(datetime.now())) 
        scraped_time = str(datetime.time(datetime.now()))
        d_and_t = datetime.utcnow().replace(tzinfo=utc)
        print d_and_t

        try:

            #current_trains will be a list of dictionaries
            #each dictionary is one currently running train
            current_trains = json.load(urllib2.urlopen(url))         

            for train in current_trains:
                #complete the data set by adding date / time 
                train["scraped_date"] = scraped_date
                train["scraped_time"] = scraped_time
                train["date_and_time"] = d_and_t

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
                scrapedtrain.date_and_time = train["date_and_time"]

                #Saves to database as defined in django settings
                scrapedtrain.save()
                
        except:
            print "no connection"
            conn = psycopg2.connect(database = my_settings.db, user = my_settings.user, host = my_settings.host)
            c = conn.cursor()
            e = "Conn/Data Error"
            error_log = (e, e, 9999, 9999, 9999, e, e, e, scraped_time, scraped_date, d_and_t)
            query = "INSERT INTO regional_rail_trains (destination, source, late, lat, lon, trainno, service, nextstop, scraped_time, scraped_date, date_and_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            c.execute(query, error_log)
            conn.commit()
            c.close()



           
