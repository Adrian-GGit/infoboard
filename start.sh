#!/bin/bash
poetry install
poetry shell
flask --app app run