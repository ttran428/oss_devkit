import os
import toml
import plot_pr
from queue import *
from datetime import datetime
from datetime import timedelta
from os.path import join as pjoin

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

def week_old_comments_helper(list_of_dictionaries):
    """Helper function that finds all PRs in a dictionary that are over a week old
    """
    all_prs = []
    for dictionary in list_of_dictionaries:
        for sub_keys in list(dictionary.keys()):
            sub_dictionary = dictionary[sub_keys]
            if(sub_dictionary['most_recent_comment'] == ""):
                #all_prs.append('PR #{0}: {1}/{2} {3}'.format(sub_keys, sub_dictionary['user'], sub_dictionary['branch'], sub_dictionary['comment']))
                all_prs.append(f'PR #{sub_keys}: {sub_dictionary["user"]}/{sub_dictionary["branch"]}: {sub_dictionary["comment"]}')
            else:
                comment_time = parse_time(sub_dictionary['most_recent_comment'])
                if((datetime.now() - comment_time).days > 7):
                    #all_prs.append('PR #{0}: {1}/{2} {3}'.format(sub_keys, sub_dictionary['user'], sub_dictionary['branch'], sub_dictionary['comment']))
                    all_prs.append(f'PR #{sub_keys}: {sub_dictionary["user"]}/{sub_dictionary["branch"]}: {sub_dictionary["comment"]}')
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
    hour, time = time.split(':',1)
    minute, time = time.split(':',1)
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

def oldest_prs_helper(dictionary):
    """Helper function that finds oldest prs"""
    oldest = []
    q = PriorityQueue(maxsize=3)
    old = timedelta()
    now = datetime.now()
    for prs in dictionary:
        for pr_num in list(prs.keys()):
            pr = prs[pr_num]
            if now-parse_time(pr['created_at']) > old:
                if q.qsize() == 3:
                    q.get()
                q.put(now-parse_time(pr['created_at']))
                old = q.get()
                q.put(old)

    for prs in dictionary:
        for pr_num in list(prs.keys()):
            pr = prs[pr_num]
            if now-parse_time(pr['created_at']) > old:
                days = str(now-parse_time(pr['created_at']))[:8]
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

def most_active_prs_helper(dictionary):
    """helper function to find pull requests."""
    popular = []
    q = PriorityQueue()
    for prs in dictionary:
        for pr_num in list(prs.keys()): #find in last two weeks, not all time
            pr = prs[pr_num]
            recent_comment_count = recent_comments(pr)
            q.put(-recent_comment_count)

    most_comments = {-q.get(), -q.get(), -q.get()}
    most_comments.discard(0) #removes 0 because don't want to have pr with 0 comments
    for prs in dictionary:
        for pr_num in list(prs.keys()):
            pr = prs[pr_num]
            recent_comment_count = recent_comments(pr)
            if recent_comment_count in most_comments:
                popular.append(f'PR #{pr_num}: {pr["user"]}/{pr["branch"]}: {pr["title"]} -- {recent_comment_count} comment(s)')
    return popular

def recent_comments(pr):
    #counts how many comments in the last two weeks
    count = 0
    comment_dates = eval(pr['comment_dates'])
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

def no_discussion_helper(dictionary):
    """helper function to find pull requests."""
    no_disc_prs = []
    for prs in dictionary: # is this just one dictionary
        for pr_num in list(prs.keys()):
            pr = prs[pr_num]
            if pr['comment_count'] == "0":
                no_disc_prs.append(f'PR #{pr_num}: {pr["user"]}/{pr["branch"]}: {pr["title"]}')
    return no_disc_prs

def prs_with_me():
    """Finds PRs that haven't seen any discussion. """
    try:
        path_prs = path_to_toml()
        f = open(path_prs, "r")
        pr_dict = toml.load(f)      # fetches toml file and creates a dictionary
    except (OSError, IOError) as e:
        # if pull-requests.toml hasnt been created yet calls sync and then reties to fetch
        print("ERROR: pull-requests.toml doesn't exist. Run 'git hub sync' and try again")
    open_dict = pr_dict['open pull requests']
    opened = find_prs_with_me(open_dict)
    return opened

def find_prs_with_me(dictionary):
    """helper function to find pull requests."""
    prs_with_me = []
    for prs in dictionary: # is this just one dictionary
        for pr_num in list(prs.keys()):
            pr = prs[pr_num]
            if pr['self_comment'] == "True":
                prs_with_me.append(f'PR #{pr_num}: {pr["user"]}/{pr["branch"]}: {pr["title"]}')
    return prs_with_me

def prs_with_me():
    """Finds PRs that haven't seen any discussion. """
    try:
        path_prs = path_to_toml()
        f = open(path_prs, "r")
        pr_dict = toml.load(f)      # fetches toml file and creates a dictionary
    except (OSError, IOError) as e:
        # if pull-requests.toml hasnt been created yet calls sync and then reties to fetch
        print("ERROR: pull-requests.toml doesn't exist. Run 'git hub sync' and try again")
    open_dict = pr_dict['open pull requests']
    opened = find_prs_with_me(open_dict)
    return opened

def find_prs_with_me(dictionary):
    """helper function to find pull requests."""
    prs_with_me = []
    for prs in dictionary: # is this just one dictionary
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

def find_unmergeable_prs(dictionary):
    """helper function to find pull requests."""
    unmergeable_prs = []
    for prs in dictionary: # is this just one dictionary
        for pr_num in list(prs.keys()):
            pr = prs[pr_num]
            if pr['mergeable'] == "False":
                unmergeable_prs.append(f'PR #{pr_num}: {pr["user"]}/{pr["branch"]}: {pr["title"]}')
    return unmergeable_prs