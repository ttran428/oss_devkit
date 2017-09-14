Command Line Functions
======================
**1. git hub pr** [num]
Pulls down and checkout the branch of the pull request [num]. It will run these commands in the terminal.::
	
	git remote add user git@github.com:user/repo
    git fetch user
    git checkout -b pr/num user/branch



**2. git hub push**
Pushes changes back to a branch. It will run this command in the terminal.::
	
	git push user pr/num:branch

**3. git hub sync**
Updates and saves pull requests in pull-requests.toml in the .git folder.

**4. git hub search** [*args]
Searches in pull-requests.toml to find pull-requests that match search keywords in *args.

.. note:: It is recommended to run **git hub sync** to update pull-requests.toml before running **git hub search** [*args].
