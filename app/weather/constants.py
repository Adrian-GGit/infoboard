# weather coords constants
API_KEY_ENV_VAR = 'OPENWEATHER_API_KEY'
API_KEY_MISSING = 'Missing weather API key'
COORDS_CITY_MISSING = 'No city provided'
COORDS_CITY_NOT_FOUND = 'City not found'

CITY_MISSING = 'Missing argument city'

CITY = 'city'
LATITUDE = 'latitude'
LONGITUDE = 'longitude'

# weather forecast constants
TIME = 'time'
FORECASTS = 'forecasts'
SUNRISE = 'sunrise'
SUNSET = 'sunset'
TEMP_MIN = 'temp_min'
TEMP_MAX = 'temp_max'
TEMP = 'temp'
WEATHER_FORECAST_ID = 'wf_id'
WEATHER_FORECAST_DESCRIPTION = 'wf_description'
WEATHER_FORECAST_ICON = 'wf_icon'
TEMP_FEELS_LIKE = 'temp_fl'
PROP_PRECIPITATION = 'prop_precip'


# weather description mappings
WEATHER_DESCRPITION_MAPPING = {
    # thunderstorm
    'thunderstorm with light rain': 'thunderstorm',
    'thunderstorm with rain': 'thunderstorm',
    'thunderstorm with heavy rain': 'thunderstorm',
    'light thunderstorm': 'thunderstorm',
    'thunderstorm': 'thunderstorm',
    'heavy thunderstorm': 'thunderstorm',
    'ragged thunderstorm': 'thunderstorm',
    'thunderstorm with light drizzle': 'thunderstorm',
    'thunderstorm with drizzle': 'thunderstorm',
    'thunderstorm with heavy drizzle': 'thunderstorm',
    # drizzle
    'light intensity drizzle': 'rain',
    'drizzle': 'rain',
    'heavy intensity drizzle': 'rain',
    'light intensity drizzle rain': 'rain',
    'drizzle rain': 'rain',
    'heavy intensity drizzle rain': 'rain',
    'shower rain and drizzle': 'rain',
    'heavy shower rain and drizzle': 'rain',
    'shower drizzle': 'rain',
    # rain
    'light rain': 'rain',
    'moderate rain': 'rain',
    'heavy intensity rain': 'shower rain',
    'very heavy rain': 'shower rain',
    'extreme rain': 'shower rain',
    'freezing rain': 'rain',
    'light intensity shower rain': 'rain',
    'shower rain': 'shower rain',
    'heavy intensity shower rain': 'shower rain',
    'ragged shower rain': 'shower rain',
    # snow
    'light snow': 'snow',
    'snow': 'snow',
    'heavy snow': 'snow',
    'sleet': 'snow',
    'light shower sleet': 'snow',
    'shower sleet': 'snow',
    'light rain and snow': 'snow',
    'rain and snow': 'snow',
    'light shower snow': 'snow',
    'shower snow': 'snow',
    'heavy shower snow': 'snow',
    # atmosphere
    'mist': 'mist',
    'smoke': 'mist',
    'haze': 'mist',
    'sand/dust whirls': 'mist',
    'fog': 'mist',
    'sand': 'mist',
    'dust': 'mist',
    'volcanic ash': 'mist',
    'squalls': 'mist',
    'tornado': 'mist',
    # clear
    'clear sky': 'clear sky',
    # clouds
    'few clouds': 'few clouds',
    'scattered clouds': 'scattered clouds',
    'broken clouds': 'broken clouds',
    'overcast clouds': 'broken clouds'
}
