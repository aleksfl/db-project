from commands import get_all_station_routes, get_routes_between_stations, print_available_places, register_customer, get_available_places, register_order, get_future_customer_orders
from colorama import Fore

print('''
      \t**********************************************
      \t***     Railway service DB application     ***
      \t**********************************************2
      ''')

def print_choices() -> str:
    print(Fore.YELLOW + '''
    1. See all routes for a station

    2. Get routes between stations

    3. Register a customer

    4. See available places

    5. Register an order
        
    6. Get orders by customer

    7. Quit
            ''')
    return input(f"{Fore.RED}    Enter number here: ")



"""

    Input function for the user interface

"""

def userinput_gco() -> list[str]:
    return input(f"{Fore.GREEN} Customer Number: ")


def userinput_grbs() -> list[str]:
    return input(f"{Fore.GREEN} Start Station: "), input(f"{Fore.GREEN} End Station: "), input(f"{Fore.GREEN} Day: "), input(f"{Fore.GREEN} Month: "), input(f"{Fore.GREEN} Year: ")

def userinput_rc() -> list[str]:
    return input(f"{Fore.GREEN} Name: "), input(f"{Fore.GREEN} Email: "), input(f"{Fore.GREEN} Mobile No.: ")

def userinput_gas() -> list[str]:
    return input(f"{Fore.GREEN} Route ID: "), input(f"{Fore.GREEN} Day: "), input(f"{Fore.GREEN} Month: "), input(f"{Fore.GREEN} Year: "), input(f"{Fore.GREEN} Start Station: "), input(f"{Fore.GREEN} End Station: ")

def userinput_ro() -> list[str]:
    return (
        input(f"{Fore.GREEN} CustomerID: "),
        input(f"{Fore.GREEN} Start Station: "),
        input(f"{Fore.GREEN} End Station: "),
        input(f"{Fore.GREEN} Route ID: "),
        input(f"{Fore.GREEN} Day: "),
        input(f"{Fore.GREEN} Month: "),
        input(f"{Fore.GREEN} Year: "),
        input(f"{Fore.GREEN} Seats <CarNo-PlaceNo> seperated by space: "),
    )

def userinput_gasr() -> list[str]:
    return input(f"{Fore.GREEN} Station: "), input(f"{Fore.GREEN} Weekday: ")


"""

    Main entry point 

"""

if __name__ == "__main__":
    choice = print_choices()
    while choice != "quit":
        if choice == "1":
            print(Fore.BLUE, get_all_station_routes(*userinput_gasr()))
            choice = print_choices()
        if choice == "2":
            print(Fore.BLUE, get_routes_between_stations(*userinput_grbs()))
            choice = print_choices()
        if choice == "3":
            print(Fore.BLUE, register_customer(*userinput_rc()))
            choice = print_choices()
        if choice == "4":
            print(Fore.BLUE, print_available_places(*userinput_gas()))
            choice = print_choices()
        if choice == "5":       
            print("Give seats / beds as CarNo-PlaceNo separated by spaces")
            print(Fore.BLUE, register_order(*userinput_ro()))
            choice = print_choices()
        if choice == "6":        
            print(get_future_customer_orders(*userinput_gco()))
            choice = print_choices()
        if choice == "7":
            exit()
        
        