import sqlite3
import os
from commands import get_all_station_routes, get_routes_between_stations, register_customer, get_available_seats, register_order, get_future_customer_orders

print("\t**********************************************")
print("\t***  Railway service DB application  ***")
print("\t**********************************************")

def print_choices():
    print("Seperate words by single space")
    print("1. get_all_station_routes station weekday")
    print("2. get_routes_between_stations start_station end_station day month year")
    print("3. register_customer customer_number name email mobile_number")
    print("4. get_available_seats route_id day month year")
    print("5. register_order customer_number start_station end_station route_id day month year place1 place2....")
    print("For 5. a place consists of the car number and the place number joined by a hyphen, i.e carnr-placenr")
    print("Minimum 1 place")    
    print("6. get_future_customer_orders customer_number")
    print("7. quit")

print_choices()
choice = ""

while choice != "quite":
    args = choice.split()
    if choice.startswith("get_all_station_routes"):
        print(get_all_station_routes(args[1], args[2]))        
    if choice.startswith("get_routes_between_stations"):
        print(get_routes_between_stations(args[1], args[2], args[3], args[4], args[5]))
    if choice.startswith("register_customer"):
        print(register_customer(args[1], args[2], args[3], args[4]))        
    if choice.startswith("get_available_seats"):
        print(get_available_seats(args[1], args[2], args[3], args[4]))    
    if choice.startswith("register_order"):        
        print(get_routes_between_stations(args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[7:]))
    if choice.startswith("get_customer_orders"):        
        print(get_future_customer_orders(args[1]))