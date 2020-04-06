# TL;DR;

1. The `master` branch is the single source of truth for **current** MAJOR or MINOR versions, with PATCH versions for the current MAJOR or MINOR release.
1. The `development` branch is the single source of truth for the **next** MAJOR or MINOR version.
1. Versions are tracked with [Releases](https://github.com/sociallydistant/couchapy/releases).
1. This repo follows a defined development process.

# OVERVIEW

The overall purpose of defining this process is to improve the development processes for Couchapy.  The intent is to:

1. Simplify the organization of the respository;
1. Enhance the development workflow; and
1. Simplify usage of the repository for non-technical persons.

# Branch Organization

The repo will consist of various branches that serve defined purposes, which are broken into categories. The categories are:

1. **Master**. There only exists a single master branch. The master branch is the branch that is considered the stable, current code for release of product versions and rebasing if required. The master branch will be the base branch for the `development` branch, and a new MINOR release as a result of patching bug fixes, security vulnerabilities, and dependency updates, for the current version of the app as released to the public.  GitHub Tags and Releases will be used to identify critical points in the commit history, such as releases.

1. **Development**. There only exists a single development branch. The development branch is the base branch for current ongoing development work that will result in a **new** MAJOR or MINOR release, and will be the target branch for all pull requests that are considered complete but will not result in an imminent release.

1. **Working Branches**. The majority of branches created will be working branches. Working branches are merged into the appropriate branch when the code is considered complete and it has been reviewed. After a branch has been merged via a pull request, and work on the branch is considered complete, it will be deleted. Working branches are created for specific purposes such as:
   1. Fixing bugs and security vulnerabilities;
   1. Developing new functionality;
   1. Refactoring code; or
   1. Testing.

1. **Bot Branches**.  Bot branches are created automatically by automation and productivity bots, such as Dependabot, which continuously monitors the dependencies of the application and opens pull requests automatically.  These branches are created and managed automatically, or manipulated through bot commands using Git Mentions.

# Branch Nomenclature
Meaningful names are an important part of the development process, and in particular the maintenance of a repository.  Thus,
branch names will follow a standard naming convention that emphasize purpose and conciseness.

**Master branch conventions:**

1. The master branch will be named: *master*

**Development branch conventions:**
1. The development branch will be named: *development*

**Working branch conventions:**
1. Names will consist of only lowercase letters (a-z), numbers (0 - 9), hyphens ( - ), and underscores ( _ )
1. Names will begin with a single word, followed by a hyphen (-), from the following list:
   1. bugfix;
   1. feature;
   1. refactor;
   1. testing; and rarely
   1. other;
1. Names will be concise and should not exceed five (5) words, connected with underscores ( _ ); and
1. Names will be chosen that are representative of the purpose of the working branch and task.

Working branch name examples:
1. bugfix-some_issue_keywords;
1. feature-new_cool_feature;
1. refactor-some_important_thing;
1. testing-new_concept;
1. other-security_for_x

**Bot branch conventions:***
1. Although these branches are technically working branches, they can have branch nomenclature that deviates from the pattern defined above.  These branches are managed separately using interfaces that are specific to each bot or productivity tool, but typically through Git Mentions.

# Versioning
Versioning is an important aspect of maintaining a historical record of changes to the application.  

1. The version will be defined in [setup.py](https://github.com/sociallydistant/couchapy/blob/master/setup.py). This version number will follow the spirit of [Semantic Versioning](https://semver.org).  
1. Changes to the code base that are considered stable for release will result in the creation of a GitHub Release Tag;

# Development Workflow

1. The `master` branch is the basing point for all bug fixes and other work targetting a current release that will result in a PATCH release;
1. The `development` branch is for ongoing work that will result in a new MAJOR or MINOR release;
1. Working branches will be based from either `master` or `development`, depending on the purpose of the working branch:
   1. For working branches that target bug fixes, or minor changes to a release, the `master` branch will be the base;
	 1. For working branches that target new features, bug fixes, or minor changes to an upcoming MAJOR or MINOR release, the `development` branch will be the base.
1. Merges into the Master branch represent either full or partial PATCH versions, which may or may not trigger version changes in [setup.py](https://github.com/sociallydistant/couchapy/blob/master/setup.py); specifically, a PATCH version may include several changes, updates, and bug fixes that are sourced from several merged Pull Requests.  
1. Merges into the `development` branch represent code that is largely complete and considered stable for beta testing;
1. When a version change in [setup.py](https://github.com/sociallydistant/couchapy/blob/master/setup.py) is made, a change log will be provided that indicates changes made from the previous version;

# Commit Messages, Pull Requests, and Change Log

Commit messages, pull requests, and change logs are all useful tools for maintaining a mature code base.  Together, they allow developers and users to view changes to the code from different perspectives.

The following guiding principles apply to commit messages, pull requests, and the change log:

1. Commit messages are for developer consumption to track specific changes to code, which may have no contextual meaning for the purpose of generating a change log.
1. Since all code will be introduced into either `master` or `development` through Working Branches, pull requests will be used consistently.  As part of merging Pull Requests, there will be an accurate and descriptive overview of what each Pull Request represents.
1. Merge names, and optionally commits, will be prefixed with a tag that indicates what the pull request is for, for the purpose of generating a change log.  Valid prefixes are enclosed in square brackets:
   1. [BUILD]. Changes related to the build system (involving scripts, configurations or tools) and package dependencies;
	 1. [CI]. Changes related to the continuous integration and deployment system - involving scripts, configurations or tools
	 1. [DOCS]. Documentation changes related to the project - whether intended externally for the end users (in case of a library) or internally for the developers
	 1. [FEAT]. Changes related to new abilities or functionality.
	 1. [FIX]. Changes related to fixing bugs or minor requested changes.
	 1. [REFACTOR].  Changes related to modifying the codebase, which neither adds a feature nor fixes a bug - such as removing redundant code, simplifying the code, renaming variables, etc.
	 1. [LINT]. Changes related to styling of the code or cleanup as a result of linters.
	 1. [TEST]. Changes related to test code.
