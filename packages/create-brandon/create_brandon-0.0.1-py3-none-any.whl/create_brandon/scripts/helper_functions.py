from random import gauss
import time
from pathlib import PurePath
import nbformat as nbf

prompts = {
    "introduction": "Hello, who am I talking to?",
    "fridge_prompt": "Name of the fridge: ",
    "device_prompt": "Name of the device: ",
    "experiment_prompt": "Name of the experiment: ",
}


def wpm_to_cps(typing_speed):
    """Convert words per minute to characters per second
    Assumes that 1 word per minute is the same as 5 characters per second

    Args:
        typing_speed (float): Typing Speed in Words per minute

    Returns:
        float: typing speed in characters per second
    """
    assert isinstance(
        typing_speed, (int, float)
    ), f"typing_speed is neither int nor float, it is {type(typing_speed)}"
    cps = typing_speed * 5 / 60
    return cps


def type_to_terminal(output, typing_speed=100, deviation=10):
    """Type text in commmand line as though being typed by a human.

    Args:
        output (string): Text to be typed in the command line
        typing_speed (int, optional): Typing speed of computer. Defaults to 70.
        deviation (int, optional): Deviation of typing speed 
            (Guassian distribution). Defaults to 5.
    """
    output = str(output)
    for character in output:
        wpm = gauss(typing_speed, deviation)
        cps = wpm_to_cps(wpm)
        print(character, end="", flush=True)
        time.sleep(1 / cps)

    print("")


def create_parent_name(
    date_today, fridge_name=None, device_name=None, experiment_name=None
):
    """Create name of project
    Will be used as folder name and name of jupyter notebook unless stated otherwise
    Relies on the date today

    Args:
        date_today (string): _description_
        fridge_name (string, optional): Defaults to None.
        device_name (string, optional): Defaults to None.
        experiment_name (string, optional): Defaults to None.

    Returns:
        string: Name of project (<date>_<fridge_name>_<device_name>_<experiment_name>)
    """
    parent_name = (
        (
            str(date_today)
            + "_"
            + str(fridge_name)
            + "_"
            + str(device_name)
            + "_"
            + str(experiment_name)
        )
        .lower()
        .replace(" ", "_")
    )

    return parent_name


def initialise_notebook(notebook_name=None, directory=None, content=None):
    """Create Jupyter notebook named of name `notebook_name` in the
    directory `directory` with `content` in the cells. 

    Args:
        notebook_name (string, optional): Name of Jupyter notebook. 
        Defaults to None.
        directory (string, optional): Name of directory containing new 
        Jupyter notebook. Defaults to None ("Untitled").
        content (string, optional): Content of new Jupyter notebook. 
        Defaults to None ("Untitled").
    """
    if notebook_name == None:
        notebook_name = "Untitled"

    nb = nbf.v4.new_notebook()
    text = content if content != None else "# Untitled "

    code = ""

    nb["cells"] = [nbf.v4.new_markdown_cell(text), nbf.v4.new_code_cell(code)]

    file_path = PurePath(directory).joinpath(notebook_name + ".ipynb")
    with open(file_path, "w") as f:
        nbf.write(nb, f)


def speak_friend_and_enter(input_arg_list=[None], verbose_list=["-verbose", "-v"]):
    """Brandon introduces itself, and asks the user their name.
    This function is a bit of an Easter egg and is to simulate the opening 
    scene of *The Matrix* - Wake up Neo.

    Args:
        input_arg_list (list, optional): Command line arguments passed by the 
            user. Defaults to [None].
        verbose_list (list, optional): Required list of arguments to trigger 
            conversation from Brandon. Defaults to ["-verbose", "-v"].
    """

    input_arg_list = map(str, input_arg_list)
    input_arg_list = [word.lower() for word in input_arg_list]

    if any(arg in input_arg for input_arg in input_arg_list for arg in verbose_list):
        type_to_terminal(prompts["introduction"])
        experimentalist_name = input()
        time.sleep(0.7)
        first_name = experimentalist_name.split()[0]
        type_to_terminal(f"Hello {first_name}.")
        time.sleep(0.6)
        type_to_terminal(f"This is Brandon. Welcome to The Matrix")
        time.sleep(0.6)
        type_to_terminal("Let's start an experiment.")
        type_to_terminal("...")
