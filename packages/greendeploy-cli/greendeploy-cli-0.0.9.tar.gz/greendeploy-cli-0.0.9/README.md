# GreenDeploy

GreenDeploy is a framework that makes it easy to build Dockerized Django projects
by providing uniform templates.

This is mostly a cli software.

## how to update PyPi

```
python setup.py sdist bdist_wheel
twine check dist/*
rm dist/package-name-slug-<previous-tag>*
rm dist/snake_package_name-<previous-tag>*
twine upload --skip-existing --repository-url https://test.pypi.org/legacy/ dist/*

twine upload --skip-existing dist/*
```

```
cd {{ cookiecutter.full_path_to_your_project }}{{ cookiecutter.project_slug }}

{{ cookiecutter.full_path_to_pyenv }}/versions/3.8.12/bin/python3.8 -m venv {{ cookiecutter.full_path_to_venv }}{{ cookiecutter.project_slug }}-py3812

source {{ cookiecutter.full_path_to_venv }}{{ cookiecutter.project_slug }}-py3812/bin/activate

python -m pip install --upgrade "{{ cookiecutter.pip_version }}"

pip install pip-tools "{{ cookiecutter.pip_tools_version }}"

git init .

git add .
git commit -m '🎉 Initial commit'
git tag -a v0.0.0 -m '🔖 First tag v0.0.0'

pip-compile

pip-sync

pip install -e .
```

Now run

```
python -m {{ cookiecutter.project_slug }}
```

## Release Schedule

1. py3.8 will be on `to-be-frozen` status starting 2022-10. This serves as a 1 year countdown to `frozen` status where it will no longer be supported
2. py3.8 will be supported till 2023-10 after which it will be on `frozen` status and removed from main brach and no longer supported.
3. py3.9 will be on `to-be-frozen` status starting 2023-10. This serves as a 1 year countdown to `frozen` status where it will no longer be supported

So the full schedule for this package is

| Python | add | `to-be-frozen` status | `frozen` status and stop supporting | PSF start release | PSF stop full support | PSF stop security fix |
|---|---|---|---|---|---|---|
| 3.8 | since package inception | 2022-10 | 2023-10 | 2019-10 | 2021-05 | 2024-10 |
| 3.9 | since package inception | 2023-10 | 2024-10 | 2020-10 | 2022-05 | 2025-10 |
| 3.10 **(latest)** | since package inception | 2024-10 | 2025-10 | 2021-10 | 2023-05 | 2026-10 |
| 3.11 *(preview)* | 2023-04 |2025-10 | 2026-10 | 2022-10 | 2024-05 | 2027-10 |
