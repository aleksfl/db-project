import sqlite3
from datetime import date, time, datetime
from typing import Optional
from decimal import Decimal

def create_customer(id:str, name: str, email: str, phone_no: str):
    con = sqlite3.connect("main.db")
    cur = con.cursor()
    query = "INSERT INTO CUSTOMER (Name, Email, PhoneNo) VALUES (?, ?, ?)"
    cur.execute(query, (name, email, phone_no))
    con.commit()
    con.close()
    print(f"Inserted customer {name} with email {email} and phone number {phone_no} into the database.")

def create_order(order_id: int, customer_id: int, date_time: datetime, trip_year: int, trip_week_nr: int, start_station_name: str, end_station_name: str, route_id: int, weekday: str):
    con = sqlite3.connect("main.db")
    cur = con.cursor()
    query = "INSERT INTO CUSTOMER_ORDER (OrderID, CustomerID, DateTime, TripYear, TripWeekNr, StartStationName, EndStationName, RouteID, Weekday) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    cur.execute(query, (order_id, customer_id, date_time, trip_year, trip_week_nr, start_station_name, end_station_name, route_id, weekday))
    con.commit()
    con.close()
    print(f"Inserted order with ID {order_id} for customer with ID {customer_id} for trip from {start_station_name} to {end_station_name} on {weekday}, year {trip_year}, week {trip_week_nr} into the database.")        

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
    con = sqlite3.connect("main.db")
    cur = con.cursor()
    query = "SELECT * FROM CUSTOMER_ORDER WHERE CustomerID = ?"
    cur.execute(query, (customer_id,))    
    results = cur.fetchall()
    con.close()
    print(f"Fetched {len(results)} orders for customer {customer_id}")
    # Convert the results into a list of Order objects
    orders = []
    for row in results:
        order = Order(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
        orders.append(order)

    # Return the list of Order objects
    return orders

class RouteStationTime:
    def __init__(self, route_id: int, station_name: str, time_of_arrival: Optional[time], time_of_departure: Optional[time]):
        self.route_id = route_id
        self.station_name = station_name
        self.time_of_arrival = time_of_arrival
        self.time_of_departure = time_of_departure
        self.is_start = time_of_arrival is None and time_of_departure != None
        self.is_end = time_of_departure is None and time_of_arrival != None
        
def get_route_station_times() -> list[RouteStationTime]:
    con = sqlite3.connect("main.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM ROUTE_STATION_TIME")
    route_station_times = []
    results = cur.fetchall()
    print(f"Fetched {len(results)} route station times")
    for row in results:
        time_of_arrival is None
        time_of_departure is None
        if row[2] != None:
            time_of_arrival = datetime.strptime(row[2], '%H:%M:%S').time()
        if row[3] != None:
            time_of_departure = datetime.strptime(row[3], '%H:%M:%S').time()
        route_station_time = RouteStationTime(row[0], row[1], row[2], row[3])
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
    con = sqlite3.connect("main.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM ROUTE")
    results = cur.fetchall()
    print(f"Fetched {len(results)} routes")
    routes = [
        RouteStationTime(row[0], row[1], row[2], row[3], row[4])
        for row in results
    ]
    con.close()
    return routes

class RouteWeekday:
    def __init__(self, route_id: int, weekday: str):
        self.route_id = route_id
        self.weekday = weekday
def get_route_weekdays() -> list[RouteWeekday]:
    con = sqlite3.connect("main.db")
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
    con = sqlite3.connect("main.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM Station")
    results = cur.fetchall()
    print(f"Fetched {len(results)} stations")
    stations = [RouteWeekday(row[0], Decimal(row[1]/10)) for row in results]
    con.close()
    return stations
