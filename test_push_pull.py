
import subprocess
import os
def test_git_repo():
    os.makedirs("test3")
    os.chdir(os.getcwd() + "/test3")
    p = subprocess.Popen(["git", "clone", "https://github.com/machine-shop/test_repo.git"])
    p.communicate()
    os.chdir(os.getcwd() + "/test_repo")

    print("running new command")
    #command = subprocess.Popen(["git", "hub", "pr", "1"], stdout=subprocess.PIPE, stdin = subprocess.PIPE)
    p = subprocess.Popen(["git", "remote", "add", "ttran428", 'git@github.com:ttran428/test_repo'])
    p.communicate()
    p = subprocess.Popen(["git", "fetch", "ttran428"], stdout=subprocess.PIPE)
    p.stdout.read()
    p = subprocess.Popen(["git", "checkout", "-b",'pr/1', 'ttran428/test'], stdout=subprocess.PIPE)
    assert str(p.stdout.read()) == 'Branch pr/1 set up to track remote branch test from ttran428.\n'
    os.chdir(os.getcwd() + "/../..")
    subprocess.Popen(["rm", "-rf", "test3"])


def test_push():
    assert 5 == 5

def test_pull():
    assert 6 == 6
