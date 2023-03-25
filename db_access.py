import sqlite3
from datetime import date, time, datetime
from typing import Optional
from decimal import Decimal

DB_PATH = "train.db"

def create_customer(name: str, email: str, phone_no: str) -> int: 
    """
        Creates a customer entity in the database

        :param name: The name of the user
        :param email: Email of the user
        :param phone_no: Phone number of the user
        
        :return: returns the customer_id of the user entity
    """
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    query = "INSERT INTO CUSTOMER (Name, Email, PhoneNo) VALUES (?, ?, ?)"
    cur.execute(query, (name, email, phone_no))
    customer_id = cur.lastrowid
    con.commit()
    con.close()
    print(f"Inserted customer with id {customer_id} and name {name} with email {email} and phone number {phone_no} into the database.")
    return customer_id

def create_order(customer_id: int, date_time: datetime, trip_year: int, trip_week_nr: int, start_station_name: str, end_station_name: str, route_id: int, weekday: str):
    """
        Creates a order entity in the database

        :param customer_id: The customer buying the ticket
        :param date_time: date_time object for when the ticket should be valid
        :param trip_year: What year the ticket is valid
        :param trip_week_nr: Week number 1-52
        :param start_station_name: First valid station of the ticket
        :param end_station_name: Last valid station for the ticket
        :param route_id: The RouteID of the route the ticket is purchased for
        :param weekday: Monday, Tuesday....
        
        :return: returns the order_id of the order entity
    """
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    query = "INSERT INTO CUSTOMER_ORDER (CustomerID, DateTime, TripYear, TripWeekNr, StartStationName, EndStationName, RouteID, Weekday) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    cur.execute(query, (customer_id, date_time, trip_year, trip_week_nr, start_station_name, end_station_name, route_id, weekday))
    order_id = cur.lastrowid
    con.commit()
    con.close()
    print(f"Inserted order with ID {order_id} for customer with ID {customer_id} for trip from {start_station_name} to {end_station_name} on {weekday}, year {trip_year}, week {trip_week_nr} into the database.")        
    return order_id

class Order:
    """
        Order is the class containing information about a train-ticket.
    """
    def __init__(self, order_id: int, customer_id: int, date_time: datetime, trip_year: int, trip_week_nr: int, start_station_name: str, end_station_name: str, route_id: int, weekday: str):
        """
            Constructs a RouteStationTime Object

            :param order_id: The primary key of the order table
            :param customer_id: The tickets owner
            :param date_time: Date for the ticket
            :param trip_year: The year the ticket is valid
            :param trip_week_nr: Week number (1-52)
            :param start_station_name: Start station for the ticket
            :param end_station_name: End station for the ticket
            :param route_id: The route the order is placed for
            :param weekday: The day e.g. Monday, Tuesday..
            
            :return: returns nothing
        """
        self.order_id = order_id
        self.customer_id = customer_id
        self.datetime = date_time
        self.trip_year = trip_year
        self.trip_week_nr = trip_week_nr
        self.start_station_name = start_station_name
        self.end_station_name = end_station_name
        self.route_id = route_id
        self.weekday = weekday


