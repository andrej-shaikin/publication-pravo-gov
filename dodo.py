from doit.tools import CmdAction


def task_pip_compile():
    return {
      "actions": [
        CmdAction(
            "pip-compile -o requirements/main.txt requirements/main.in"
        ),
        CmdAction(
            "pip-compile -o requirements/dev.txt requirements/dev.in"
        ),
      ]
    }


def task_pip_sync():
    return {
      "actions": [
        CmdAction(
            "pip-sync requirements/main.txt requirements/dev.txt"
        ),
      ]
    }


__all__ = [
  "task_pip_sync",
  "task_pip_compile",
]
