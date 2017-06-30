import subprocess 
from github import Github 
import yaml
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
		print("pulling down pr " + str(num) + ":" )

		#runs git and gets user and repo.
		process = subprocess.Popen("git remote -v", stdout=subprocess.PIPE)
		name = str(process.stdout.read())
		almost = name.split(" ", 1)[0] #splits by first space to get the fetch url
		url = almost.split("\\t", 1)[1]#takes out information("origin") before url
		arguments = url.split(".com/")[1]
		arguments = arguments[:len(arguments) - 4] #takes out ".git"
		username, repo = arguments.split("/")
		
		try:
			with open(".config/git-hub.yaml") as stream:
				yaml_file = str(yaml.load(stream))
				token = yaml_file.split("=")[1].strip()
		except:
			print("Needs an authentification token in ~/.config/git-hub.yaml")
			print("file simply says:")
			print("token = iejfjlkajdf")
			print("'iejfjlkajdf' being the token name from github ")

		try:
			g = Github(token)#authentification token goes here
			pr = g.get_user(username).get_repo(repo).get_pull(num)
			print(pr.body)
		except:
			Print("The authentification token is not valid")
			print("or there is no pr with number" + str(num))
		


	else:
		print("invalid command")

#trying to use subprocess
# process = subprocess.Popen("git remote -v", stdout=subprocess.PIPE)
# name = str(process.stdout.read())
# almost = name.split(" ", 1)[0] #splits by first space to get the fetch url
# url = almost.split("\\t", 1)[1]#takes out information("origin") before url
# arguments = url.split(".com/")[1]
# arguments = arguments[:len(arguments) - 4] #takes out ".git"
# username, repo = arguments.split("/")



		# try:
		# 	#pr = g.get_user(username).get_repo(repo).get_pull(num)
		# 	#print(pr.body)
		# 	repo = g.get_user(username).get_repo(repo)
		# 	print(repo.description)
		# except:
		# 	print("no pr with number " + str(num))
		# 	repo = g.get_user(username).get_repo(repo)
		