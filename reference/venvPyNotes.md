# Python Virtual Environment (.venv) Notes

## What is .venv?
- A .venv is a private, isolated Python environment for your project.
- It keeps dependencies (packages) separate from other projects and from system Python.
- It makes it easier to have a common version of Python when working on our team project.
- Eliminates compatibility issues

---

## Creating a virtual environment
```bash
# Inside the project folder:
/usr/local/bin/python3 -m venv .venv
```

---

## Activating the virtual environment
```bash
# Mac/Linux (zsh/bash):
source .venv/bin/activate
```
- After activating, the prompt will look like this:
```
(.venv) user@MacBook project %
```
- The `(.venv)` at the start of the prompt means you’re inside the virtual environment.

---

## Deactivating the virtual environment
```bash
deactivate
```
- Your prompt will return to normal, meaning you’re back to system Python.

---

## Why .venv?
- Keeps project dependencies isolated.
- Prevents conflicts between projects.
- Makes it easy to share environment with teammates via `requirements.txt`.

---

## Saving dependencies for teammates
```bash
# After installing packages (example: pip install pillow)
pip freeze > requirements.txt

# Teammates can install the same environment:
pip install -r requirements.txt
```

---

## Good things to do and habits
- ALWAYS activate .venv before working on the project.
- NEVER commit the .venv folder to Git (add `.venv/` in `.gitignore`).
- If .venv breaks, you can safely delete it and recreate it with:
```bash
rm -rf .venv
/usr/local/bin/python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Quick reference
```bash
Activate:   source .venv/bin/activate
Deactivate: deactivate
Rebuild:    rm -rf .venv && /usr/local/bin/python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```
