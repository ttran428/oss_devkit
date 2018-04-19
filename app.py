import jinja2
import os
import toml
import re
from os.path import join as pjoin
from queue import *
from datetime import datetime
from datetime import timedelta


def path_to_git():
    """Finds path to .git folder
    """
    path_repo = os.path.abspath('.')
    while os.path.abspath(path_repo) != '/' and not os.path.isdir(pjoin(path_repo, '.git')):
        path_repo = pjoin(path_repo, '..')
    path_git = pjoin(path_repo, ".git")
    return path_git


def path_to_toml():
    """Finds path to pull-requests.toml
    """
    path_git = path_to_git()
    path_github = pjoin(path_git, 'git-hub')
    path_prs = pjoin(path_github, 'pull-requests.toml')
    return path_prs


def week_old_comments():
    """Main function to find PRs that haven't been commented on in over a week
    """
    try:
        path_prs = path_to_toml()
        f = open(path_prs, "r")
        pr_dict = toml.load(f)
    except (OSError, IOError) as e:
        print("ERROR: pull-requests.toml doesn't exist. Run 'git hub sync' and try again")
    open_dict = pr_dict['open pull requests']
    opened, url = week_old_comments_helper(open_dict)
    return opened, url


def week_old_comments_helper(prs):
    """Helper function that finds all PRs in a dictionary that are over a week old
    """
    all_prs = []
    url = []
    for num in list(prs.keys()):
        pr = prs[num]
        if(pr['most_recent'] == ""):
            all_prs.append(f'PR #{num}: {pr["user"]}/{pr["branch"]}: {pr["comment"]}')
            url.append(pr["url"])
        else:
            comment_time = parse_time(pr['most_recent'])
            if((datetime.now() - comment_time).days > 7):
                all_prs.append(f'PR #{num}: {pr["user"]}/{pr["branch"]}: {pr["comment"]}')
                url.append(pr["url"])
    return all_prs, url


def parse_time(time):
    """
    Converts time into python datetime object

    Parameters
    ----------
    Time : String
        Time that git-hub gives
    """
    date = time.split('T')[0]
    time = time.split('T')[1][:-1]
    year, date = date.split('-', 1)
    month, date = date.split('-', 1)
    day = date
    hour, time = time.split(':', 1)
    minute, time = time.split(':', 1)
    second = time
    d = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
    return d


def oldest_prs():
    """Finds oldest prs by date created"""
    try:
        path_prs = path_to_toml()
        f = open(path_prs, "r")
        pr_dict = toml.load(f)
    except (OSError, IOError) as e:
        print("ERROR: pull-requests.toml doesn't exist. Run 'git hub sync' and try again")
    open_dict = pr_dict['open pull requests']
    oldest, url = oldest_prs_helper(open_dict)
    return oldest, url


def oldest_prs_helper(prs):
    """Helper function that finds oldest prs"""
    oldest = []
    url = []
    q = PriorityQueue(maxsize=3)
    old = timedelta()
    now = datetime.now()
    for pr_num in list(prs.keys()):
        pr = prs[pr_num]
        if now-parse_time(pr['created_at']) > old:
            if q.qsize() == 3:
                q.get()
            q.put(now-parse_time(pr['created_at']))
            old = q.get()
            q.put(old)

    for pr_num in list(prs.keys()):
        pr = prs[pr_num]
        if now-parse_time(pr['created_at']) > old:
            days = str(now-parse_time(pr['created_at']))[:8]
            oldest.append(f'PR #{pr_num}: {pr["user"]}/{pr["branch"]}: {pr["title"]} --  {days}')
            url.append(pr["url"])
    return oldest, url


def most_active_prs():
    """Finds most active prs by most comments"""
    try:
        path_prs = path_to_toml()
        f = open(path_prs, "r")
        pr_dict = toml.load(f)
    except (OSError, IOError) as e:
        print("ERROR: pull-requests.toml doesn't exist. Run 'git hub sync' and try again")
    open_dict = pr_dict['open pull requests']
    most_popular, url = most_active_prs_helper(open_dict)
    return most_popular, url


def most_active_prs_helper(prs):
    """helper function to find pull requests."""
    popular = []
    url = []
    q = PriorityQueue()
    for pr_num in list(prs.keys()):
        pr = prs[pr_num]
        recent_comment_count = recent_comments(pr)
        q.put(-recent_comment_count)

    most_comments = set()
    count = 0
    while q.qsize() != 0 and count != 3:
        most_comments.add(-q.get())
        count += 1
    most_comments.discard(0)
    for pr_num in list(prs.keys()):
        pr = prs[pr_num]
        recent_comment_count = recent_comments(pr)
        if recent_comment_count in most_comments:
            popular.append(f'PR #{pr_num}: {pr["user"]}/{pr["branch"]}: {pr["title"]} -- {recent_comment_count} comment(s)')
            url.append(pr["url"])
    return popular, url


