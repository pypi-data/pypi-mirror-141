# CHANGELOG

## 0.2.1

### Bugfix

- [version-bump] - required for github automatic workflows

## 0.2.0

### New Features

- [command] - new command `ingeniictl infra destroy`

### Improvements

- [refactor] - simplify pulumi commands, improve DRY in the codebase

## 0.1.2

### Improvements

- [disable-resource-protection] - adding `--pulumi-locks-only` and `--cloud-locks-only` options.

## 0.1.1

### Bugfix

- [disable-resource-protection] - add a missing `cwd` variable to the pulumi destroy command.

## 0.1.0

### New Features

- [command] - new command `ingeniictl infra disable-resource-protection`