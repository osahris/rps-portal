# RPS Relase Checklist

Reminder: You don't need to rigidly follow this checklist. It's just a guide to help you remember the steps that need to be taken. Feel free to modify the list as you see fit. But please make sure you add or modify any steps that will be required in future releases.

TODO: Automate most of those steps

## Prepare the release branch

- [x] Create a new branch from `dev` named `release/v$version`, e.g. `release/v2.0.0`
- [x] Merge `main` into the release branch
- [ ] Add an entry in `CHANGELOG.md` with all important changes since the last release

## Pin upstream artifact versions

- [ ] Pin budibase upstream image version in `roles/budibase/defaults/main.yml`

TODO: Add other roles

## Review all changes since the last release

- [ ] Review all changes since the last release with `git diff main..release/v$version`
- [ ] Create a merge request from the release branch into `main` called `Release v$version`

## Do the release

- [ ] Merge the release branch into `main`
- [ ] Tag the release with the version number, format `v$version`, e.g. `v2.0.0`

## Bring release changes back to dev

- [ ] Merge `main` into `dev`
- [ ] Add a new entry in `CHANGELOG.md` for the next release called `Unreleased`
- [ ] Uncheck all items in this release checklist in `release.SOP.md`

## Change artifact versions back to track latest and development versions

- [ ] Change budibase upstream image version in `roles/budibase/defaults/main.yml` back to `latest`

TODO: Add other roles
