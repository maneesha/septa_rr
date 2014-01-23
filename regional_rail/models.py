from django.db import models

class Trains(models.Model):
    late = models.IntegerField()
    destination = models.CharField(max_length = 100)
    scraped_date = models.DateField()
    nextstop = models.CharField(max_length = 100)
    service = models.CharField(max_length = 100)
    source = models.CharField(max_length = 100)
    lat = models.FloatField()
    trainno = models.CharField(max_length = 15)
    scraped_time = models.TimeField() 
    lon = models.FloatField()

    def __unicode__(self):
        return u'%d %s %s %s %s %s %s %s %s %s' % (self.late, self.destination, self.scraped_date, self.nextstop, self.service, self.source, self.lat, self.trainno, self.scraped_time, self.lon)









