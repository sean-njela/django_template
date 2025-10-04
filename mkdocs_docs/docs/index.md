<div align="center">

  <!-- Row of icons -->
  <p>
    <img src="https://logo.svgcdn.com/l/django.svg" alt="Django" height="95"/>
  </p>

  <h1>Django Portfolio Template</h1>

  <p>
    A production-ready Django template for personal portfolio websites. It demonstrates a standardised project structure, containerised development environment, automated task runner, and documentation integration. It is designed to showcase projects, experience, and skills with minimal setup.
  </p>

  <p>
    <a href="https://github.com/sean-njela/django_template/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/sean-njela/django_template" alt="contributors" />
  </a>
  <a href="">
    <img src="https://img.shields.io/github/last-commit/sean-njela/django_template" alt="last update" />
  </a>
  <a href="https://github.com/sean-njela/django_template/network/members">
    <img src="https://img.shields.io/github/forks/sean-njela/django_template" alt="forks" />
  </a>
  <a href="https://github.com/sean-njela/django_template/stargazers">
    <img src="https://img.shields.io/github/stars/sean-njela/django_template" alt="stars" />
  </a>
  <a href="https://github.com/sean-njela/django_template/issues/">
    <img src="https://img.shields.io/github/issues/sean-njela/django_template" alt="open issues" />
  </a>
  <a href="https://github.com/sean-njela/django_template/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/sean-njela/django_template.svg" alt="license" />
  <a href="https://github.com/sean-njela/django_template/actions/workflows/ci.yml">
    <img src="https://github.com/sean-njela/django_template/actions/workflows/ci.yml/badge.svg" alt="CI" />
  <a href="https://github.com/sean-njela/django_template/actions/workflows/dependabot/dependabot-updates">
    <img src="https://github.com/sean-njela/django_template/actions/workflows/dependabot/dependabot-updates/badge.svg" alt="Dependabot" />
  <a href="https://github.com/sean-njela/django_template/actions/workflows/pages/pages-build-deployment">
    <img src="https://github.com/sean-njela/django_template/actions/workflows/pages/pages-build-deployment/badge.svg" alt="GH-Pages" />
  </a>
  </p>
</div>

## Tech Stack

> List of tools used in the project

[![Devbox](https://www.jetify.com/img/devbox/shield_moon.svg)](https://www.jetify.com/devbox/docs/contributor-quickstart/)
![Taskfile](https://img.shields.io/badge/Taskfile-3.44.0-green)
![gitflow](https://img.shields.io/badge/gitflow-1.12-green)
[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Prerequisites

!!! IMPORTANT
    This project uses **Devbox** to provide a consistent development environment.

1. **Install Docker**
   [Docker installation guide](https://docs.docker.com/get-docker/)

2. **Install Devbox**
   [Devbox installation guide](https://www.jetify.com/devbox/docs/installing_devbox/)

3. **Clone the repository**
   ```bash
   git clone ...
   cd ...

   sudo apt-get update
   sudo apt-get install -y libpq-dev python3-dev build-essential pkg-config
   ```

4. **Start Devbox shell**

   ```bash
   devbox shell
   ```

  > First run may take several minutes to install tools, but subsequent runs spin up in seconds.

## Quick Start

```bash
task setup
task status   # check if everything is running
task dev      # start development stack
task info     # to list urls to visit
task cleanup-dev
```

## Documentation

For full documentation, setup instructions, and architecture details, visit the [docs](mkdocs_docs/index.md) directory or run locally with:

```bash
task docs
```

Then open: [http://127.0.0.1:8030/]()

## Tasks (Automation)

!!! IMPORTANT
    This project is designed for a simple, one-command setup. All necessary actions are orchestrated through `Taskfile.yml`.

The `Taskfile.gitflow.yml` provides a structured Git workflow using Git Flow. This helps in managing features, releases, and hotfixes in a standardized way. To run these tasks just its the same as running any other task. Using gitflow is optional. If you do not want the gitflow tasks, you can remove the `Taskfile.gitflow.yml` file and unlink it from the `Taskfile.yml` file (remove the `includes` section). If you cannot find the section use CTRL + F to search for `Taskfile.gitflow.yml`.

To see all tasks:

```bash
task --list-all
```

## Contributing

<a href="https://github.com/sean-njela/django_template/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=sean-njela/django_template" />
</a>

> Contributions are welcome! Open an issue or submit a PR.

## License

Distributed under the MIT License. See `LICENSE` for more info.

## Contact

* [LinkedIn](https://linkedin.com/in/sean-njela)
* [Twitter/X](https://x.com/devopssean)
* [seannjela@outlook.com](mailto:seannjela@outlook.com)
* [About Me](mkdocs_docs/4-about/0-about.md)
