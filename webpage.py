import os
import toml
import re
from queue import PriorityQueue
from datetime import datetime
from os.path import join as pjoin
import plot_pr

#plot_pr.execute()  # before it didn't work since the cache directory wasn't made yet.


def path_to_git():
    """Finds path to .git folder
    """
    path_repo = os.path.abspath('.')
    # if not in directory with .git, keep going back to find file
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
        pr_dict = toml.load(f)      # fetches toml file and creates a dictionary
    except (OSError, IOError) as e:
        # if pull-requests.toml hasnt been created yet calls sync and then reties to fetch
        print("ERROR: pull-requests.toml doesn't exist. Run 'git hub sync' and try again")
    open_dict = pr_dict['open pull requests']
    opened = week_old_comments_helper(open_dict)
    return opened


def week_old_comments_helper(prs):
    """Helper function that finds all PRs in a dictionary that are over a week old
    """
    all_prs = []
    for num in list(prs.keys()):
        pr = prs[num]
        if(pr['most_recent_comment'] == ""):
            all_prs.append(f'PR #{num}: {pr["user"]}/{pr["branch"]}: {pr["comment"]}')
        else:
            comment_time = parse_time(pr['most_recent_comment'])
            if((datetime.now() - comment_time).days > 7):
                all_prs.append(f'PR #{num}: {pr["user"]}/{pr["branch"]}: {pr["comment"]}')
    return all_prs


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
        pr_dict = toml.load(f)      # fetches toml file and creates a dictionary
    except (OSError, IOError) as e:
        # if pull-requests.toml hasnt been created yet calls sync and then reties to fetch
        print("ERROR: pull-requests.toml doesn't exist. Run 'git hub sync' and try again")
    open_dict = pr_dict['open pull requests']
    oldest = oldest_prs_helper(open_dict)
    return oldest


def oldest_prs_helper(prs):
    """Helper function that finds oldest prs"""
    oldest = []
    q = PriorityQueue(maxsize=3)
    for pr_num in list(prs.keys()):
        pr = prs[pr_num]
        q.put(parse_time(pr['created_at']))

    oldest_dates = set()
    count = 0
    while q.qsize() != 0 and count != 3:
        oldest_dates.add(q.get())
        count += 1

    for pr_num in list(prs.keys()):
        pr = prs[pr_num]
        if parse_time(pr['created_at']) in oldest_dates:
            days = str(datetime.now()-parse_time(pr['created_at']))[:8]
            oldest.append(f'PR #{pr_num}: {pr["user"]}/{pr["branch"]}: {pr["title"]} --  {days}')
    return oldest


def most_active_prs():
    """Finds most active prs by most comments"""
    try:
        path_prs = path_to_toml()
        f = open(path_prs, "r")
        pr_dict = toml.load(f)      # fetches toml file and creates a dictionary
    except (OSError, IOError) as e:
        # if pull-requests.toml hasnt been created yet calls sync and then reties to fetch
        print("ERROR: pull-requests.toml doesn't exist. Run 'git hub sync' and try again")
    open_dict = pr_dict['open pull requests']
    most_popular = most_active_prs_helper(open_dict)
    return most_popular


def most_active_prs_helper(prs):
    """helper function to find pull requests."""
    popular = []
    q = PriorityQueue()
    for pr_num in list(prs.keys()):  # find in last two weeks, not all time
        pr = prs[pr_num]
        recent_comment_count = recent_comments(pr)
        q.put(-recent_comment_count)

    most_comments = set()
    count = 0
    while q.qsize() != 0 and count != 3:
        most_comments.add(-q.get())
        count += 1
    most_comments.discard(0)  # removes 0 because don't want to have pr with 0 comments
    for pr_num in list(prs.keys()):
        pr = prs[pr_num]
        recent_comment_count = recent_comments(pr)
        if recent_comment_count in most_comments:
            popular.append(f'PR #{pr_num}: {pr["user"]}/{pr["branch"]}: {pr["title"]} -- {recent_comment_count} comment(s)')
    return popular


def recent_comments(pr):
    """counts how many comments in the last two weeks
    """
    count = 0
    comment_dates = pr['comment_dates']
    for date in comment_dates:
        comment_time = parse_time(date)
        if((datetime.now() - comment_time).days < 14):
            count += 1
    return count


def no_discussion():
    """Finds PRs that haven't seen any discussion. """
    try:
        path_prs = path_to_toml()
        f = open(path_prs, "r")
        pr_dict = toml.load(f)      # fetches toml file and creates a dictionary
    except (OSError, IOError) as e:
        # if pull-requests.toml hasnt been created yet calls sync and then reties to fetch
        print("ERROR: pull-requests.toml doesn't exist. Run 'git hub sync' and try again")
    open_dict = pr_dict['open pull requests']
    opened = no_discussion_helper(open_dict)
    return opened


def no_discussion_helper(prs):
    """helper function to find pull requests."""
    no_disc_prs = []
    for pr_num in list(prs.keys()):
        pr = prs[pr_num]
        if pr['comment_count'] == "0":
            print("this pr")
            print(pr['comment_count'])
            no_disc_prs.append(f'PR #{pr_num}: {pr["user"]}/{pr["branch"]}: {pr["title"]}')
    return no_disc_prs


