# vgr-availability-svc

## Setup

  - Install Python version `3.8`+
  - Download dependencies with the command `pip install -r requirements.txt`
  - Configure the next environment variables:
    - `FLASK_ENV` set to `development` or `production`.
    - `DEBUG_ENABLED` `true` for enable debug, `false` otherwise.
    - Optionally you can set the environment variables `HOST` and `PORT` to change the default values of `0.0.0.0` and `8092` respectively.
  - Run the command `python app.py`
  - App will run on `http://localhost:8092`
  - A complete **swagger.yml** definition is provided to test the available endpoints.