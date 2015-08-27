import boto.ec2


def connect(config):
    return boto.ec2.connect_to_region(config.region,
                                      aws_access_key_id=config.access_key_id,
                                      aws_secret_access_key=config.secret_key)
