from datetime import datetime
from itertools import groupby
from operator import attrgetter

class Console(object):
    @staticmethod
    def images(images, owners):
        print ""
        print "Images for {owners}:".format(owners=owners)
        print "-----"
        for number, image in enumerate(images):
            print "\t{number}. {name}: {id} {region}".format(
                number=number, name=image.name,
                id=image.id, region=image.region)

    @staticmethod
    def prices(os, instance_type, prices):
        keyfunc = attrgetter('availability_zone')
        prices = sorted(prices, key=keyfunc)

        print ""
        print "Prices for: {os} - {type}".format(os=os, type=instance_type)

        for zone, prices in groupby(prices, key=keyfunc):
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

    @staticmethod
    def reservations(requests, reservations):
        for request in requests:
            print request

        for reservation in reservations:
            print reservation
