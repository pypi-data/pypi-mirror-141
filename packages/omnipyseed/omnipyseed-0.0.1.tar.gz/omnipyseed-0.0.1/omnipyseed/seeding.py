import os
import sys
import random


def is_package_available(package_name):
    """
    It checks if a Python package is installed.

    Args:
        package_name (string):  A Python package name

    Returns:
        True if the Python package is installed, False otherwise.
    """
    available = False
    if package_name in sys.modules:
        available = True
    return available


def seed_numpy():
    """
    It imports and seeds Numpy, if it's installed on the system.

    Args:
        Void

    Returns:
        Void
    """
    if is_package_available("numpy"):
        import numpy as np
        np.random.seed(random.randint(1, 1E6))


def seed_torch():
    """
    It imports and seeds Torch, if it's installed.

    Args:
        Void

    Returns:
        Void
    """
    if is_package_available("torch"):
        import torch
        torch.manual_seed(random.randint(1, 1E6))
        torch.cuda.manual_seed_all(random.randint(1, 1E6))


def seed_python():
    """
    It seeds OS-based Python RNGs.

    Args:
        Void

    Returns:
        Void
    """
    os_seed = random.randint(1, 1E6)
    os.environ['PYTHONHASHSEED'] = str(os_seed)


def universal_seed(seed=1234):
    """
    It seeds all the native Python RNGs as well as Numpy and Torch (if the
    latter two are already installed)

    Args:
        seed (long int):    The seed for the RNGs

    Returns:
        void
    """
    random.seed(seed)
    seed_numpy()
    seed_torch()
    seed_python()
