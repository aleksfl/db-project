from datetime import date, time, datetime, timedelta
import calendar
import prettytable
from utils import check_weekday, check_week_nr, check_date_fields, error_handler, valid_weekdays
from db_access import create_customer, create_order, get_all_orders_by_customer, get_route_station_times, get_routes, get_route_weekdays, get_order_places_by_order, get_arranged_cars_by_route, get_places, get_orders, get_route_station_times_by_route, RouteStationTime, get_car_types, Order, create_order_place


def get_all_station_routes(station: str, weekday: str):
    """
        Userstory C:
        
        Gets all the routes for a given station and weekday
        
        :param station: The station where the routes are departuring from
        :param weekday: The weekday to be checked for routes
        
        :returns: A table with the route information for the given input
    """
    station = str.capitalize(str.lower(station))
    weekday = str.capitalize(str.lower(weekday))
    if check_weekday(weekday) == False: 
        return "Failed"
    all_routes = get_routes()
    route_weekdays = get_route_weekdays()
    route_station_times = get_route_station_times()
    routes_that_run_on_weekday = []
    routes_that_pass_station = []
    arrival_times = {}
    for r in route_weekdays:
        if r.route_id not in routes_that_run_on_weekday and r.weekday == weekday:
            routes_that_run_on_weekday.append(r.route_id)
    for r in route_station_times:
        if (r.route_id not in routes_that_pass_station and r.station_name == station):
            arrival_times[r.route_id] = r.time_of_arrival
            routes_that_pass_station.append(r.route_id)
    relevant_routes = [
        r
        for r in all_routes
        if r.route_id in routes_that_run_on_weekday
        and r.route_id in routes_that_pass_station
    ]
    table = prettytable.PrettyTable(['Route ID', 'Name', 'Operator ID', 'Start Station Name', 'End Station Name', 'Time Of Arrival At Station'])    

    for r in relevant_routes:    
        table.add_row([r.route_id, r.name, r.operator_id, r.start_station_name, r.end_station_name, arrival_times[r.route_id]])
    return table


def get_routes_between_stations(start_station: str, end_station: str, day_str: str, month_str: str, year_str: str):
    """
        Userstory D:
        
        Gets all the routes that runs from one station to another on a given
        date.
        
        :param start_station: The station of departure
        :param end_station: The station of arrival
        :param day_str: The day of the month (1-30/1)
        :param month_str: Month of the year (1-12)
        :param year_str: The year of the departure
        
        :returns: An table with a overview of the available departures that satisfy the given route.
    """
    day = int(day_str)
    month = int(month_str)
    year = int(year_str)    
    if check_date_fields(day, month, year) == False: 
        return "Failed"
    search_date = date(year, month, day)
    weekday1 = search_date.weekday()
    search_date = search_date + timedelta(days=1)
    weekday2 = search_date.weekday()     
    route_station_times = get_route_station_times()
    route_weekdays = get_route_weekdays()
    routes_on_days = []
    routes_day_1 = []
    routes_day_2 = []
    routes = get_routes()
    for r in routes:
        if r.route_id not in routes_on_days:
            for rw in route_weekdays:
                if rw.route_id == r.route_id:
                    weekday_int = valid_weekdays.index(rw.weekday)
                    on_relevant_day = False
                    if (weekday1 == weekday_int):
                        routes_day_1.append(r.route_id)
                        on_relevant_day = True
                    if (weekday2 == weekday_int):
                        routes_day_2.append(r.route_id)
                        on_relevant_day = True
                    if rw.route_id not in routes_on_days:                                            
                        if on_relevant_day:
                            routes_on_days.append(r.route_id)                            
    routes_between_stations = []    
    for r in routes:
        all_relevant_rst = []
        rst_start = []
        rst_end = []
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
            routes_between_stations.append(r.route_id)
    table = prettytable.PrettyTable(['Route ID', 'Name', 'Operator ID', 'Start Station Name', 'End Station Name', 'Time Of Departure', 'Weekday(s)'])
    relevant_routes = {}
    for r in routes:
        if r.route_id in routes_on_days and r.route_id in routes_between_stations:
            relevant_routes[r.route_id] = r    
    route_times = {}
    print(relevant_routes.keys())
    for r in relevant_routes.values():
        for rst in route_station_times:        
            if (rst.route_id == r.route_id and rst.station_name == start_station and not rst.is_end):
                route_times[r.route_id] = rst.time_of_departure

    sorted(route_times.items(), key=lambda x: x[1])
    for r in route_times.keys():    
        days = ""
        if (r in routes_day_1):
            days = days + " " + valid_weekdays[weekday1]
        if (r in routes_day_2):
            days = days + " " + valid_weekdays[weekday2]
        route = relevant_routes[r]
        table.add_row([r, route.name, route.operator_id, route.start_station_name, route.end_station_name, route_times[r], days])
    return table


