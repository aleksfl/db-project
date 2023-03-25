import sqlite3
from datetime import date, time, datetime
from typing import Optional
from decimal import Decimal

DB_PATH = "train.db"

def create_customer(name: str, email: str, phone_no: str):
    """
    Creates a customer entity in the database

    :param route_id: The primary key of the route table
    :param station_name: Name of the station
    :param time_of_arrival: Arrival time of the train
    :param time_of_departure: Departure time of the train
    
    :return: returns nothing
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
    def __init__(self, order_id: int, customer_id: int, date_time: datetime, trip_year: int, trip_week_nr: int, start_station_name: str, end_station_name: str, route_id: int, weekday: str):
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
    def __init__(self, route_id: int, name: str, operator_id: int, start_station_name: str, end_station_name: str):
        self.route_id = route_id
        self.name = name
        self.operator_id = operator_id
        self.start_station_name = start_station_name
        self.end_station_name = end_station_name
        
def get_routes() -> list[Route]:
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
    def __init__(self, route_id: int, weekday: str):
        self.route_id = route_id
        self.weekday = weekday
def get_route_weekdays() -> list[RouteWeekday]:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT * FROM ROUTE_WEEKDAY")
    results = cur.fetchall()
    print(f"Fetched {len(results)} route weekdays")
    route_weekdays = [RouteWeekday(row[0], row[1]) for row in results]
    con.close()
    return route_weekdays

class Station:
    def __init__(self, name: str, altitude: Decimal):
        self.name = name
        self.altitude = altitude

def get_stations() -> list[Station]:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT * FROM Station")
    results = cur.fetchall()
    print(f"Fetched {len(results)} stations")
    stations = [Station(row[0], Decimal(row[1]/10)) for row in results]
    con.close()
    return stations

class OrderPlace:
    def __init__(self, order_id: int, car_type_name: str, place_no: int, car_no: int):
        self.order_id = order_id
        self.car_type_name = car_type_name
        self.place_no = place_no
        self.car_no = car_no

def get_order_places() -> list[OrderPlace]:
    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()

    cursor.execute("SELECT * FROM ORDER_PLACE")
    results = cursor.fetchall()
    print(f"Fetched {len(results)} order places")
    order_places = [OrderPlace(row[0], row[1], row[2], row[3]) for row in results]
    con.close()
    return order_places

def get_order_places_by_order(order_id: int) -> list[OrderPlace]:
    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()
    cursor.execute("SELECT * FROM ORDER_PLACE WHERE OrderID = ?", (order_id, ))
    results = cursor.fetchall()
    print(f"Fetched {len(results)} order places for order id {order_id}")
    order_places = [OrderPlace(row[0], row[1], row[2], row[3]) for row in results]
    con.close()
    return order_places

def create_order_place(order_id: int, car_type_name: str, place_no: int, car_no: int):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    query = "INSERT INTO ORDER_PLACE (OrderID, CarTypeName, PlaceNo, CarNo) VALUES (?, ?, ?, ?)"
    cur.execute(query, (order_id, car_type_name, place_no, car_no))
    con.commit()
    con.close()
    print(f"Inserted order place for order {order_id} car_type_name {car_type_name} place_no {place_no} car_no {car_no}")


class Place:
    def __init__(self, car_type_name: str, place_no: int):        
        self.car_type_name = car_type_name
        self.place_no = place_no        

def get_places() -> list[Place]:
    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()

    cursor.execute("SELECT * FROM PLACE")
    results = cursor.fetchall()
    print(f"Fetched {len(results)} car places")
    places = [Place(row[0], row[1]) for row in results]
    con.close()
    return places

class ArrangedCar:
    def __init__(self, route_id: int, number: int, car_type_name: str):        
        self.route_id = route_id
        self.number = number
        self.car_type_name = car_type_name               

def get_arranged_cars_by_route(route_id: int) -> list[ArrangedCar]:
    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()

    cursor.execute("SELECT * FROM ARRANGED_CAR WHERE RouteID = ?", (route_id,))
    results = cursor.fetchall()
    print(f"Fetched {len(results)} arranged cars for route id {route_id}")
    places = [ArrangedCar(row[0], row[1], row[2]) for row in results]
    con.close()
    return places

class CarType:
    def __init__(self, name: str, type: str, no_rows: int, no_seats_in_row: int, no_compartments: int):
        self.name = name
        self.type = type
        self.no_rows = no_rows
        self.no_seats_in_row = no_seats_in_row
        self.no_compartments = no_compartments
def get_car_types() -> list[CarType]:
    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()

    cursor.execute("SELECT * FROM CAR_TYPE")
    results = cursor.fetchall()
    print(f"Fetched {len(results)} car typse")
    car_types = [CarType(row[0], row[1], row[2], row[3], row[4]) for row in results]
    con.close()
    return car_types