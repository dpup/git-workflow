
import json
import getpass
import os.path


BOLD      = '\033[1m'
ITALIC    = '\033[3m'
UNDERLINE = '\033[4m'

RED     = '\033[31m'
GREEN   = '\033[32m'
YELLOW  = '\033[33m'
BLUE    = '\033[34m'
MAGENTA = '\033[35m'
CYAN    = '\033[36m'

RESET = '\033[0m'

def fatal_if_dirty(repo):
    """
    Checks whether there are pending changes and exits the program if there are.
    """

    info('Checking for pending changes')
    if repo.is_dirty():
        warn('You have uncommitted changes, proceeding automatically would be dangerous.')
        print(repo.git.status('-s'))
        exit(1)

def update_master(repo, initial_branch):
    """
    Switches to the master branch and pulls from origin. If an exception occurs
    it switches back to the initial branch and exits.
    """

    info('Switching to master branch')
    try:
        repo.heads.master.checkout()
    except:
        fatal('Could not checkout master.')
    info('Pulling updates for master branch')
    try:
        repo.git.remote('update', '--prune')
        repo.remotes.origin.pull('--no-tags')
    except:
        warn('Failed to update master')
        initial_branch.checkout()
        exit(1)

def get_auth_filename():
    """
    Returns the full path to ~/.github-auth.
    """

    return os.path.join(os.path.expanduser('~'), '.github-auth')


def get_github_creds():
    """
    Returns a dict containing GitHub auth details. Exits with an error if the
    file does not exist.
    """

    with open(get_auth_filename()) as auth_file:
        return json.load(auth_file)


def prompt(msg, default='', password=False):
    """
    Wrapper around raw_input and getpass.getpass.
    """

    suffix = ''
    if default != '':
        suffix = '[%s] ' % default
    msg = '%s: %s' % (msg, suffix)
    try:
        if password:
            answer = getpass.getpass(msg)
        else:
            answer = raw_input(msg)
    except KeyboardInterrupt:
        # Allow Ctrl-C exit at this point without barfing up an exception.
        print()
        exit(1)
    except:
        raise

    if answer == '':
        return default
    return answer


def fatal(msg, code=1):
    """
    Primts a red error message and then exits the program.
    """

    print(RED + BOLD + msg + RESET)
    exit(code)


def info(msg):
    """
    Prints an info message in blue.
    """
    print(BLUE + ITALIC + '> ' + msg + RESET)


def success(msg):
    """
    Prints a  message in green.
    """
    print(GREEN + '> ' + msg + RESET)



def warn(msg):
    """
    Prints a warning in yellow.
    """
    print(YELLOW + '> ' + msg + RESET)
