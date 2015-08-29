from datetime import datetime
from itertools import groupby
from operator import attrgetter

import click

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
            Console._header(zone)
            for price in prices:
                time = datetime.strptime(
                    price.timestamp,
                    "%Y-%m-%dT%H:%M:%S.%fZ")

                print "\t{time} - ${price}".format(
                    price=price.price,
                    time=time.strftime("%Y-%m-%d %I:%M %p"))

    @staticmethod
    def reservations(requests, reservations):
        Console._header("Requests")
        for request in requests:
            print "{id}: {instance_id} {price} {state} {status} {create_time}".format(**request.__dict__)

        Console._header("Reservations")
        for reservation in reservations:
            print reservation

    @staticmethod
    def error(text):
        click.echo(click.style(text, fg='red'))

    @staticmethod
    def _header(text):
        print ""
        print text
        print "-----"
