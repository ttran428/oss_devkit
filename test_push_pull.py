
import subprocess
def test_git_repo():
	subprocess.Popen(["mkdir", "test3"])
	subprocess.Popen(["ls"])
	subprocess.Popen(["cd", "test3"])
	subprocess.Popen(["git", "clone", "https://github.com/ttran428/test_repo.git"])
	subprocess.Popen(["ls"])
	subprocess.Popen(["cd", "test_repo"])
def test_push():
	assert 5 == 5

def test_pull():
	assert 6 == 6