def register_customer(name: str, email: str, mobile_number: str):
    """
        Userstory E:
        
        Registers a customer in the database based on the user input
        
        :param name: The name of the user
        :param email: User's email
        :param mobile_number: The users phone number
        :returns: A confirmation of the registration.
    """
    if name == "" or email == "" or mobile_number == "":
        error_handler("All fields must have a value")
        return "Failed"
    customer_id = create_customer(name, email, mobile_number)
    return f"Customer registration for customer: {customer_id} finished"

def get_stations_on_route(route_id: str) -> list[str]:
    """
        Fetches all the stations that is within a train route
                
        :param route_id: The primary key of the ROUTE-table

        :returns: A list of all the stations in a route.
    """
    station_times = get_route_station_times_by_route(int(route_id))
    not_start_or_end = []
    start_station = ""
    end_station = ""
    for st in station_times:        
        if st.is_start:
            start_station = st.station_name
        elif st.is_end:
            end_station = st.station_name
        else:                    
            not_start_or_end.append(st)    
    not_start_or_end.sort(key=lambda x: x.time_of_arrival)    
    sorted_times = [st.station_name for st in not_start_or_end] 
    sorted_times.insert(0, start_station)
    sorted_times.append(end_station)    
    return sorted_times


def get_available_places(route_id: str, day_str: str, month_str: str, year_str: str, start_station: str, end_station: str) -> list[str]:
    """
        Userstory G1
        
        FETCHES all the available seats on a departure. I.e. seats that are not booked.
                
        :param route_id: The primary key of the ROUTE-table
        :param day_str: The day of the month (1-30/1)
        :param month_str: Month of the year (1-12)
        :param year_str: The year of the departure
        :param start_station: The station of departure
        :param end_station: The station of arrival
        

        :returns: A list of all the available seats for the chosen train departure.
    """
    day = int(day_str)
    month = int(month_str)
    year = int(year_str)
    if check_date_fields(day, month, year) == False: 
        return "Failed"
    search_date = date(year, month, day)
    week_nr = search_date.isocalendar()[1]
    weekday = calendar.day_name[search_date.weekday()]
    arranged_cars = get_arranged_cars_by_route(int(route_id))
    car_types = get_car_types()
    is_sleeping = {}
    for a in arranged_cars:
        for c in car_types:            
            if (a.car_type_name == c.name):
                is_sleeping[a.number] = (c.type == "Sleeping")

    orders = get_orders()
    route_stations = get_stations_on_route(route_id)
    start_index = route_stations.index(start_station)
    end_index = route_stations.index(end_station)
    relevant_orders = []
    for o in orders:
        
        if (o.weekday == weekday and o.trip_week_nr == week_nr and o.trip_year == year) and not (end_index <= route_stations.index(o.start_station_name)):
            relevant_orders.append(o)
    places = get_places()
    all_route_places = []
    for a in arranged_cars:
        for p in places:            
            if p.car_type_name == a.car_type_name:
                all_route_places.append(str(a.number) + "-" + str(p.place_no))
    print(all_route_places)    
    ordered_places = []
    for o in relevant_orders:        
        order_places = get_order_places_by_order(o.order_id)
        for p in order_places:
            if is_sleeping[p.car_no] or not (route_stations.index(o.end_station_name) <= start_index):
                ordered_places.append(str(p.car_no) + "-" + str(p.place_no))
                if (is_sleeping[p.car_no]):
                    if ((p.place_no % 2) == 0):
                        ordered_places.append(str(p.car_no) + "-" + str(p.place_no - 1))
                    else:
                        ordered_places.append(str(p.car_no) + "-" + str(p.place_no + 1))

    available_places = []    
    for p in all_route_places:
        if p not in ordered_places:
            type_str = ""
            car_no = int(p.split('-')[0])
            if (is_sleeping[car_no] == True):
                type_str = "Bed"
            else: 
                type_str = "Seat"
            available_places.append(p + "-" + type_str)
    return available_places

