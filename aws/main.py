import click
import config
from aws.spot import AWSSpotInstance


@click.group()
def spots():
    pass


@spots.group()
def spot():
    pass


@spot.command()
@click.option("--os", default=lambda: config.default_os)
@click.option("--type", default=lambda: config.default_instance_type)
def prices(os, type):
    spot = AWSSpotInstance(config)
    spot.printPriceHistory(os=os, instance_type=type)


@spot.command()
@click.option("--owners", prompt=False, default=lambda: ['self'])
def images(owners):
    spot = AWSSpotInstance(config)
    spot.printImages(owners=owners)


@spot.command()
def running():
    spot = AWSSpotInstance(config)
    spot.getAllReservations()


@spot.command()
@click.option("--price", prompt="Enter the desired price ")
@click.option("--image", prompt="Enter the image id ")
@click.option("--zone", prompt="Enter the zone name ")
@click.option("--type", default=lambda: config.default_instance_type)
def create(price, image, zone, type):
    spot = AWSSpotInstance(config)
    try:
        image = int(image)
        spot.getImages()
        image = spot.images[image].id
    except ValueError:
        pass

    spot.create(price=price, image=image, zone=zone, type=type)


cli = click.CommandCollection(sources=[spots])


def main():
    cli()
