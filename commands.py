from datetime import date, datetime, now
from utils import check_weekday, check_week_nr, check_date_fields, error_handler
from db_access import create_customer, create_order, get_orders_by_customer
# User stories c)
def get_all_station_routes(station: str, weekday: str):
    # Ensure only first letter in weekday is capitalized
    station = str.capitalize(str.lower(station))    
    weekday = str.capitalize(str.lower(weekday))
    check_weekday(weekday)
    pass

# User stories d)
def get_routes_between_stations(start_station: str, end_station: str, day_str: str, month_str: str, year_str: str):
    day = int(day_str)
    month = int(month_str)
    year = int(year_str)
    check_date_fields(day, month, year)
    search_date = date(year, month, day)
    pass

# User stories e)
def register_customer(customer_number: str, name: str, email: str, mobile_number: str):
    if customer_number == "" or name == "" or email == "" or mobile_number == "":
        error_handler("All fields must have a value")
    create_customer(customer_number, name, email, mobile_number)    
    return "Customer created"

# User stories g part 1)
def get_available_seats(route_id: str, day_str: str, month_str: str, year_str: str):
        day = int(day_str)
        month = int(month_str)
        year = int(year_str)        
        check_date_fields(day, month, year)
        search_date = date(year, month, day)
        pass

# User stories g part 2)
def register_order(customer_id: str, trip_year_str: str, trip_week_nr_str: str, start_station: str, end_station: str, route_id: str, weekday: str, places: list[str]):
    # TODO: GENERATE
    order_id = 123
    year = int(trip_year_str)
    week_nr = int(trip_week_nr_str)
    start_station = str.capitalize(str.lower(start_station))
    end_station = str.capitalize(str.lower(end_station))
    check_date_fields(1, 1, year)
    check_week_nr(week_nr)
    check_weekday(weekday)
    create_order(order_id, int(customer_id), datetime.now(), year, week_nr, start_station, end_station, int(route_id), weekday)  
    for place in places:
        # TODO: FIGRE THIS SHIT OUT
        create_order_place()  
    
def get_customer_orders(customer_id: str):
    orders = get_orders_by_customer(int(customer_id))
    # TODO: NICE FORMATTING
    return orders
    

