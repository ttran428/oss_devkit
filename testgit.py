
# from github import Github 

import click


@click.group()
def cli():
	pass

@cli.command()
@click.argument("command", default = "")
@click.argument("num", default = 0)
def hub(command,num):
    if command == "pr":
    	print("pulling down pr " + str(num))
    else:
    	print("invalid command")


# g = Github("ttran428", "Tweedletee428")
# for repo in g.get_user().get_repos():
#     print(1)
# # print(g.get_user().get_repos())