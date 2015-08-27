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
    
    
    

cli = click.CommandCollection(sources=[spots])

def main():
    cli()