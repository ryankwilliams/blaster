# Changelog

All changes made to this project will be documented here.

When adding changes, please follow the standards at the link below:
https://keepachangelog.com/en/1.0.0/

## [0.2.0] - 2019-12-23
### Added
- Use bumpversion for making new releases
- Added changelog file

### Changed
- Updates to setuptools for packaging/distribution
- Consolidate common code across both parallel/sequential methods
- Makefile adjustments
- Some minor adjustments to project README.md

## [0.1.8] - 2018-05-02
### Fixed
- Do not process any more tasks if previous tasks fails. This is only when
  running tasks sequentially.

## [0.1.7] - 2018-04-17
### Changed
- This release provides the ability for users to define a delay between
  starting processes. By default this delay is 5 seconds.

## [0.1.6] - 2017-09-19
### Changed
- This release brings maintenance throughout all modules.

## [0.1.5] - 2017-08-30
### Added
- Ability to run a sequence of tasks in parallel or sequentially.

## [0.1.4] - 2017-08-23
### Added
- Added unit tests to gain code coverage.
- Travis CI enabled for all pushes to master branch or pull requests.
- Coveralls added to keep code coverage results per commits.

### Changed
- Updated doc strings for all modules.
- Updated README.md.

### Fixed
- Fix bug that was not allowing task method traceback to be saved when a
  failure happened.
- Fix bug that was not having blaster task id saved within each task.

## [0.1.3] - 2017-08-16
### Changed
- Ability to determine the number of processes to spawn when processing tasks.

## [0.1.2] - 2017-08-14
### Changed
- This release brings an updated package structure and fine tunes the core
  classes.

## [0.1.1] - 2017-08-04
### Fixed
- Ensure potential task configuration updates during process run are returned.

## [0.1.0] - 2017-08-03
### Added
- Initial release.