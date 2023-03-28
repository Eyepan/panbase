# Panbase

A free-for-all open-source Backend-Base-As-A-Service project I took up to actually learn how BBaaSses work. Made with 💙 by [EyePan](https://github.com/eyepan)

# Download and run:

Panbase is soon to be available in a release format. Until then, you can build it yourself using the instructions below.

## Build Locally:

-   Clone this repository

```powershell
git clone https://github.com/eyepan/panbase.git
```

-   Create a virtual environment and download all `pip` packages

```powershell
python3 -m venv venv
pip install -r requirements.txt
```

-   Create a `config.py` file with the following contents:

```python
import sys


LOG_LEVEL = "DEBUG" if '--debug' in sys.argv else "CRITICAL"
API_PORT = 8000
ADMIN_PORT = 9000
RELOAD = True if '--reload' in sys.argv else False
JWT_SECRET = "supersecretjwtsecret"


```

-   Go to the UI folder and download all the `npm` packages

```powershell
cd ui
npm install
```

-   Build the admin UI using `vite`

```powershell
npm run build
```

-   Go back and run the build command with `nuitka`:

```powershell
cd ..
del database.db
python main.py --debug --init
python -m nuitka main.py --output-dir=dist --onefile --standalone -o panbase.exe --quiet --remove-output --show-progress --include-data-file=database.db=database.db --include-data-dir=admin-ui/dist=admin-ui/dist --onefile-tempdir-spec="%TEMP%\panbase\0.1.0"
```

The `--onefile-tempdir` flag is enabled in `Nuitka` to not create a new temp directory everytime the built executable runs. This will throw an warning saying

```diff
-Not using any variables for '--onefile-tempdir-spec' should only be done if your program absolutely needs to be in the same path always
```

This is **ABSOLUTELY FINE** and is totally expected. Don't panic.

## Run Without Building:

-   Create a virtual environment and download all `pip` packages

```powershell

python3 -m venv venv
pip install -r requirements.txt

```

-   Create a `config.py` file with the following contents:

```python
import sys

LOG_LEVEL = "DEBUG" if '--debug' in sys.argv else "CRITICAL"
API_PORT = 8000
ADMIN_PORT = 9000
RELOAD = True if '--reload' in sys.argv else False
JWT_SECRET = "super_secret_jwt_secret"

```

-   Go to the UI folder to download and install all `npm` packages

```powershell

cd UI
npm i
npm run dev
```

-   Come back to the root folder and run

```powershell
cd ..
python main.py --debug
```

Alternatively, you can also use `uvicorn` to run it directly, although you might have to set up the ports yourself.

```powershell
uvicorn main:app --reload
```

NOTE: `--debug` can also be swapped out for `--verbose`:
|Flag|Meaning|
|-|-|
|`--debug`/ `-d`| Shows debugging information. Sets `log_level` to DEBUG. Also shows the SQL Queries that are actually run|
|`--init`| Just initializes the database.db file. Used during building with `Nuitka` |
