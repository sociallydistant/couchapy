# Contributing

Socially Distant welcomes ideas, pull requests, and feedback.  If you would like to contribute you can!

Before contributing, please read:

1. [The Development Process](docs/DEVELOPMENT_PROCESS.md);
1. [How to setup a development environment](docs/ENVIRONMENT_SETUP.md); and
1. The information below!

# How you can contribute

1. _Fixing problems_: If you find a problem, the most helpful thing you can do is open a pull request with detailed information on the problem and steps to reproduce it if possible.

1. _Contributing requested features_: If you see an issue for a new feature and would like to take a stab at it, please reply to the issue to express your intent before starting; we will assign the issue to you so that the remainder of the community is not working on the same request.  If you are unsure of what to do, please post questions!

1. _Contributing unsolicited features_: If you'd like to contribute features that you think is missing, please start by checking the issues page. There may already be a plan to add this feature! If not, open an issue yourself so that you can get feedback before you start developing. 

* _Writing documentation_: Documentation can always be improved.  If you see something wrong, or you believe you have a better way to explain a particular part of the documentation, please let us know your ideas!

## Making Your First Pull Request

First-time contributors are encouraged to choose issues that are labeled 
"needs owner" If you have questions, want a suggestion of what to work on, or would like help on your first contribution, please post in the issue you would like to work.

To get started:
1. Fork this repository (click "fork" on the repository's home page in GitHub)
1. Clone the forked repository with `git clone <your fork's url>` and create a
branch with `git checkout -b some-branch-name`. [See the development process documentation for branch naming nomenclature](docs/DEVELOPMENT_PROCESS.md#branch-nomenclature)
1. After you create a branch, immediately open a pull request, so that we can track your progress.  The pull request description should make reference to the Issue that you are working on. Choose `master` or `development` for the base and your branch name for `compare`, according to the [Development Workflow](docs/DEVELOPMENT_PROCESS.md#development-workflow)
1. Your PR will be reviewed by another contributor, and then either merged or have changes requested.

## Keeping your fork updated

As you tackle new Issues, you'll want to be sure that you always start by working
on the most recent code. To sync up your fork's  `master` with a parent repository's master, set an upstream and pull from it. For this to work, you should make sure you're always committing to a branch, not master.

```bash
git remote add upstream https://github.com/sociallydistant/couchapy.git
git checkout master
git pull upstream master
```

## Attribution

Portions of this contributing documentation has been adapted from the contributing guidelines prepared by the fine folks on the [Learning Team for EmberJS](https://github.com/ember-learn/guides-source/edit/master/CONTRIBUTING.md)
