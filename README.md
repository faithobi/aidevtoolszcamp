# aidevtoolszcamp — Django TODO App

This repository contains a small Django project with a TODO app used for learning and experimentation.

## Setup

1. Install Python 3.11 or later.
2. Create a virtual environment and activate it:
```powershell
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\venv\Scripts\Activate.ps1
```
3. Install dependencies:
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Development server

Start the development server using the helper script (recommended):
```powershell
Use the `dev_start` wrapper to explicitly control whether your default browser opens:

```powershell
.\scripts\dev_start.ps1 -HostName 127.0.0.1 -Port 8000 -Open  # opens browser
.\scripts\dev_start.ps1 -HostName 127.0.0.1 -Port 8000       # does not open browser
```

Or call `start_server.ps1` directly to rely on its internal auto-open:

.\scripts\start_server.ps1 -HostName 127.0.0.1 -Port 8000
```
This will start the server, create `server.pid`, and write logs to `server.log` and `server.err.log`. It will also attempt to open your default browser to the server URL.

Stop the development server and cleanup logs with:
```powershell
.\scripts\stop_server.ps1
```

Or run Django commands directly in the venv:
```powershell
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

## Running tests

Run the Django unit tests:
```powershell
.\venv\Scripts\Activate.ps1
python manage.py test
```

## Notes
- Templates are located at `todo/templates/todo/` and use `base.html` and `home.html`.
- The `todo` app includes create/edit/delete/assign due dates and resolve (toggle) functionality.
- Additions and changes to the project should generally be run inside the `venv` virtual environment.

---

If you want additional features like validations, styling, or a full API, I can add them next.
