from temp_functions import *
from pathlib import Path
import os

if __name__ == "__main__":

    # Get the path of the test folder
    path = os.path.join(Path(__file__).parents[0], "ParentFolder")

    PackageCreator(path)