def prs_with_me():
    """Finds PRs that I have commented on"""
    try:
        path_prs = path_to_toml()
        f = open(path_prs, "r")
        pr_dict = toml.load(f)      # fetches toml file and creates a dictionary
    except (OSError, IOError) as e:
        # if pull-requests.toml hasnt been created yet calls sync and then retries to fetch
        print("ERROR: pull-requests.toml doesn't exist. Run 'git hub sync' and try again")
    open_dict = pr_dict['open pull requests']
    opened = find_prs_with_me(open_dict)
    return opened


def find_prs_with_me(prs):
    """helper function to find pull requests."""
    prs_with_me = []
    for pr_num in list(prs.keys()):
        pr = prs[pr_num]
        if pr['self_comment'] == "True":
            prs_with_me.append(f'PR #{pr_num}: {pr["user"]}/{pr["branch"]}: {pr["title"]}')
    return prs_with_me


def unmergeable_prs():
    """Finds PRs that haven't seen any discussion. """
    try:
        path_prs = path_to_toml()
        f = open(path_prs, "r")
        pr_dict = toml.load(f)      # fetches toml file and creates a dictionary
    except (OSError, IOError) as e:
        # if pull-requests.toml hasnt been created yet calls sync and then reties to fetch
        print("ERROR: pull-requests.toml doesn't exist. Run 'git hub sync' and try again")
    open_dict = pr_dict['open pull requests']
    opened = find_unmergeable_prs(open_dict)
    return opened


def find_unmergeable_prs(prs):
    """helper function to find pull requests."""
    unmergeable_prs = []
    for pr_num in list(prs.keys()):
        pr = prs[pr_num]
        if pr['mergeable'] == "False":
            unmergeable_prs.append(f'PR #{pr_num}: {pr["user"]}/{pr["branch"]}: {pr["title"]}')
    return unmergeable_prs


def issues_no_comments():
    """Finds issues without any comments. """
    try:
        path_prs = path_to_toml()
        f = open(path_prs, "r")
        pr_dict = toml.load(f)      # fetches toml file and creates a dictionary
    except (OSError, IOError) as e:
        # if pull-requests.toml hasnt been created yet calls sync and then reties to fetch
        print("ERROR: pull-requests.toml doesn't exist. Run 'git hub sync' and try again")
    open_dict = pr_dict['issues']
    opened = find_issues_no_comments(open_dict)
    return opened


def find_issues_no_comments(issues):
    """helper function to find issues with no comments."""
    issues_no_comments = []
    for num in list(issues.keys()):
        issue = issues[num]
        if issue['comment_count'] == "0":
            print(issue['comment_count'])
            issues_no_comments.append(f'issue #{num}: {issue["title"]}')
    return issues_no_comments


def tickets_referred(comments):
    """finds tickets in comments of pull requests or issues
    """
    issues = []
    for comment in comments:
        if "#" in comment:
            tickets_referred = (re.findall(r"(#\d+)", comment))
            for ticket in tickets_referred:
                ticket = ticket[1:]
                issues.append(ticket)
    return issues


def closed_pr_refer_tickets():
    """Finds issues that are referred to from prs and other issues """
    try:
        path_prs = path_to_toml()
        f = open(path_prs, "r")
        pr_dict = toml.load(f)    # fetches toml file and creates a dictionary
    except (OSError, IOError) as e:
        # if pull-requests.toml hasnt been created yet calls sync and then reties to fetch
        print("ERROR: pull-requests.toml doesn't exist. Run 'git hub sync' and try again")
    closed = pr_dict['closed pull requests']
    issues = pr_dict['issues']
    issues_referred = find_closed_pr_refer_ticket(closed, issues)
    return issues_referred


def find_closed_pr_refer_ticket(closed_prs, issues):
    """helper function to find closed prs that reference open issues"""
    unresolved_issues = []
    for num in closed_prs:
        pr = closed_prs[num]
        referred_tickets = tickets_referred(pr['comment_content'])
        for ticket in referred_tickets:
            if ticket in issues:
                unresolved_issues.append(f'issue #{ticket}: {issues[ticket]["title"]}')
    return unresolved_issues


def popular_tickets():
    """tickets that are referred to many times"""
    try:
        path_prs = path_to_toml()
        f = open(path_prs, "r")
        pr_dict = toml.load(f)    # fetches toml file and creates a dictionary
    except (OSError, IOError) as e:
        # if pull-requests.toml hasnt been created yet calls sync and then reties to fetch
        print("ERROR: pull-requests.toml doesn't exist. Run 'git hub sync' and try again")
    opened = pr_dict['open pull requests']
    issues = pr_dict['issues']
    popular = find_popular_tickets(opened, issues)
    return popular


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
        for ticket in referred_tickets_in_tickets:
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
    # most_popular.remove(1) #is it considered popular if there is only one comment
    for ticket in list(tickets.keys()):
        if tickets[ticket] in popular_count:
            most_popular.append(f'issue #{ticket}: {issues[ticket]["title"]}')
    return most_popular
