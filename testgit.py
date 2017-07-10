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

		#runs git and gets user and repo of current folder.
		process = subprocess.Popen("git remote -v", stdout=subprocess.PIPE)
		name = str(process.stdout.read())
		almost = name.split(" ", 1)[0] #splits by first space to get the fetch url
		url = almost.split("\\t", 1)[1]#takes out information("origin") before url
		arguments = url.split(".com/")[1]
		arguments = arguments[:len(arguments) - 4] #takes out ".git"
		username, repo = arguments.split("/")
		
		#gets token from config folder.
		try:
			with open(".config/git-hub.yaml") as stream:
				yaml_file = str(yaml.load(stream))
				token = yaml_file.split("=")[1].strip()
		except:
			print("Needs an authentification token in ~/.config/git-hub.yaml")
			print("file simply says:")
			print("token = iejfjlkajdf")
			print("'iejfjlkajdf' being the token name from github ")

		#gets pr and runs command.
		try:
			g = Github(token)
			pr = g.get_user(username).get_repo(repo).get_pull(num)
			label = pr.head.label
			other_user, branch = label.split(":")
			# subprocess.Popen("git remote add " + other_user + " git@github.com:" + other_user + "/" +"test_repo")
			# subprocess.Popen("git fetch " + other_user)
			# subprocess.Popen("git checkout -b pr/" + str(num) + " " + other_user + "/" + branch)

			print("git remote add " + other_user + " git@github.com:" + other_user + "/" +"test_repo")
			print("git fetch " + other_user)
			print("git checkout -b pr/" + str(num) + " " + other_user + "/" + branch)
		
		except:
			print("The authentification token is not valid")
			print("or there is no pr with number" + str(num))
		


	else:
		print("invalid command")
