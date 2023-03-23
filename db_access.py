import sqlite3
from datetime import date, datetime
con = sqlite3.connect("railway.db")

def create_customer(id:str, name: str, email: str, phone_no: str):
    pass

def create_order(order_id: int, customer_id: int, date_time: datetime, trip_year: int, trip_week_kr: int, start_station_name: str, end_station_name: str, route_id: int, weekday: str):
    pass
