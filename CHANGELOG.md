# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [v0.1.2] - 2024-07-28

### Chore

* chore: update precommit hooks, exclude `CHANGELOG.md` from spellchecking. ([`491a0c1`](https://github.com/tom65536/annual/commit/491a0c1a5eb025a868ad404dc24a466c52626204))

### Ci

* ci: pin version of codacy uploader. ([`4cd9c23`](https://github.com/tom65536/annual/commit/4cd9c23c0d07748d64831aa93bee8b5fe3862e95))

* ci: create xml coverage report ([`43e06cf`](https://github.com/tom65536/annual/commit/43e06cfe362c2060d70f389d877d3e1b19aa2486))

* ci: add token to codacy action ([`64457bb`](https://github.com/tom65536/annual/commit/64457bb7462be20545c43ec96eb45268736d3c96))

### Fix

* fix: set build command for semantic release ([`6098ddc`](https://github.com/tom65536/annual/commit/6098ddc9f2ccfa7a7bcf5752f846109981cd1360))

* fix: coverage path configuration ([`921441c`](https://github.com/tom65536/annual/commit/921441cbd7319b725fcc78b316ac2d98b17c125f))

### Unknown

* Merge pull request #21 from tom65536/11-add-code-coverage

fix: set build command for semantic release ([`4d275c8`](https://github.com/tom65536/annual/commit/4d275c8f66bd816eb6fb6d825e4ccb0d4a598fa9))

* doc: add coverage badge ([`3f26ab7`](https://github.com/tom65536/annual/commit/3f26ab73eb35dc239dca9067cdbfed183814f714))
## [v0.1.1] - 2024-07-28

### Ci

* ci: pin version of codacy uploaer. ([`d151a7c`](https://github.com/tom65536/annual/commit/d151a7c4a31340e80e7f48b411fbf92a7f809297))

* ci: create xml coverage report ([`458394e`](https://github.com/tom65536/annual/commit/458394e4f9b4a5ebded1128586d8395b8a13eeb0))

* ci: add token tocodacy action ([`f1531e9`](https://github.com/tom65536/annual/commit/f1531e964fbc06400876b860812405ffc015e025))

* ci: add coverity upload ([`4bcd7d3`](https://github.com/tom65536/annual/commit/4bcd7d36d0fd6b665fd126625a84c7535949006f))

* ci: Add deployment to pypi to workflow. (#8) ([`0e2007a`](https://github.com/tom65536/annual/commit/0e2007a3fbfa35c613031fa6aa6d7e676d6327ac))

### Documentation

* docs: fix requirements for readthedocs (#17)

Closes #16 ([`f901716`](https://github.com/tom65536/annual/commit/f9017168fe9c1e5640d955c4ff44aca3f366c17b))

### Fix

* fix: coverage path configuration ([`a3983b3`](https://github.com/tom65536/annual/commit/a3983b3c908d9ecbaceef33cbfa83975bf6a85b1))

### Unknown

* Merge pull request #20 from tom65536/11-add-code-coverage

fix: coverage path configuration ([`4f9d508`](https://github.com/tom65536/annual/commit/4f9d5080fce1c020e1a2236f4985bff3bb0e479b))

* Merge pull request #19 from tom65536/11-add-code-coverage

feat: add coverity upload ([`84e1ede`](https://github.com/tom65536/annual/commit/84e1ede4051ced2e1f45c4a849b8a55029175a00))

* doc: add coverage badge ([`15be575`](https://github.com/tom65536/annual/commit/15be575db57daf20da582607b219d4d3c8eba7c6))

* 12 add easter date (#18)

feat: add easter algorithms

* add `date_function` decorator and registry.
* add easter date

Issue #12 ([`88d1878`](https://github.com/tom65536/annual/commit/88d1878bad9b649d58e8a6dd1c244aaa867f7102))

* 9 improve documentation (#10)

* doc: add API docs with sphinx and autoapi.

* feat: add BDD tests.

* docs: add gherkin files to documentation.

* test: add doctests (modules)

* fix: fix mypy and flake warnigs.

* doc: add basic documentation files.

* docs: improve Introduction

* fix: correct style in docs/source/conf.py

* fix: fix format in issue template

* ci: pin versions of actions

* feat: add readthedocs.yaml

* ci: quality issues

* docs: updatecuser&#39;s giude

* fix: remove unnecessary flake8 exceptions ([`b168c4d`](https://github.com/tom65536/annual/commit/b168c4dba56b6b3dcca554602e8c128ffe237e5b))

* Update issue templates ([`ae20ea1`](https://github.com/tom65536/annual/commit/ae20ea140e21d6dd9e2380df926f3fc7a31f5ded))
## [v0.1.0] - 2024-06-26

### Chore

* chore: add unit tests ([`a9146b9`](https://github.com/tom65536/annual/commit/a9146b9c57321c9ec1ed90be6f2ca9a1dbe46bd1))

* chore: initial commit ([`ae56c8c`](https://github.com/tom65536/annual/commit/ae56c8ceccbb9488bef3f2ce59b2e87457ea2935))

### Feature

* feat: add year conditions ([`21ee930`](https://github.com/tom65536/annual/commit/21ee9306671bac32b4db7ca598afd9ca45fd9767))

* feat: add conditions ([`f798dee`](https://github.com/tom65536/annual/commit/f798deebea9d3978aea27316469a649085d8a8cf))

* feat: implement ruleparser ([`2e27d12`](https://github.com/tom65536/annual/commit/2e27d12d0f0fc3330e775662f532347b4c239289))

* feat: implement transformer [WIP] ([`3b76398`](https://github.com/tom65536/annual/commit/3b76398b78db2efd418e91445dfb5e844a7e4ae0))

* feat: add rule parser ([`3856946`](https://github.com/tom65536/annual/commit/3856946d279776907b530275d98a46e54adaa8d0))

### Fix

* fix: fixes weekday calculation ([`a00e9ad`](https://github.com/tom65536/annual/commit/a00e9add5b05e6de7d43b506a6d9077fa3cc7192))

### Style

* style: fix linter warning ([`6a7a372`](https://github.com/tom65536/annual/commit/6a7a372eeb2c4468f73b9d6c8154853d9a92f1d7))

### Unknown

* Adds release pipeline using python semantic release. (#5)

* chore: Adds release pipeline using python semantic release.

Close #4

* fix: Fix formatting issue in CI workflow. ([`98a6541`](https://github.com/tom65536/annual/commit/98a654102863095fe401307da16d905ad0d30691))

* Add basic CI/CD (#3)

* chore: add commitizen pre-commit hook

* chore: update tool versions
ß

* chore: update tool versions

* chore: update python version in CI

* style: adapt to stylesheet

* chore: add gitattributes ([`3e15b62`](https://github.com/tom65536/annual/commit/3e15b629a9039bfa4d58772fdf1c00692be8e092))

* Update README.md ([`04fa24d`](https://github.com/tom65536/annual/commit/04fa24d82d046868f9cb90db987f8fa18366f850))

* Update pyproject.toml ([`00e16ac`](https://github.com/tom65536/annual/commit/00e16ac1c56afdf71d1bc10c65e885134992892f))

* Initial commit ([`4f4ce28`](https://github.com/tom65536/annual/commit/4f4ce28db4c22914f2ac50b77d5ba311915c80be))
