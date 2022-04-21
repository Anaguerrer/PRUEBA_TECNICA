import datetime
import sqlite3
import logging

conexion=sqlite3.connect("weather_info.db")

def create_table():
    try:
        logging.info('Creating table')
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
        logging.error("The table cities already exists")


def insert_city(row):
    try:
        logging.info('inserting data about: %s', row.name)
        conexion.execute("insert into cities(name,temp_max,temp_min,temp_media,hum_media,wind_speed,date) values (?,?,?,?,?,?,?)", (row.name, row.temp_Max, row.temp_Min, row.temp_Main, row.hum_Main, row.wind_speed, datetime.date.today()))
        conexion.commit()
    except sqlite3.OperationalError:
        logging.error("Error inserting the data about: %s", row.name)


def get_highest_tempMax():
    try:
        logging.info('Executing query for highest temp')
        query1 = conexion.execute("select * from cities where date >" + str(datetime.date.today()).replace(".0","") + " order by temp_max desc limit 1")
        for fila in query1:
            print('THE HIGHEST TEMPERATURE FOR TODAY IS', fila[2],'K CORRESPONDING TO THE CITY OF', fila[1])
            print(fila) 
    except sqlite3.OperationalError:
        logging.error("Error executing query get_highest_tempMax")


def order_cities_by_wind_speed(param):
    try:
        logging.info('Ordering cities by wind speed')
        query2 = conexion.execute("select name, wind_speed from cities where date >" + str(datetime.date.today()).replace(".0","") + " order by wind_speed " + param)
        print('WE ORDER THE CITIES BY WIND SPEED FOR TODAY')
        for fil in query2:
            print(fil)
    except sqlite3.OperationalError:
        logging.error("Error executing query order_cities_by_wind_speed")


def query_all_table():
    try:
        logging.info('executing query for all data')
        queryall = conexion.execute("select * from cities")
        print('----------------')
        print('SE MUESTRAN TODOS LOS DATOS DE LA TABLA')
        for element in queryall:
            print(element)
    except sqlite3.OperationalError:
        logging.error("Error executing query all")


def close_conexion():
    conexion.close()