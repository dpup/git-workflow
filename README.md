# git-workflow

_Opinionated tools for managing a team based git workflow._


## Principles

- Local `master` is kept clean and relatively up to date with origin
- Avoid merge commits where possible
- Most work occurs in personal branches and are considered private (hence `push -f` is acceptable)


## Commands

### Start

`git start [feature]`

Pulls master and creates a new feature branch named `$USERNAME/feature`.

### Sync

`git sync [-i]`

Pulls master and rebases working branch.

### Pull Request

`git pull-request`

Opens a GitHub pull request for the current branch, using a templatable message and list of
reviewers who should be CCd on the request.

### Cleanup

`git cleanup`

Removes local and remote branches that have been merged into master.

### GitHub Login

`git github-login`

Prompts for GitHub username/password and requests a github auth token. Credentials
are stored in `~/.github-auth`.


## Prequisites

- Python 2.7
- Requests - `pip install requests`
- GitPython - `pip install gitpython`


## License

Licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).
