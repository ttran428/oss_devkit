
from github import Github 

import click


@click.group()
def cli():
	pass

@cli.command()
@click.argument("command", default = "")
@click.argument("num", default = 0)
#activates when user types in cmd "test hub pr"
def hub(command,num):
	if command == "pr":
		print("pulling down pr " + str(num))
		g = Github('')#authentification token goes here
		g.get_user().get_repo("oss_devkit").get_pull(num)
	else:
		print("invalid command")

#testing to get all pull requests
# g = Github('')
# for pulls in g.get_user().get_repo("oss_devkit").get_pulls():


