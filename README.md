# raspi
General overview for
- weather info
    - clothing recommendation
- public tansit info


# Installation
Setup for backend executing in root dir:
```
poetry install
```

Setup for frontend executing in root dir:
```
npm install
```


# Implementation
Updates are made every 5 minutes. This means every
- hour => 12 updates
- day => 288 updates
- week => 2016 updates
- month => 8640 updates


# Start
Execute in root dir:
```
flask --app app run
```


# Development and debugging
Execute in root dir:
```
flask --app app --debug run
```