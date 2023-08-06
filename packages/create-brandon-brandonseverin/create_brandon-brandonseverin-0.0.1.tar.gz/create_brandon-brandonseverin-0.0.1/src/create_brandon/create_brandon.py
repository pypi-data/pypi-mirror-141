"""create_brandon commandline application
By calling `create_brandon` in the command line, the user will be prompted
to answer a few questions. The answers to these questions will create an
directory for the user to proceed and run and experiment. The directory 
will be named based on the date and time of running `create_brandon` and
will contain `data/` and `scripts/` folders as well as a jupyter notebook.

If the user calls `create_brandon -v` they will meet Brandon and be
welcomed to the matrix.
"""
from datetime import datetime, timezone
from pathlib import Path
import sys
import copy
from create_brandon.scripts.helper_functions import (
    initialise_notebook,
    speak_friend_and_enter,
    create_parent_name,
    prompts,
)


def main(args=None):

    if args is None:
        input_arg_list = sys.argv[1:]

    # Only trigger if input arguments are correct
    speak_friend_and_enter(
        input_arg_list=input_arg_list, verbose_list=["-verbose", "-v"]
    )

    fridge_name = input(prompts["fridge_prompt"])
    device_name = input(prompts["device_prompt"])
    experiment_name = input(prompts["experiment_prompt"])

    now = datetime.now(timezone.utc)
    date_today = now.strftime("%Y%m%d_%H%M%S")

    parent_name = create_parent_name(
        date_today, fridge_name, device_name, experiment_name
    )
    notebook_name = copy.deepcopy(parent_name)

    print("Creating directories...")
    Path("./" + parent_name + "/data").mkdir(parents=True)
    Path("./" + parent_name + "/scripts").mkdir(parents=True)
    initialise_notebook(notebook_name, parent_name)

    print(f"Experiment directory made at: {parent_name}")

