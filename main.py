
from utils import classes, functions, queries

def main():
    logging.basicConfig(filename="std.log",
					format='%(asctime)s %(message)s', 
					filemode='a',
                    level=logging.DEBUG) 
    logging.info('starting main')

    ApiKey = "yourAPIkey"
    cities = {
        classes.city("Tokio", "139.6917", "35.6895"),
        classes.city("Nueva York", "-73.935242", "40.730610")
    }
    
    queries.create_table()

    for city in cities:
        functions.get_and_insert_city_info(city, ApiKey)

    # ----------------- queries -----------------------

    queries.get_highest_tempMax()
    queries.order_cities_by_wind_speed('asc')
    # queries.query_all_table()

    queries.close_conexion()

        
if __name__ == '__main__':
    import sys
    import logging
    import os
    # logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    sys.exit(int(main() or 0))