Command Line Functions
======================

git hub pr
----------
Pulls down and checkout the branch of the pull request. For example, the command

::

  git hub pr 42

is equivalent to these commands at the terminal:
	
::

  git remote add user git@github.com:user/repo
  git fetch user
  git checkout -b pr/num user/branch

git hub push
------------
Pushes changes back to a branch. It will run this command in the terminal.::

  git push user pr/num:branch

git hub sync
------------
Updates and saves pull requests in pull-requests.toml in the .git folder.

git hub search [*args]
----------------------
Searches in pull-requests.toml to find pull-requests that match search keywords in *args.

.. note:: It is recommended to run **git hub sync** to update pull-requests.toml before running **git hub search [*args]**.

git hub render
--------------
Creates a html file of facts and statistics about the project.

git hub image
-------------
Creates the image of open pull requests over time.