def recent_comments(pr):
    """Counts how many comments in the last two weeks"""
    count = 0
    comment_dates = pr['comment_dates']
    for date in comment_dates:
        comment_time = parse_time(date)
        if((datetime.now() - comment_time).days < 14):
            count += 1
    return count


def no_discussion_prs():
    """Finds PRs that haven't seen any discussion. """
    try:
        path_prs = path_to_toml()
        f = open(path_prs, "r")
        pr_dict = toml.load(f)
    except (OSError, IOError) as e:
        print("ERROR: pull-requests.toml doesn't exist. Run 'git hub sync' and try again")
    open_dict = pr_dict['open pull requests']
    opened, url = no_discussion_helper(open_dict)
    return opened, url


def no_discussion_helper(prs):
    """helper function to find pull requests."""
    no_disc_prs = []
    url = []
    for pr_num in list(prs.keys()):
        pr = prs[pr_num]
        if pr['comment_count'] == "0":
            no_disc_prs.append(f'PR #{pr_num}: {pr["user"]}/{pr["branch"]}: {pr["title"]}')
            url.append(pr["url"])
    return no_disc_prs, url


def prs_with_me():
    """Finds PRs that I have commented on"""
    try:
        path_prs = path_to_toml()
        f = open(path_prs, "r")
        pr_dict = toml.load(f)
    except (OSError, IOError) as e:
        print("ERROR: pull-requests.toml doesn't exist. Run 'git hub sync' and try again")
    open_dict = pr_dict['open pull requests']
    opened, url = find_prs_with_me(open_dict)
    return opened, url


def find_prs_with_me(prs):
    """helper function to find pull requests."""
    prs_with_me = []
    url = []
    for pr_num in list(prs.keys()):
        pr = prs[pr_num]
        if pr['self_comment'] == "True":
            prs_with_me.append(f'PR #{pr_num}: {pr["user"]}/{pr["branch"]}: {pr["title"]}')
            url.append(pr["url"])
    return prs_with_me, url


def unmergeable():
    """Finds PRs that haven't seen any discussion. """
    try:
        path_prs = path_to_toml()
        f = open(path_prs, "r")
        pr_dict = toml.load(f)
    except (OSError, IOError) as e:
        print("ERROR: pull-requests.toml doesn't exist. Run 'git hub sync' and try again")
    open_dict = pr_dict['open pull requests']
    opened, url = find_unmergeable_prs(open_dict)
    return opened, url


def find_unmergeable_prs(prs):
    """helper function to find pull requests."""
    unmergeable_prs = []
    url = []
    for pr_num in list(prs.keys()):
        pr = prs[pr_num]
        if pr['mergeable'] == "False":
            unmergeable_prs.append(f'PR #{pr_num}: {pr["user"]}/{pr["branch"]}: {pr["title"]}')
            url.append(pr["url"])
    return unmergeable_prs, url


def issues_no_comment():
    """Finds issues without any comments. """
    try:
        path_prs = path_to_toml()
        f = open(path_prs, "r")
        pr_dict = toml.load(f)
    except (OSError, IOError) as e:
        print("ERROR: pull-requests.toml doesn't exist. Run 'git hub sync' and try again")
    if 'issues' not in pr_dict:
        return None, None
    open_dict = pr_dict['issues']
    opened, url = find_issues_no_comments(open_dict)
    return opened, url


def find_issues_no_comments(issues):
    """helper function to find issues with no comments."""
    issues_no_comments = []
    url = []
    for num in list(issues.keys()):
        issue = issues[num]
        if issue['comment_count'] == "0":
            issues_no_comments.append(f'issue #{num}: {issue["title"]}')
            url.append(issues["url"])
    return issues_no_comments, url


def tickets_referred(comments):
    """Finds tickets in comments of pull requests or issues"""
    issues = []
    for comment in comments:
        if "#" in comment:
            tickets_referred = (re.findall(r"(#\d+)", comment))
            for ticket in tickets_referred:
                ticket = ticket[1:]
                issues.append(ticket)
    return issues


