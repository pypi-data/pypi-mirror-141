# ta-core
[![pip version](https://img.shields.io/pypi/v/ta-core.svg)](https://pypi.python.org/pypi/ta-core)

Thoughtful Automation Core package. This package contains the function required for Thoughtful Automation bots. Documentation may be closed and certain functions may not work outside the Thoughtful Automation environment.

Example Usage
-------------
To use `Status` you need to install the library `rpaframework` and get WorkItems from `robocorp` environment.

    from ta_core.status import Status

    Status.change_status_to_warning()
