# Zono-Full-Release
This is the full release of Zono on github here! Look below on how to start the bot.

# Hosting
Want to host this bot? Download all files and upload them onto https://replit.com. Then go on the project **Secrets** tab. On that tab, add a new secret named "DiscordToken" and set the value to the token of you bot. Then open your **.replit** file and make sure it looks like this:

```# The command that runs the program. Commented out because it is not run when the interpreter command is set
# run = ["python3", "main.py", "alive.html"]
# The primary language of the repl. There can be others, though!
language = "python3"
# The main file, which will be shown by default in the editor.
entrypoint = "main.py"
# A list of globs that specify which files and directories should
# be hidden in the workspace.
hidden = ["venv", ".config", "**/__pycache__", "**/.mypy_cache", "**/*.pyc"]

# Specifies which nix channel to use when building the environment.
[nix]
channel = "stable-21_11"

# Per-language configuration: python3
[languages.python3]
pattern = "**/*.py"
# Tells the workspace editor to syntax-highlight these files as
# Python.
syntax = "python"

  # The command needed to start the Language Server Protocol. For
  # linting and formatting.
[languages.python3.languageServer]
start = "pylsp"

# The command to start the interpreter.
[interpreter]
  [interpreter.command]
  args = [
    "stderred",
    "--",
    "prybar-python3",
    "-q",
    "--ps1",
    "\u0001\u001b[33m\u0002\u0001\u001b[00m\u0002 ",
    "-i",
  ]
  env = { LD_LIBRARY_PATH = "$PYTHON_LD_LIBRARY_PATH" }

[env]
VIRTUAL_ENV = "/home/runner/${REPL_SLUG}/venv"
PATH = "${VIRTUAL_ENV}/bin"
PYTHONPATH="${VIRTUAL_ENV}/lib/python3.8/site-packages"
REPLIT_POETRY_PYPI_REPOSITORY="https://package-proxy.replit.com/pypi/"
MPLBACKEND="TkAgg"
POETRY_CACHE_DIR="${HOME}/${REPL_SLUG}/.cache/pypoetry"

# Enable unit tests. This is only supported for a few languages.
[unitTest]
language = "python3"

# Add a debugger!
[debugger]
support = true

  # How to start the debugger.
  [debugger.interactive]
  transport = "localhost:0"
  startCommand = ["dap-python", "main.py"]

    # How to communicate with the debugger.
    [debugger.interactive.integratedAdapter]
    dapTcpAddress = "localhost:0"

    # How to tell the debugger to start a debugging session.
    [debugger.interactive.initializeMessage]
    command = "initialize"
    type = "request"

      [debugger.interactive.initializeMessage.arguments]
      adapterID = "debugpy"
      clientID = "replit"
      clientName = "replit.com"
      columnsStartAt1 = true
      linesStartAt1 = true
      locale = "en-us"
      pathFormat = "path"
      supportsInvalidatedEvent = true
      supportsProgressReporting = true
      supportsRunInTerminalRequest = true
      supportsVariablePaging = true
      supportsVariableType = true

    # How to tell the debugger to start the debuggee application.
    [debugger.interactive.launchMessage]
    command = "attach"
    type = "request"

      [debugger.interactive.launchMessage.arguments]
      logging = {}

# Configures the packager.
[packager]
# Search packages in PyPI.
language = "python3"
# Never attempt to install `unit_tests`. If there are packages that are being
# guessed wrongly, add them here.
ignoredPackages = ["unit_tests"]

  [packager.features]
  enabledForHosting = false
  # Enable searching packages from the sidebar.
  packageSearch = true
  # Enable guessing what packages are needed from the code.
  guessImports = true

# These are the files that need to be preserved when this 
# language template is used as the base language template
# for Python repos imported from GitHub
[gitHubImport]
requiredFiles = [".replit", "replit.nix", ".config", "venv"]
```

Once done, you may run the bot. If there are any errors, please get in contact with me on our Discord server, Zono Hub.


# 24/7 Uptime
To keep the bot online 24/7, use a uptime monitor service like UptimeRobot.
