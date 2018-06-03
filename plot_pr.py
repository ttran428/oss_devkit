import json
import urllib
import dateutil.parser
from collections import OrderedDict
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.transforms import blended_transform_factory

import subprocess
import math
cache = '.git/git-hub/_pr_cache.txt'


def execute():
    def login():
        """Retrieves the user's remote.

        Returns
        -------
        username : string
            username of the remote
        repo : string
            repository of the remote
        remote : string
            returns remotes

        """
        process = subprocess.Popen(["git", "remote", "-v"], stdout=subprocess.PIPE)
        remotes = str(process.stdout.read())
        url = remotes.split(" ", 1)[0]  # gets the fetch url
        arguments = url.split(".com")[1]  # gets just the username/repo.git
        arguments = arguments[1:]
        arguments = arguments.split(".git")[0]  # takes out ".git"
        username, repo = arguments.split("/")
        return (username, repo)


    def fetch_PRs(user, repo, state='open'):
        """Pulls down all the information

        Parameters
        ----------
        user : string
            user's repo we are pulling from
        repo : string
            name of repo we are pulling from
        """
        params = {'state': state,
                  'per_page': 100,
                  'page': 1}

        data = []
        page_data = True

        while page_data:
            config = {'user': user,
                      'repo': repo,
                      'params': urllib.parse.urlencode(params)}

            fetch_status = ('Fetching page %(page)d (state=%(state)s)' % params +
                            ' from %(user)s/%(repo)s...' % config)
            print(fetch_status)

            f = urllib.request.urlopen(
                'https://api.github.com/repos/%(user)s/%(repo)s/pulls?%(params)s'
                % config
            )

            params['page'] += 1
            page_data = json.loads(f.read())

            if 'message' in page_data and page_data['message'] == "Not Found":
                page_data = []
                print('Warning: Repo not found (%(user)s/%(repo)s)' % config)
            else:
                data.extend(page_data)

        return data


    def seconds_from_epoch(dates):
        """Difference in times between dates given and the first PR.

        Parameters
        ----------
        dates : list
            list of times to compare against the first PR
        """
        seconds = [(dt - epoch).total_seconds() for dt in dates]
        return seconds


    def get_month_bins(dates):
        """Counts month_duration number of months back from current time.

        Parameters
        ----------
        dates : list
            list of times to compare against the first PR
        """
        now = datetime.now(tz=dates[0].tzinfo)
        this_month = datetime(year=now.year, month=now.month, day=1,
                              tzinfo=dates[0].tzinfo)
        bins = [this_month - relativedelta(months=i)
                for i in reversed(range(-1, month_duration+3))]
        return seconds_from_epoch(bins)


    def diff_month(d1, d2):
        """Finds the difference in months between two datetime objects

        Parameters
        ----------
        d1 : Datetime
            Second datetime object we are comparing
        d2 : Datetime
            Second datetime object we are comparing
        """
        return (d1.year - d2.year) * 12 + d1.month - d2.month

    def date_formatter(value, _):
        """Formats from seconds from epoch to YYYY/MM.

        Parameters
        ----------
        value : int
            Number of seconds from epoch
        """
        dt = epoch + timedelta(seconds=value)
        return dt.strftime('%Y/%m')

    # Try to either pull down or fetch from cache all the PRs
    try:
        PRs = json.loads(open(cache, 'r').read())
        print('Loaded PRs from cache...')

    except IOError:
        user, repo = login()
        PRs = fetch_PRs(user=user, repo=repo, state='closed')
        PRs.extend(fetch_PRs(user=user, repo=repo, state='open'))

        cf = open(cache, 'w')
        cf.write(json.dumps(PRs))
        cf.flush()
    nrs = [pr['number'] for pr in PRs]
    print('Processing %d pull requests...' % len(nrs))
    # All the dates a PR was created
    dates = [dateutil.parser.parse(pr['created_at']) for pr in PRs]

    # Finds all the release dates (tags)
    p = subprocess.run(["git", "log", "--tags", "--simplify-by-decoration", "--pretty='format:%ai %d'"], stdout=subprocess.PIPE)
    tag_dates = str(p.stdout.decode("utf-8").strip('\n'))
    releases = OrderedDict([])
    for release in tag_dates:
        if not 'tag' in release:
            continue
        date = release[:26]
        tag = release.split('tag: ')[1]
        tag = tag[:len(tag) - 2]
        releases.update({tag: date})
    # Formats all the release dates from strings to Datetime objects
    for r in releases:
        releases[r] = dateutil.parser.parse(releases[r])

    # How many months we want to plot, difference between first PR and now
    month_duration = abs(diff_month(min(dates), datetime.now(tz=dates[0].tzinfo)))

    # First PR
    epoch = min(dates)
    # The time between each PR and the first PR
    dates_f = seconds_from_epoch(dates)
    bins = get_month_bins(dates)
    bins.sort()
    fig, ax = plt.subplots(figsize=(7, 5))
    n, bins, _ = ax.hist(dates_f, bins=bins, color='blue', alpha=0.6)
    tick_space = math.ceil(diff_month(datetime.now(tz=dates[0].tzinfo), epoch)/10)

    ax.xaxis.set_major_formatter(FuncFormatter(date_formatter))
    ax.set_xticks(bins[0:-1:tick_space])
    ax.set_xlim(bins[0], bins[-1])

    labels = ax.get_xticklabels()
    for l in labels:
        l.set_rotation(40)
        l.set_size(10)

    mixed_transform = blended_transform_factory(ax.transData, ax.transAxes)

    for version, date in releases.items():
        date = seconds_from_epoch([date])[0]
        ax.axvline(date, color='black', linestyle=':', label=version)
        ax.text(date, 1, version, color='r', va='bottom', ha='center',
                transform=mixed_transform)

    ax.set_title('Pull request activity').set_y(1.05)
    ax.set_xlabel('Date')
    ax.set_ylabel('PRs per month', color='blue')

    cumulative = np.cumsum(n)
    cumulative += len(dates) - cumulative[-1]

    ax2 = ax.twinx()
    ax2.plot(bins[1:], cumulative, color='black', linewidth=2)
    ax2.set_ylabel('Total PRs', color='black')

    plt.tight_layout()
    fig.savefig('.git/git-hub/PRs.png')
