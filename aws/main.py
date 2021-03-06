import click
import config
from aws.spot import AWSSpotInstance
from aws.writers import Console


@click.group()
def spots():
    pass


@spots.group()
def spot():
    pass


@spot.command()
@click.option("--os", prompt=True, default=lambda: config.default_os)
@click.option("--type", prompt=True, default=lambda: config.default_instance_type)
def prices(os, type):
    spot = AWSSpotInstance(config)
    prices = spot.getPrices(os=os, instance_type=type)
    Console.prices(os, type, prices)


@spot.command()
@click.option("--owners", prompt=False, default=lambda: ['self'])
def images(owners):
    spot = AWSSpotInstance(config)
    images = spot.getImages(owners=owners)
    Console.images(images, owners)


@spot.command()
def running():
    spot = AWSSpotInstance(config)
    Console.reservations(
        spot.getInstanceRequests(),
        spot.getReservation()
    )


@spot.command()
@click.option("--price", prompt="Enter the desired price ")
@click.option("--image", prompt="Enter the image id ")
@click.option("--zone", prompt="Enter the zone name ")
@click.option("--type", default=lambda: config.default_instance_type)
@click.option("--security_group_id", default=lambda: config.default_security_group_id)
def create(price, image, zone, type, security_group_id):
    spot = AWSSpotInstance(config)
    spot.create(price=price, image=image, zone=zone, type=type,
        security_group_id=security_group_id)

@spot.command()
@click.option("--id", prompt="Enter the id to cancel ")
def cancel(id):
    spot = AWSSpotInstance(config)
    requests = spot.cancel(id)

    if isinstance(requests, list):
        Console.reservations(requests, [])
    else:
        Console.error(requests)

@spot.command()
@click.option("--id", prompt="Enter the id to terminate ")
def terminate(id):
    spot = AWSSpotInstance(config)
    instances = spot.terminate(id)

    if isinstance(instances, list):
        Console.reservations([], instances)
    else:
        Console.error(instances)


cli = click.CommandCollection(sources=[spots])


def main():
    cli()
