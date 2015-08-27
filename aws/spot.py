from datetime import datetime, timedelta
from itertools import groupby
from operator import attrgetter

import connection


class AWSSpotInstance(object):
    def __init__(self, config):
        self.conn = None
        self.images = None
        self.history = None

        self.conn = connection.connect(config)

    def getImages(self, owners):
        self.images = list(self.conn.get_all_images(owners=owners))

    def getPriceHistory(self, os, instance_type):
        to_date = datetime.now()
        from_date = to_date - timedelta(minutes=15)

        self.history = self.conn.get_spot_price_history(
            start_time=from_date.isoformat(),
            end_time=to_date.isoformat(),
            product_description=os,
            instance_type=instance_type)

        return self.history
        
    def printImages(self, owners):
        self.getImages(owners)
        
        print ""
        print "Images for {owners}:".format(owners=owners)
        print "-----"
        for number, image in enumerate(self.images):
            print "\t{number}. {name}: {id} {region}".format(
                number=number, name=image.name,
                id=image.id, region=image.region)

    def printPriceHistory(self, os, instance_type):
        self.getPriceHistory(os, instance_type)
        
        keyfunc = attrgetter('availability_zone')
        history = sorted(self.history, key=keyfunc)
        
        print ""
        print "Prices for: {os} - {type}".format(os=os, type=instance_type)

        for zone, prices in groupby(history, key=keyfunc):
            print ""
            print zone
            print "-----"
            for price in prices:
                time = datetime.strptime(
                    price.timestamp,
                    "%Y-%m-%dT%H:%M:%S.%fZ")

                print "\t{time} - ${price}".format(
                    price=price.price,
                    time=time.strftime("%Y-%m-%d %I:%M %p"))