def print_available_places(route_id: str, day_str: str, month_str: str, year_str: str, start_station: str, end_station: str):
    """
        Userstory G
        
        PRINTS all the available seats on a departure. I.e. seats that are not booked.
                
        :param route_id: The primary key of the ROUTE-table
        :param day_str: The day of the month (1-30/1)
        :param month_str: Month of the year (1-12)
        :param year_str: The year of the departure
        :param start_station: The station of departure
        :param end_station: The station of arrival
        

        :returns: A table with all of the available seats for the chosen train departure.
    """
    available_places = get_available_places(route_id, day_str, month_str, year_str, start_station, end_station)
    table = prettytable.PrettyTable(['Car No', 'Place No', "Place type"])
    for p in available_places:
        items = p.split('-')
        table.add_row(items)   
    return table


def register_order(customer_id: str, start_station: str, end_station: str, route_id: str, day_str: str, month_str: str, year_str: str, places_str: str):
    """
        Userstory G2
        
        Registers an order for one or more seats/beds on a given departure and route
            
        :param customer_id: The customer - Primary key of the CUSTOMER-table 
        :param start_station: The station of departure
        :param end_station: The station of arrival
        :param route_id: The primary key of the ROUTE-table
        :param day_str: The day of the month (1-30/1)
        :param month_str: Month of the year (1-12)
        :param year_str: The year of the departure
        :param places_str: A string with places to be booked (on the format "CarNo-PlaceNo")
        

        :returns: An order confirmation
    """
    places = places_str.split()
    day = int(day_str)
    month = int(month_str)
    year = int(year_str)   
    if check_date_fields(day, month, year) == False: 
        return "Failed"
    route_date = datetime(year, month, day)
    week_nr = route_date.isocalendar()[1]
    weekday = calendar.day_name[route_date.weekday()]    
    # Creates a short but almost always unique id which is suitable for printing on a physical ticket / reciept             
    start_station = str.capitalize(str.lower(start_station))
    end_station = str.capitalize(str.lower(end_station))    
    if check_week_nr(week_nr) == False or check_weekday(weekday) == False: 
        return "Failed"        

    available_seats_with_type = get_available_places(route_id, day_str, month_str, year_str, start_station, end_station)    
    available_seats = []
    for a in available_seats_with_type:
        items = a.split('-')
        available_seats.append(items[0] + '-' + items[1])
    for p in places:
        if p not in available_seats:
            error_handler(f"Place {p} is already booked.")
            return "Failed"                    
    arranged_cars = get_arranged_cars_by_route(route_id)
    car_types = get_car_types()
    is_sleeping = {}
    for a in arranged_cars:
        for c in car_types:            
            if (a.car_type_name == c.name):
                is_sleeping[a.number] = (c.type == "Sleeping")
    car_type_names = {}
    for a in arranged_cars:
        car_type_names[a.number] = a.car_type_name
    order_id = create_order(int(customer_id), datetime.now(), year, week_nr, start_station, end_station, int(route_id), weekday)  
    for p in places:        
        fields = p.split('-')
        car_no = fields[0]
        place_no = fields[1]
        create_order_place(order_id, car_type_names[int(car_no)], int(place_no), int(car_no))  
    return (f"Registered order with id: {order_id} for places: {', '.join(places)}")
    
def get_future_customer_orders(customer_id: str):
    """
        Userstory H
        
        Gives all the future orders for a given customer
            
        :param customer_id: The customer - Primary key of the CUSTOMER-table 

        :returns: An table with all the customers orders
    """
    orders = get_all_orders_by_customer(int(customer_id))        
    route_station_times = get_route_station_times()    
    now = datetime.now()    
    week_nr = now.date().isocalendar()[1]    
    future_orders = []
    order_place_str = {}
    is_sleeping = {}
    car_types = get_car_types()
    for o in orders:
        for a in get_arranged_cars_by_route(o.route_id):
            for c in car_types:            
                if (a.car_type_name == c.name):
                    key = (str(o.route_id) + "-" + str(a.number))
                    if c.type == "Sleeping":
                        is_sleeping[key] = "Bed"
                    else:
                        is_sleeping[key] = "Chair"
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
        places = get_order_places_by_order(o.order_id)
        place_str = ""
        for p in places:
            place_str = place_str + " " + str(p.car_no) + "-" + str(p.place_no) + "-" + is_sleeping[(str(o.route_id) + "-" + str(p.car_no))]
        order_place_str[o.order_id] = place_str
    table = prettytable.PrettyTable(['Order ID', 'Customer ID', 'Purchase DateTime', 'Trip Year', 'Trip Week Nr', 'Start Station Name', 'End Station Name', 'Route ID', 'Weekday', 'Places (CarNo-PlaceNo)'])        
    for order in future_orders:
        table.add_row([order.order_id, order.customer_id, order.datetime, order.trip_year, order.trip_week_nr, order.start_station_name, order.end_station_name, order.route_id, order.weekday, order_place_str[o.order_id]])
    return table
    