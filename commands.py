from datetime import date, datetime
import calendar
import prettytable
from utils import check_weekday, check_week_nr, check_date_fields, error_handler, valid_weekdays
from db_access import create_customer, create_order, get_all_orders_by_customer, get_route_station_times, Order, Route, RouteStationTime, RouteWeekday, get_routes, get_route_weekdays, get_stations
from typing import Optional
# User stories c)
def get_all_station_routes(station: str, weekday: str):
    # Ensure only first letter in weekday is capitalized
    station = str.capitalize(str.lower(station))    
    weekday = str.capitalize(str.lower(weekday))
    check_weekday(weekday)
    all_routes = get_routes()
    route_weekdays = get_route_weekdays()
    route_station_times = get_route_station_times()
    routes_that_run_on_weekday = list[int]
    routes_that_pass_station = list[int]

    for r in route_weekdays:
        if r.route_id not in routes_that_run_on_weekday and r.weekday == weekday:
            routes_that_run_on_weekday.append(r.route_id)
    for r in route_station_times:
        if (r.route_id not in routes_that_pass_station and r.station_name == station):
            routes_that_pass_station.append(r.route_id)
    relevant_routes = list[Route]
    for r in all_routes:
        if r.route_id in routes_that_run_on_weekday and r.route_id in routes_that_pass_station:
            relevant_routes.append(r)
    
    table = prettytable.PrettyTable(['Route ID', 'Name', 'Operator ID', 'Start Station Name', 'End Station Name'])    

    for r in relevant_routes:    
        table.add_row([r.route_id, r.operator_id, r.start_station_name, r.end_station_name])
    return table

# User stories d)
def get_routes_between_stations(start_station: str, end_station: str, day_str: str, month_str: str, year_str: str):
    day = int(day_str)
    month = int(month_str)
    year = int(year_str)
    check_date_fields(day, month, year)
    search_date = date(year, month, day)
    route_station_times = get_route_station_times()
    routes = get_routes()
    relevant_routes = list[Route]
    for r in routes:
        all_relevant_rst = list[RouteStationTime]
        rst_start = Optional[RouteStationTime]
        rst_end = Optional[RouteStationTime]
        for rst in route_station_times:
            if rst.route_id == r.route_id:
                if (rst.station_name == start_station):
                    rst_start = rst
                if (rst.station_name == end_station):
                    rst_end = rst
                all_relevant_rst.append(rst)
        if (
            rst_start != None
            and rst_end != None
            and (
                rst_start.is_start
                or rst_end.is_end
                or rst_start.time_of_arrival < rst_end.time_of_arrival
            )
        ):
            relevant_routes.append(r)
    table = prettytable.PrettyTable(['Route ID', 'Name', 'Operator ID', 'Start Station Name', 'End Station Name'])
    for r in relevant_routes:    
        table.add_row([r.route_id, r.operator_id, r.start_station_name, r.end_station_name])
    return table

# User stories e)
def register_customer(customer_number: str, name: str, email: str, mobile_number: str):
    if customer_number == "" or name == "" or email == "" or mobile_number == "":
        error_handler("All fields must have a value")
    create_customer(customer_number, name, email, mobile_number)    
    return "Customer registration finished"

# User stories g part 1)
def get_available_seats(route_id: str, day_str: str, month_str: str, year_str: str):
        day = int(day_str)
        month = int(month_str)
        year = int(year_str)        
        check_date_fields(day, month, year)
        search_date = date(year, month, day)
        pass

# User stories g part 2)
def register_order(customer_id: str, trip_year_str: str, trip_week_nr_str: str, start_station: str, end_station: str, route_id: str, day_str: str, month_str: str, year_str: str, places: list[str]):
    day = int(day_str)
    month = int(month_str)
    year = int(year_str)   
    check_date_fields(day, month, year)
    route_date = datetime(year, month, day)
    week_nr = route_date.date.isocalendar()[1]
    weekday = calendar.day_name[route_date.weekday()]
    # TODO: GENERATE
    order_id = 123     
    start_station = str.capitalize(str.lower(start_station))
    end_station = str.capitalize(str.lower(end_station))
    check_date_fields(1, 1, year)
    check_week_nr(week_nr)
    check_weekday(weekday)
    create_order(order_id, int(customer_id), datetime.now(), year, week_nr, start_station, end_station, int(route_id), weekday)  
    for place in places:
        # TODO: FIGRE THIS SHIT OUT
        create_order_place()  
    
def get_future_customer_orders(customer_id: str):
    orders = get_all_orders_by_customer(int(customer_id))    
    route_station_times = get_route_station_times()    
    now = datetime.now()    
    week_nr = now.date.isocalendar()[1]    
    future_orders = list[Order]
    for o in orders:
        relevant_time = None
        for t in route_station_times:
            if t.route_id ==  o.route_id and t.is_start:
                relevant_time = t
        weekday_int = valid_weekdays.index(o.weekday)
        if (o.trip_year > now.year):
            future_orders.append(o)
        elif (o.trip_year == now.year):
            if (o.trip_week_nr > week_nr):
                future_orders.append(o)
            elif (o.trip_week_nr == week_nr):
                if (weekday_int > now.weekday):
                    future_orders.append(o)
                elif (weekday_int == now.weekday and relevant_time != None and relevant_time.time_of_arrival > now.time):                 
                    future_orders.append(o)
    table = prettytable.PrettyTable(['Order ID', 'Customer ID', 'Purchase DateTime', 'Trip Year', 'Trip Week Nr', 'Start Station Name', 'End Station Name', 'Route ID', 'Weekday'])    

    for order in future_orders:
        table.add_row([order.order_id, order.customer_id, order.datetime, order.trip_year, order.trip_week_nr, order.start_station_name, order.end_station_name, order.route_id, order.weekday])
    return table
    