def get_all_orders_by_customer(customer_id: int) -> list[Order]:
    """
        Constructs a RouteStationTime Object
        :param customer_id: The tickets owner
        
        :return: returns a list with the orders for a given customer
    """
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    query = "SELECT * FROM CUSTOMER_ORDER WHERE CustomerID = ?"
    cur.execute(query, (customer_id,))    
    results = cur.fetchall()
    con.close()
    print(f"Fetched {len(results)} orders for customer {customer_id}")    
    orders = []
    for row in results:
        order = Order(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
        orders.append(order)

    # Return the list of Order objects
    return orders

def get_orders() -> list[Order]:
    """
        Fetches all the customer orders in the database
        
        :return: returns a list with all customers orders
    """
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()    
    cur.execute('SELECT * FROM CUSTOMER_ORDER')    
    results = cur.fetchall()
    con.close()
    print(f"Fetched {len(results)} orders")    
    orders = []
    for row in results:
        order = Order(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
        orders.append(order)
    
    return orders

class RouteStationTime:
    """
        RouteStationTime is creating a object to keep track of the respective instances in the SQLite database.
    """
    def __init__(self, route_id: int, station_name: str, time_of_arrival: Optional[time], time_of_departure: Optional[time]):
        """
            Constructs a RouteStationTime Object

            :param route_id: The primary key of the route table
            :param station_name: Name of the station
            :param time_of_arrival: Arrival time of the train
            :param time_of_departure: Departure time of the train
            
            :return: returns nothing
        """
        self.route_id = route_id
        self.station_name = station_name
        self.time_of_arrival = time_of_arrival
        self.time_of_departure = time_of_departure
        self.is_start = time_of_arrival is None and time_of_departure != None
        self.is_end = time_of_departure is None and time_of_arrival != None
        
def get_route_station_times() -> list[RouteStationTime]:
    """
        Fetches  the departures for all stations in the database
        
        :return: returns a list with all departures
    """
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT * FROM ROUTE_STATION_TIME")
    route_station_times = []
    results = cur.fetchall()
    print(f"Fetched {len(results)} route station times")
    for row in results:
        time_of_arrival = None
        time_of_departure = None
        if row[2] != None:
            time_of_arrival = datetime.strptime(row[2], '%H:%M:%S').time()
        if row[3] != None:
            time_of_departure = datetime.strptime(row[3], '%H:%M:%S').time()
        route_station_time = RouteStationTime(row[0], row[1], time_of_arrival, time_of_departure)
        route_station_times.append(route_station_time)
    con.close()
    return route_station_times

def get_route_station_times_by_route(route_id: int) -> list[RouteStationTime]:
    """
        Fetches all the departures for a given route
        
        :return: returns a list with the departure for a route
    """
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(f"SELECT * FROM ROUTE_STATION_TIME WHERE RouteID = {route_id}")
    route_station_times = []
    results = cur.fetchall()
    print(f"Fetched {len(results)} route station times")
    for row in results:
        time_of_arrival = None
        time_of_departure = None
        if row[2] != None:
            time_of_arrival = datetime.strptime(row[2], '%H:%M:%S').time()
        if row[3] != None:
            time_of_departure = datetime.strptime(row[3], '%H:%M:%S').time()
        route_station_time = RouteStationTime(row[0], row[1], time_of_arrival, time_of_departure)
        route_station_times.append(route_station_time)
    con.close()
    return route_station_times

class Route:
    """
        A Route instance keeps track of the information about a route entity in the database
    """
    def __init__(self, route_id: int, name: str, operator_id: int, start_station_name: str, end_station_name: str):
        """
            Constructs a RouteStationTime Object

            :param route_id: The primary key of the route table
            :param name: Name of the route
            :param operator: The primary key of the OPERATOR-table
            :param start_station: First station for the route
            :param end_station: Last station for the route
            
            :return: returns nothing
        """
        self.route_id = route_id
        self.name = name
        self.operator_id = operator_id
        self.start_station_name = start_station_name
        self.end_station_name = end_station_name
        
def get_routes() -> list[Route]:
    """
        Fetches all the routes from the database
        
        :return: a list of Routes.
    """
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT * FROM ROUTE")
    results = cur.fetchall()
    routes = [
        Route(row[0], row[1], row[2], row[3], row[4]) for row in results
    ]
    con.close()
    return routes

class RouteWeekday:
    """
        RouteWeekDay tells us if a route is operator on a given Weekday
    """
    def __init__(self, route_id: int, weekday: str):
        """
            Constructor for the RouteWeekDay object
            
            :param route_id: The primary key of the ROUTE-table
            :param weekday: A weekday e.g. Monday Tuesday..
            
            :returns: returnsnothing.
        """
        self.route_id = route_id
        self.weekday = weekday
        
def get_route_weekdays() -> list[RouteWeekday]:
    """
        Fetches all the RouteWeekDay instances from the database 
        
        :returns: A list of the weekdays the routes are operating.
    """
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT * FROM ROUTE_WEEKDAY")
    results = cur.fetchall()
    print(f"Fetched {len(results)} route weekdays")
    route_weekdays = [RouteWeekday(row[0], row[1]) for row in results]
    con.close()
    return route_weekdays

class Station:
    """
        Station holds the information about the STATION-entities in the database
    """
    def __init__(self, name: str, altitude: Decimal):
        """
            Constructor for the Station object
            
            :param name: Name of the train station
            :param altitude: Height above sea level in meters
            
            :returns: returnsnothing.
        """
        self.name = name
        self.altitude = altitude

def get_stations() -> list[Station]:
    """
        Fetches all the Station-instances from the database 
        
        :returns: A list of all the registered stations.
    """
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT * FROM Station")
    results = cur.fetchall()
    print(f"Fetched {len(results)} stations")
    stations = [Station(row[0], Decimal(row[1]/10)) for row in results]
    con.close()
    return stations

class OrderPlace:
    """
        Keeps track of the places that are ordered for a order
    """
    def __init__(self, order_id: int, car_type_name: str, place_no: int, car_no: int):
        """
            Constructor for OrderPlace instances in the database
            
            :param order_id: The primary key of the order-table
            :param car_type_name: If the car is a seating car or a sleeping car
            :param place_no: what place number is reserved 
            :param car_no: Which car in the arrangment is containing the reserved seat
            
            :returns: returnsnothing.
        """
        self.order_id = order_id
        self.car_type_name = car_type_name
        self.place_no = place_no
        self.car_no = car_no

def get_order_places() -> list[OrderPlace]:
    """
        Fetches all the reserved places registered in the database
        
        :returns: A list of the reserved places.
    """
    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()

    cursor.execute("SELECT * FROM ORDER_PLACE")
    results = cursor.fetchall()
    print(f"Fetched {len(results)} order places")
    order_places = [OrderPlace(row[0], row[1], row[2], row[3]) for row in results]
    con.close()
    return order_places

def get_order_places_by_order(order_id: int) -> list[OrderPlace]:
    """
        Fetches all the reserved seats for a given order
        
        :param order_id: The primary key of the order-table
        
        :returns: A list of the reserved seat on a order.
    """
    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()
    cursor.execute("SELECT * FROM ORDER_PLACE WHERE OrderID = ?", (order_id, ))
    results = cursor.fetchall()
    print(f"Fetched {len(results)} order places for order id {order_id}")
    order_places = [OrderPlace(row[0], row[1], row[2], row[3]) for row in results]
    con.close()
    return order_places

def create_order_place(order_id: int, car_type_name: str, place_no: int, car_no: int):
    """
        Creates an entity in the database for ORDER_PLACE.
        
        :param order_id: The primary key of the order-table
        :param car_type_name: If the car is a seating car or a sleeping car
        :param place_no: what place number is reserved 
        :param car_no: Which car in the arrangment is containing the reserved seat
        
        :returns: nothing.
    """
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    query = "INSERT INTO ORDER_PLACE (OrderID, CarTypeName, PlaceNo, CarNo) VALUES (?, ?, ?, ?)"
    cur.execute(query, (order_id, car_type_name, place_no, car_no))
    con.commit()
    con.close()
    print(f"Inserted order place for order {order_id} car_type_name {car_type_name} place_no {place_no} car_no {car_no}")


class Place:
    """
        Place is equivalent to a seat or a bed on a train car
    """
    def __init__(self, car_type_name: str, place_no: int):  
        """
            Constructor for a Place object
            
            :param car_type_name: If the car is a seating car or a sleeping car
            :param place_no: The number for a seat or a bed.
        
            :returns: nothing.
            
        """      
        self.car_type_name = car_type_name
        self.place_no = place_no        

def get_places() -> list[Place]:
    """
        Fetches all the places registered in the database
    
        :returns: A list of all places in the cars.
    """  
    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()

    cursor.execute("SELECT * FROM PLACE")
    results = cursor.fetchall()
    print(f"Fetched {len(results)} car places")
    places = [Place(row[0], row[1]) for row in results]
    con.close()
    return places

class ArrangedCar:
    """
        ArrangedCar is the car-setting for a given route 
    """  
    def __init__(self, route_id: int, number: int, car_type_name: str):
        """
            Fetches all the places registered in the database
            
            :param route_id: The primary key of the ROUTE-table
            :param number: The order of the car in the car-setting/layout i.e. 1 is the first car...
            :car_type_name: If the car is a seating car or a sleeping car
        
            :returns: A list of all places in the cars.
        """          
        self.route_id = route_id
        self.number = number
        self.car_type_name = car_type_name               

def get_arranged_cars_by_route(route_id: int) -> list[ArrangedCar]:
    """
        Fetches the layout of the cars for a route
        
        :param route_id: The primary key of the ROUTE-table

        :returns: A list of the arranged cars for a route.
        """    
    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()

    cursor.execute("SELECT * FROM ARRANGED_CAR WHERE RouteID = ?", (route_id,))
    results = cursor.fetchall()
    print(f"Fetched {len(results)} arranged cars for route id {route_id}")
    places = [ArrangedCar(row[0], row[1], row[2]) for row in results]
    con.close()
    return places

class CarType:
    """
        CarType tells us if the car is a sleeping car or a seating car
    """
    def __init__(self, name: str, type: str, no_rows: int, no_seats_in_row: int, no_compartments: int):
        """
            Constructor for the CarType objects
            
            :param name: The name of the car (SJ-chair car1 or SJ-sleeping car1)
            :param type: If the car is a sleeping car or a seating car
            :param no_rows: Numbers of rows of chairs in a seating car
            :param no_seats_in_row: Numbers of seats in a row for a seating car
            :param no_compartments: Number of sleeping compartments in a sleeping car. NULL if seating
            
            :returns: nothing
        """
        self.name = name
        self.type = type
        self.no_rows = no_rows
        self.no_seats_in_row = no_seats_in_row
        self.no_compartments = no_compartments
        
def get_car_types() -> list[CarType]:
    """
        Fetches all the car_types from the database
        
        :returns: A list with the cartypes available in the database.
    """
    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()

    cursor.execute("SELECT * FROM CAR_TYPE")
    results = cursor.fetchall()
    print(f"Fetched {len(results)} car typse")
    car_types = [CarType(row[0], row[1], row[2], row[3], row[4]) for row in results]
    con.close()
    return car_types