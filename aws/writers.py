from datetime import datetime
from dateutil import tz
from itertools import groupby
from operator import attrgetter

import click

class Console(object):
    @staticmethod
    def images(images, owners):
        print ""
        print "Images for {owners}:".format(owners=owners)
        print "-----"
        if not len(images):
            print "No images found."

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
                print "\t{time} - ${price}".format(
                    price=price.price,
                    time=Console._convertTime(price.timestamp))

    @staticmethod
    def reservations(requests, reservations):
        Console._header("Requests")
        for request in requests:
            request.create_time = Console._convertTime(request.create_time)
            print "{id}: {instance_id} {price} {state} {status} {create_time}".format(**request.__dict__)

        Console._header("Reservations")
        for reservation in reservations:
            instance = reservation.instances[0]
            instance.__dict__['state'] = instance.state
            print "{id}: {ip_address} {instance_type} {state}".format(**instance.__dict__)

    @staticmethod
    def error(text):
        click.echo(click.style(text, fg='red'))

    @staticmethod
    def _header(text):
        print ""
        print text
        print "-----"

    @staticmethod
    def _convertTime(time):
        from_zone = tz.gettz('UTC')
        to_zone = tz.tzlocal()

        utc = datetime.strptime(
                time,
                "%Y-%m-%dT%H:%M:%S.%fZ")
        utc = utc.replace(tzinfo=from_zone)
        local = utc.astimezone(to_zone)

        return local.strftime("%Y-%m-%d %I:%M %p")
