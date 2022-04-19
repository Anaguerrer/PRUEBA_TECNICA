
def main():
    # We create the connection to sqlite3 and create the table with the requested structure
    url = "https://community-open-weather-map.p.rapidapi.com/onecall/timemachine"
    conexion=sqlite3.connect("weather_info.db")
    try:
        conexion.execute("""create table cities (
                              codigo integer primary key autoincrement,
                              name string,
                              temp_max real,
                              temp_min real,
                              temp_media real,
                              hum_media real,
                              wind_speed real,
                              date date
                        )""")
        print("table cities has been created")                        
    except sqlite3.OperationalError:
    # we configure the exception so that the program only creates the table 1 time
        print("The table cities already exists")

    # in the variable 'cities' we save the cities requested in the exercise (you can add all the cities you want)
    cities = [{"name":"Tokio", "lat":"35.6895","lon":"139.6917"}, { "name":"NY", "lat":"40.730610","lon":"-73.935242"}]
    # we get today's date
    dt = datetime.today()

    # we put today's date at 00:00:00 so that it can consult the 24 hours of the day and we calculate the previous 5 days
    today = dt.replace(hour=00, minute=00, second=00, microsecond=00)
    today1 = today - timedelta(1)
    today2 = today1 - timedelta(1)
    today3 = today2 - timedelta(1)
    today4 = today3 - timedelta(1)
    today5 = today4 - timedelta(1)
    print('today', today)
    print('5 days before', today5)
    # convert dates to timestamp format
    timestamptoday = today.replace(tzinfo=timezone.utc).timestamp()
    timestamptoday1 = today1.replace(tzinfo=timezone.utc).timestamp()
    timestamptoday2 = today2.replace(tzinfo=timezone.utc).timestamp()
    timestamptoday3 = today3.replace(tzinfo=timezone.utc).timestamp()
    timestamptoday4 = today4.replace(tzinfo=timezone.utc).timestamp()
    # timestamptoday5 = today5.replace(tzinfo=timezone.utc).timestamp()
    
    # we save in the variable dates the dates to consult (in string and removing the milliseconds)
    dates = [str(timestamptoday).replace(".0",""), str(timestamptoday1).replace(".0",""), str(timestamptoday2).replace(".0",""), str(timestamptoday3).replace(".0",""), str(timestamptoday4).replace(".0","")]

    # we query the API for each city requested on each day
    for c in cities:
        tempMax = -9999999
        tempMin = 99999999
        medTemp = 0
        mainhum = 0
        # we initialize the count to use it in the calculation of average humidity and wind speed
        # we initialize the counter to know how many hours of today's query (since it will not be 24) and thus be able to make the average correctly
        count = 0
        counter = 0
        for date in dates:
            # print('date:', str(date))
            count = count + 1
            queryparams = {"lat":c['lat'],"lon":c['lon'],"dt":date}
            headers = {
            "X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com",
            "X-RapidAPI-Key": "token"
            }
            response = requests.request("GET", url, headers=headers, params=queryparams)
            response_dict = json.loads(response.text)
            # we loop through the response data, which is given by hours
            for j in response_dict['hourly']:
                counter = counter + 1
                if float(j['temp']) > tempMax:
                    tempMax = j['temp']
                if float(j['temp']) < tempMin:
                    tempMin = j['temp']
                medTemp = medTemp + j['temp']
                # here we save the humidity data only for the last two days (yesterday and before yesterday). 
                # We do not count today because it is not complete and would skew the statistics.
                if count > 1 & count < 4:
                    mainhum = mainhum + j['humidity']
                # we save the wind speed only for today.
                # Today's wind speed is required, but it should be noted that today's information 
                # it will only be complete if the process is executed at 00:00:00 the next day.
                if count == 1:
                    windSpeed = j['wind_speed']

        # we calculate the average temperature and average humidity required
        print('hours counter', counter)
        medTemp = medTemp / counter 
        mainhum = mainhum /(24*2)
        print('temp max for', c['name'], 'in the last 5 days is:', tempMax)
        print('temp min for ',c['name'], 'in the last 5 days is:', tempMin)
        print('temp media for ', c['name'], 'in the last 5 days is:', medTemp)
        print('hum media for ',c['name'], 'in the last 5 days is:', mainhum)

        # no further transformation of the data is required because the API returns the temperature in Kelvin,
        # humidity in percentage and wind speed in m/s.
        # At this point we would have calculated the data of the last 5 days for each city: We insert them in the BBDD.
        conexion.execute("insert into cities(name,temp_max,temp_min,temp_media,hum_media,wind_speed,date) values (?,?,?,?,?,?,?)", (c['name'], tempMax, tempMin, medTemp, mainhum, windSpeed, datetime.today()))
        conexion.commit()
    print('-----------------------------------------------------------------------------------------------------')
    print('-----------------------------------------------------------------------------------------------------')

    # --------- REQUIRED QUERIES ---------------

    # we select the city with the highest tempMax for today.
    query1 = conexion.execute("select * from cities where date >" + str(timestamptoday).replace(".0","") + " order by temp_max desc limit 1")
    for fila in query1:
        print('THE HIGHEST TEMPERATURE FOR TODAY IS', fila[2],'K CORRESPONDING TO THE CITY OF', fila[1])
        print(fila)  

    print('----------------------------------------------------')
    # we order the cities from lowest to highest wind speed for today
    query2 = conexion.execute("select name, wind_speed from cities where date >" + str(timestamptoday).replace(".0","") + " order by wind_speed asc")
    print('WE ORDER THE CITIES FROM LOWEST TO HIGHEST WIND SPEED FOR TODAY')
    for fil in query2:
        print(fil)


    # query to display all the data in the table (uncomment to use)

    # queryall = conexion.execute("select * from cities")
    # print('SE MUESTRAN TODOS LOS DATOS DE LA TABLA')
    # print('----------------')
    # for element in queryall:
    #     print(element)  

    conexion.close()



        
if __name__ == '__main__':
    import sys
    import sqlite3
    import requests
    from datetime import datetime, timedelta, timezone
    import json

    sys.exit(int(main() or 0))