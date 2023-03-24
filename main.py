import sqlite3
import os
from commands import get_all_station_routes, get_routes_between_stations, register_customer, get_available_seats, register_order, get_future_customer_orders

print('''
      \t**********************************************
      \t***     Railway service DB application     ***
      \t**********************************************
      ''')

def print_choices() -> None:
    print('''
    1. Seperate words by single space

    2. get_routes_between_stations start_station end_station day month year

    3. register_customer customer_number name email mobile_number

    4. get_available_seats route_id day month year"

    5. register_order customer_number start_station end_station route_id day month year place1 place2.
        For 5. a place consists of the car no. and the place no. joined by a hyphen, i.e carnr-placenr
        Minimum 1 place
        
    6. get_customer_orders customer_number

    7. quit
            ''')

print_choices()
choice = ""

while choice != "quit":
    args = choice.split()
    if choice.lower().startswith("get_all_station_routes"):
        print(get_all_station_routes(args[1], args[2]))        
    if choice.lower().startswith("get_routes_between_stations"):
        print(get_routes_between_stations(args[1], args[2], args[3], args[4], args[5]))
    if choice.lower().startswith("register_customer"):
        print(register_customer(args[1], args[2], args[3], args[4]))        
    if choice.lower().startswith("get_available_seats"):
        print(get_available_seats(args[1], args[2], args[3], args[4]))    
    if choice.lower().startswith("register_order"):        
        print(get_routes_between_stations(args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[7:]))
    if choice.lower().startswith("get_customer_orders"):        
        print(get_future_customer_orders(args[1]))