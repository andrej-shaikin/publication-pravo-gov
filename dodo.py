from doit.tools import CmdAction, LongRunning


def task_pip_compile():
    return {
      "actions": [
        CmdAction("pip-compile -o requirements/main.txt requirements/main.in"),
        CmdAction("pip-compile -o requirements/dev.txt requirements/dev.in"),
      ]
    }


def task_pip_install():
    return {"actions": [CmdAction("pip install -r requirements/main.txt -r requirements/dev.txt")]}


def task_celery_beat():
    return {"actions": [LongRunning("celery -A conf.celery_conf:app beat -l INFo")]}


def task_celery_worker():
    return {"actions": [LongRunning("celery -A conf:celery_conf:app worker -E --pool-solo")]}


def task_celery_flower():
    return {"actions": [LongRunning("celery -A conf:celery_conf:app flower --address=0.0.0.0 --port=5556")]}


__all__ = [
  "task_pip_sync",
  "task_pip_compile",
  "task_celery_beat",
  "task_celery_worker",
  "task_celery_flower",
]
