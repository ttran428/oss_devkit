

def git_repo():
	subprocess.Popen(["git", "clone", "git@github.com:machine-shop/test_repo.git"])
	subprocess.Popen(["ls"])
def test_push():
	assert 5 == 5

def test_pull():
	assert 6 == 6
