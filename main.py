import sqlite3
import os
from commands import get_all_station_routes, get_routes_between_stations, register_customer, get_available_seats, register_order, get_future_customer_orders
import colorama
from colorama import Fore

print('''
      \t**********************************************
      \t***     Railway service DB application     ***
      \t**********************************************
      ''')

def print_choices() -> str:
    print(Fore.YELLOW + '''
    1. See all routes

    2. Get routes between stations

    3. Register a customer

    4. See available seats

    5. Register an order
        
    6. Get orders by customer

    7. Quit
            ''')
    return input(f"{Fore.RED}    Enter number here: ")

def userinput_gco() -> list[str]:
    return input(f"{Fore.GREEN} Customer Number: "), input(f"{Fore.GREEN} Customer Number: ")


def userinput_grbs() -> list[str]:
    return input(f"{Fore.GREEN} Start Station: "), input(f"{Fore.GREEN} End Station: "), input(f"{Fore.GREEN} Day: "), input(f"{Fore.GREEN} Month: "), input(f"{Fore.GREEN} Year: ")

def userinput_rc() -> list[str]:
    return input(f"{Fore.GREEN} Customer Number: "), input(f"{Fore.GREEN} Name: "), input(f"{Fore.GREEN} Email: "), input(f"{Fore.GREEN} Mobile No.: ")

def userinput_gas() -> list[str]:
    return input(f"{Fore.GREEN} Route ID: "), input(f"{Fore.GREEN} Day: "), input(f"{Fore.GREEN} Month: "), input(f"{Fore.GREEN} Year: ")

def userinput_ro() -> list[str]:
    return input(f"{Fore.GREEN} Start Station: "), input(f"{Fore.GREEN} End Station: ") , input(f"{Fore.GREEN} Route ID: "), input(f"{Fore.GREEN} Day: "), input(f"{Fore.GREEN} Month: "),input(f"{Fore.GREEN} Year: "), input(f"{Fore.GREEN} Place 1: "), input(f"{Fore.GREEN} Place 2: ")

def userinput_gasr() -> list[str]:
    return input(f"{Fore.GREEN} Customer Number: "), input(f"{Fore.GREEN} Customer Number: ")



if __name__ == "__main__":
    choice = print_choices()
    while choice != "quit":
        if choice == "1":
            print(Fore.BLUE + get_all_station_routes(*userinput_gasr()))
            choice = print_choices()
        if choice == "2":
            print(Fore.BLUE + get_routes_between_stations(*userinput_grbs))
            choice = print_choices()
        if choice == "3":
            print(Fore.BLUE + register_customer(*userinput_rc()))
            choice = print_choices()
        if choice == "4":
            print(Fore.BLUE + get_available_seats(*userinput_gas()))
            choice = print_choices()
        if choice == "5":       
            print(Fore.BLUE + get_routes_between_stations(*userinput_ro()))
            choice = print_choices()
        if choice == "6":        
            print(get_future_customer_orders(*userinput_gco()))
            choice = print_choices()
        if choice.lower() == "quit":
            quit
        
        