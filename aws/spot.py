from datetime import datetime, timedelta

import connection


class AWSSpotInstance(object):
    def __init__(self, config):
        self.conn = None
        self.images = None
        self.history = None

        self.conn = connection.connect(config)

    def getImages(self, owners=['self']):
        self.images = list(self.conn.get_all_images(owners=owners))

    def getPrices(self, os, instance_type):
        to_date = datetime.now()
        from_date = to_date - timedelta(minutes=15)

        self.history = self.conn.get_spot_price_history(
            start_time=from_date.isoformat(),
            end_time=to_date.isoformat(),
            product_description=os,
            instance_type=instance_type)

        return self.history

    def getReservation(self, *reservation_ids):
        return self.conn.get_all_reservations(
            instance_ids=list(reservation_ids))

    def getInstanceRequests(self, *request_ids):
        return self.conn.get_all_spot_instance_requests(
            request_ids=list(request_ids))

    def create(self, price, image, zone, type):
        try:
            image = int(image)
            spot.getImages()
            image = spot.images[image].id
        except ValueError:
            pass

        self.conn.request_spot_instances(
            price=price,
            image_id=image,
            count=1,
            type='one-time',
            availability_zone_group=zone,
            instance_type=type)
