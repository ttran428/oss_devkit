
from github import Github 

import click


@click.group()
def cli():
	pass

@cli.command()
@click.argument("command", default = "")
@click.argument("num", default = 0)
#activates when user types in cmd "testgit hub pr"
def hub(command,num):
	if command == "pr":
		print("pulling down pr " + str(num) + ":")
		g = Github('')#authentification token goes here
		pr = g.get_user("machine-shop").get_repo("music-features").get_pull(num)
		print(pr.body)
	else:
		print("invalid command")



