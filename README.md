AWS Launch Wrapper
=========== 
Small wrapper around [boto](https://github.com/boto/boto) to make calls to AWS EC2.

This was originally developed in order to spin up spot instances quickly. I got interested on how to run games on EC2 [[post here]](http://lg.io/2015/07/05/revised-and-much-faster-run-your-own-highend-cloud-gaming-service-on-ec2.html) and got tired of doing it through the AWS UI.

Config
=====
Open the `config.py` file and update it with your information. 

	region = <region-to-connect-to>
	access_key_id = <your-access-key>
	secret_key = <your-secret>

The next settings are optional. If you don't provide them, the CLI will ask for them when appropriate. They're there for convenience so that you don't have to type them every single time.

For example, to set up the same instance as required by the post above, your settings will look like:

    default_os = "Windows"
	default_instance_type = "g2.2xlange"
	default_security_group_id = <group-id>

Usage
===


	> python .\run.py spot
	Usage: run.py spot [OPTIONS] COMMAND [ARGS]...
	
	Options:
	  --help  Show this message and exit.
	
	Commands:
	  cancel
	  create
	  images
	  prices
	  running
	  terminate