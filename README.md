# Infoboard
This little project is a web app to visualize different information e.g. weather data.


# Installation
Setup for backend executing in root dir:
```
poetry install
```

# Setup
Get your api key from [openweathermap](https://home.openweathermap.org/api_keys) and export it as env var `OPENWEATHER_API_KEY`


# Start
Get into poetry shell:
```
poetry shell
```
Execute in root dir:
```
flask --app app run
```


# Development and debugging
Execute in root dir:
```
flask --app app --debug run
```
