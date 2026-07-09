# Sumi Fit App

## Local Development

### 1. Clone the repository

If you don't have an SSH key generated, you can use HTTPS. If you do have an SSH key, you can use SSH.

#### SSH

```sh
git clone git@github.com:tomdu3/sumi-fit.git
```

#### HTTPS

```sh
git clone https://github.com/tomdu3/sumi-fit.git
```

### 2. Navigate to the project directory

```sh
cd sumi-fit
```

### 3. Create a Python environment

We are using [uv](https://github.com/astral-sh/uv) to manage our Python environment. Having the `pyproject.toml` file in the root of the project will automatically create the virtual environment in a `.venv` folder. If you don't have `uv` installed, you can install it using `curl https://astral.sh/uv/install.sh | sh` or [pipx](https://pipx.pypa.io/). Note that the first time you run `uv sync`, it will take a while to install all the dependencies.

```sh
uv sync
```

### 4. Run the app

```sh
uv run main.py
```
