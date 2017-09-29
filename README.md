# git-workflow

_Opinionated tools for managing a team based git workflow._


## Principles

- Local `master` is kept clean and relatively up to date with origin
- Avoid merge commits where possible
- Most work occurs in personal branches and are considered private (hence `push -f` is acceptable)

## Prequisites

Have Python 2.7 or Python 3.6.

Install requirements:

`pip install -r requirements.txt`

Add this folder to your path, so `git` can pick up the scripts.


## Commands

### Start

**Pulls master and creates a new feature branch named `$USERNAME/feature`.**

`git start [feature]`


### Sync

**Pulls master and rebases working branch.**

`git sync [-i]`

This is useful to avoid your changes being interleaved with other commits.
For example, say you were coding in your branch and made the changes `A, B, C`.
If you merge with master the commit history may now be `W, A, X, Y, B, Z, C`.
Leaving the history like this can make it harder to rollback a logical set of
changes in one go.  Using rebase, you will replay your commits on the end of
master, resulting in `W, X, Y, Z, A, B, C`.

Often it makes sense to make a lot of changes locally, that you wouldn't
necessarily want to push together, in cases like this you can use
`git sync -i` to interactively rebase your changes  and squash some commits.
This can result in a commit history showing `W, X, Y, Z, D`.

Much cleaner, right? But do be careful that you understand what is going on as
rebase can both squash and remove commits.

### Sync All

**Pulls master and rebases all local branches.**

`git sync-all`

### Pull Request

**Opens a GitHub pull request for the current branch**

`git pull-request`


### Cleanup

**Removes local and remote branches that have been merged into master.**

`git cleanup`


### GitHub Login

**Requests GitHub credentials to be used by other scripts**

`git github-login`

Prompts for GitHub username/password and optional OTP password, then requests a
github auth token. Credentials are stored in `~/.github-auth`.


## License

Licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).
