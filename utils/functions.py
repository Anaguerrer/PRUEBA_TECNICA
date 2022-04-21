import datetime
from utils import classes, queries
import logging



# Get all weather info for a particulay city in a correct format and insert it into the table
def get_and_insert_city_info(city, key):
    try:
        logging.info('Enter to get and insert info for: %s', city.name)
        resp = []
        dates = get_dates()
        for date in dates:
            weather_day_info = city.weather_day(date, key)
            resp.append(weather_day_info)

        temps = get_arr_temps_5days(resp)
        humidity = get_arr_hum_2days(resp)
        wind_speed = resp[0]['current']['wind_speed']

        row = classes.data_to_insert(city.name, temps, humidity, wind_speed)
        queries.insert_city(row)
    except:
        logging.error('Error obtaining or inserting the data for: %s', city.name)


# function to obtain the 5 days before today in an acceptable format
def get_dates():
    try:
        logging.info('Enter to get dates')
        today = datetime.date.today()
        today1 = today - datetime.timedelta(1)
        today2 = today1 - datetime.timedelta(1)
        today3 = today2 - datetime.timedelta(1)
        today4 = today3 - datetime.timedelta(1)
        
        # convert dates to timestamp format
        timestamptoday = datetime.datetime.strptime(str(today), "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc).timestamp()
        timestamptoday1 = datetime.datetime.strptime(str(today1), "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc).timestamp()
        timestamptoday2 = datetime.datetime.strptime(str(today2), "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc).timestamp()
        timestamptoday3 = datetime.datetime.strptime(str(today3), "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc).timestamp()
        timestamptoday4 = datetime.datetime.strptime(str(today4), "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc).timestamp()

        dates = [str(timestamptoday).replace(".0",""), str(timestamptoday1).replace(".0",""), str(timestamptoday2).replace(".0",""), str(timestamptoday3).replace(".0",""), str(timestamptoday4).replace(".0","")]
        return dates
    except:
        logging.error('Error formatting and obtaining the dates')
        

# funtion to obtain an array with all temperature registers for a particular city during 5 days
def get_arr_temps_5days(data):
    try:
        logging.info('Enter to get array of temps')
        tempArr = []
        for day in data:
            for hour in day['hourly']:
                tempArr.append(hour['temp'])
        return tempArr
    except:
        logging.error('Error building array of temps')


# funtion to obtain an array with all humidity registers for a particular city during 2 days
def get_arr_hum_2days(data):
    try:
        logging.info('Enter to get array of humidity')
        humArr = []
        for day in (data[0], data[1]):
            for hour in day['hourly']:
                humArr.append(hour['humidity'])
        return humArr
    except:
        logging.error('Error building array of humidity')
    