# Backwards compatibility wrapper for driver_factory
from utils.driver_factory import DriverFactory


def get_driver(context=None):
    return DriverFactory.get_driver(context=context)
