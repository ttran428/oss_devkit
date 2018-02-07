from flask import Flask, render_template
import webpage
import os
from os.path import join as pjoin
import plot_pr


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
    issues_no_comments = webpage.issues_no_comments()
    closed_pr_refer_tickets = webpage.closed_pr_refer_tickets()
    popular_tickets = webpage.popular_tickets()
    plot_pr.execute()  
    picture = path_to_pic()
    return render_template('template.html', week_old=list_of_prs, no_discussion=no_diss, active_prs=popular, oldest_prs=oldest,
                           my_prs=mine, unmergeable_prs=unmergeable, no_disc_issues=issues_no_comments, pr_refer_tickets=closed_pr_refer_tickets,
                           hot_tickets=popular_tickets, picture=picture)


def main():
    port = 3000
    app.run(port=port)
