from flask import Flask, render_template
import webpage
import os
from os.path import join as pjoin

def path_to_pic():
    """Finds path to .git folder
    """
    path_repo = os.path.abspath('.')
    # if not in directory with .git, keep going back to find file
    while os.path.abspath(path_repo) != '/' and not os.path.isdir(pjoin(path_repo, '.git')):
        path_repo = pjoin(path_repo, '..')
    path_git = pjoin(path_repo, ".git")
    path_pic = pjoin(path_git, ".git-hub")
    path_pic = pjoin(path_pic, "PRs.png")
    return path_pic

app = Flask(__name__, static_url_path='')

@app.route("/")
def render_pages():
    list_of_prs = webpage.week_old_comments()
    no_diss = webpage.no_discussion()
    popular = webpage.most_active_prs()
    oldest = webpage.oldest_prs()
    mine = webpage.prs_with_me()
    unmergeable = webpage.unmergeable_prs()
    # picture = path_to_pic
    # print(picture)
    return render_template('template.html', week_old=list_of_prs, no_discussion=no_diss, active_prs=popular, oldest_prs=oldest, my_prs=mine, unmergeable_prs=unmergeable, picture="PRs.png")


def main():
    port = 3000
    app.run(port = port)