
import json
import getpass
import os.path
import os
import sys
import signal
import subprocess
import tempfile
import logging

logging.basicConfig(format='%(message)s', level=logging.INFO)

# Silences Traceback on Ctrl-C
signal.signal(signal.SIGINT, lambda x,y: os._exit(1))

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
		info(repo.git.status('-s'))
		exit(1)

def update_master(repo, initial_branch):
	"""
	Switches to the master branch and pulls from origin. If an exception occurs
	it switches back to the initial branch and exits.
	"""

	info('Switching to master branch')
	try:
		repo.heads.master.checkout()
	except BaseException as e:
		fatal('Could not checkout master: %s' % e)
	info('Pulling updates for master branch')
	try:
		repo.git.remote('update', '--prune')
		repo.remotes.origin.pull('--no-tags')
	except BaseException as e:
		warn('Failed to update master: %s' % e)
		initial_branch.checkout()
		c = prompt_y_n('Continue anyway?')
		if not c:
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

	fn = get_auth_filename()
	if not os.path.isfile(fn):
		fatal("Missing GitHub credentials. Did you run `git github-login`?")
	with open(fn) as auth_file:
		return json.load(auth_file)

def get_script_path():
	"""
	Returns the location of the current script.
	"""

	return os.path.dirname(os.path.realpath(sys.argv[0]))

def get_editor(repo):
	"""
	Returns the editor from env vars.
	"""

	return (repo.git.config("core.editor") or
               os.environ.get("GIT_EDITOR") or
	       os.environ.get("VISUAL") or
	       os.environ.get("EDITOR", "vi"))


def edit(repo, text):
	"""
	Opens the user's editor with predefined text and returns the edited copy.
	"""

	(fd, name) = tempfile.mkstemp(prefix="git-workflow-", suffix=".txt", text=True)
	try:
		f = os.fdopen(fd, "w")
		f.write(text)
		f.close()

		cmd = "%s \"%s\"" % (get_editor(repo), name)
		rc = subprocess.call(cmd, shell=True)
		if rc:
			fatal('Edit failed (%s)' % cmd)
		f = open(name)
		t = f.read()
		f.close()
	finally:
		os.unlink(name)
	return t

def prompt(msg, default='', password=False):
	"""
	Wrapper around raw_input and getpass.getpass.
	"""

	suffix = ''
	if default != '':
		suffix = '[%s] ' % default
	msg = '%s: %s' % (msg, suffix)
	if password:
		answer = getpass.getpass(msg)
	else:
		# raw_input in python2, input in python3
		try:
			answer = raw_input(msg)
		except NameError:
			answer = input(msg)
	return answer or default


def prompt_y_n(msg, default=False):
	"""
	Prompt user with given message for a yes/no answer (returning a boolean).
	If user hits 'enter' w/o supplying an answer, return 'default' value.
	"""

	suffix = ' [y/N]'  # default answer is 'No'
	if default:
		suffix = ' [Y/n]'  # default answer is 'Yes'

	answer = prompt(msg + suffix)

	if answer.lower() in ['y', 'yes']:
		return True
	elif answer == '':
		return default
	else:
		return False


def fatal(msg, code=1):
	"""
	Prints a red error message and then exits the program.
	"""

	error(msg)
	sys.exit(code)


def error(msg):
	"""
	Prints a red error message.
	"""

	logging.error(RED + BOLD + msg + RESET)


def info(msg):
	"""
	Prints an info message in blue.
	"""
	logging.info(BLUE + ITALIC + '> ' + msg + RESET)


def success(msg):
	"""
	Prints a  message in green.
	"""
	logging.error(GREEN + '> ' + msg + RESET)



def warn(msg):
	"""
	Prints a warning in yellow.
	"""
	logging.warning(YELLOW + '> ' + msg + RESET)
