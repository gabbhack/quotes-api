#!/usr/bin/env bash

set -e

aerich upgrade
uvicorn --host=0.0.0.0 --port=80 app:app