def closed_pr_refer_ticket():
    """Finds issues that are referred to from prs and other issues """
    try:
        path_prs = path_to_toml()
        f = open(path_prs, "r")
        pr_dict = toml.load(f)
    except (OSError, IOError) as e:
        print("ERROR: pull-requests.toml doesn't exist. Run 'git hub sync' and try again")
    closed = pr_dict['closed pull requests']
    if 'issues' not in pr_dict:
        return None, None
    issues = pr_dict['issues']
    issues_referred, urls = find_closed_pr_refer_ticket(closed, issues)
    return issues_referred, urls


def find_closed_pr_refer_ticket(closed_prs, issues):
    """helper function to find closed prs that reference open issues"""
    unresolved_issues = []
    urls = []
    for num in closed_prs:
        pr = closed_prs[num]
        referred_tickets = tickets_referred(pr['comment_content'])
        for ticket in referred_tickets:
            if ticket in issues:
                unresolved_issues.append(f'issue #{ticket}: {issues[ticket]["title"]}')
                urls.append(issues[ticket]["url"])
    return unresolved_issues, urls


def popular_ticket():
    """tickets that are referred to many times"""
    try:
        path_prs = path_to_toml()
        f = open(path_prs, "r")
        pr_dict = toml.load(f)
    except (OSError, IOError) as e:

        print("ERROR: pull-requests.toml doesn't exist. Run 'git hub sync' and try again")
    opened = pr_dict['open pull requests']
    if 'issues' not in pr_dict:
        return None, None
    issues = pr_dict['issues']
    popular, urls = find_popular_tickets(opened, issues)
    return popular, urls


def find_popular_tickets(opened, issues):
    """helper function to find popular tickets"""
    tickets = {}
    for num in opened:
        pr = opened[num]
        referred_tickets_in_prs = tickets_referred(pr['comment_content'])
        for ticket in referred_tickets_in_prs:
            if ticket in tickets:
                tickets[ticket] += 1
            else:
                tickets[ticket] = 1
    for num in issues:
        issue = issues[num]
        referred_tickets_in_tickets = tickets_referred(issue['comment_body'])
        for ticket in referred_tickets_in_prs:
            if ticket in tickets:
                tickets[ticket] += 1
            else:
                tickets[ticket] = 1
    q = PriorityQueue()
    for ticket in list(tickets.keys()):
        q.put(-tickets[ticket])
    count = 0
    popular_count = set()
    while q.qsize() != 0 and count < 3:
        popular_count.add(-q.get())
        count += 1
    most_popular = []
    urls = []
    for ticket in list(tickets.keys()):
        if tickets[ticket] in popular_count:
            most_popular.append(f'issue #{ticket}: {issues[ticket]["title"]}')
            urls.append(issues[ticket]["url"])
    return most_popular, urls



def main():
    week_old, week_old_url = week_old_comments()
    no_discussion, no_discussion_url = no_discussion_prs()
    most_active, most_active_url = most_active_prs()
    oldest_pr, oldest_pr_url = oldest_prs()
    my_prs, my_prs_url = prs_with_me()
    unmergeable_prs, unmergeable_prs_url = unmergeable()
    issues_no_comments, issues_no_comments_url = issues_no_comment()
    closed_pr_refer_tickets, closed_pr_refer_tickets_url = closed_pr_refer_ticket()
    popular_tickets, popular_tickets_url = popular_ticket()

    path_git = path_to_git()
    path_pic = path_pic = pjoin(path_git, "git-hub/PRs.png")
    if not os.path.exists(path_pic):
        path_pic = None

    file_path = os.path.dirname(__file__)
    complete_path = os.path.join(file_path, 'templates/template.html')
    style = os.path.join(file_path, 'templates/style.css')
    script = os.path.join(file_path, 'templates/script.js')
    path, filename = os.path.split(complete_path)
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(path or './'))
    template = env.get_template(filename)
    out = template.render({'style': style, 'script': script, 'picture': path_pic, 'issues_no_comments': issues_no_comments, 'closed_pr_refer_tickets': closed_pr_refer_tickets, 'popular_tickets': popular_tickets, 'week_old': week_old, 'no_discussion': no_discussion, 'active_prs': most_active, 'oldest_prs': oldest_pr, 'my_prs': my_prs, 'unmergeable_prs': unmergeable_prs,
     'issues_no_comments_url': issues_no_comments_url, 'closed_pr_refer_tickets_url': closed_pr_refer_tickets_url, 'popular_tickets_url': popular_tickets_url, 'week_old_url': week_old_url, 'no_discussion_url': no_discussion_url, 'active_prs_url': most_active_url, 'oldest_prs_url': oldest_pr_url, 'my_prs_url': my_prs_url, 'unmergeable_prs_url': unmergeable_prs_url})
    fname = "./output.html"
    print("Template rendered at output.html")
    with open(fname, 'w') as f:
        f.write(out)
