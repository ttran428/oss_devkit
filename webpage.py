import os
import toml
from datetime import datetime
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
    print("main function")
    try:
        path_prs = path_to_toml()
        f = open(path_prs, "r")
        pr_dict = toml.load(f)      # fetches toml file and creates a dictionary
    except (OSError, IOError) as e:
        # if pull-requests.toml hasnt been created yet calls sync and then reties to fetch
        print("ERROR: pull-requests.toml doesn't exist. Run 'git hub sync' and try again")
    open_dict = pr_dict['open pull requests']
    opened = find_week_old_comments(open_dict)
    return opened

def find_week_old_comments(list_of_dictionaries):
    """Helper function that finds all PRs in a dictionary that are over a week old
    """
    print("helper function")
    all_prs = []
    for dictionary in list_of_dictionaries:
        for sub_keys in list(dictionary.keys()):
            sub_dictionary = dictionary[sub_keys]
            if(sub_dictionary['most_recent_comment'] == ""):
                all_prs.append('PR #{0}: {1}/{2} {3}'.format(sub_keys, sub_dictionary['user'], sub_dictionary['branch'], sub_dictionary['comment']))
            else:
                comment_time = parse_time(sub_dictionary['most_recent_comment'])
                if((datetime.now() - comment_time).days > 7):
                    all_prs.append('PR #{0}: {1}/{2} {3}'.format(sub_keys, sub_dictionary['user'], sub_dictionary['branch'], sub_dictionary['comment']))
    return all_prs

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
    opened = find_no_discussion(open_dict)
    return opened

def find_no_discussion(dictionary):
    """helper function to find pull requests."""
    no_disc_prs = []
    for prs in dictionary: # is this just one dictionary
        for pr_num in list(prs.keys()):
            pr = prs[pr_num]
            if pr['comment_count'] == "0":
                no_disc_prs.append(f'PR #{pr_num}: {pr["title"]} from {pr["user"]}/{pr["branch"]}') 
    return no_disc_prs

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