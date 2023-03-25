valid_weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def error_handler(msg: str):
    print("The following error occured with your query: " + msg)    

def check_weekday(weekday):
    if weekday not in valid_weekdays:
        error_handler("Invalid weekday: " + weekday)

def check_date_fields(day: int, month: int, year: int):    
    if day > 31 or day < 1:
        error_handler("Invalid date day: " + str(day))
    if month > 12 or month < 1:
        error_handler("Invalid date month: " + str(month))
    if year > 3000 or month < 1800:
        error_handler("Invalid date year: " + str(year))

def check_week_nr(week_nr: int):
    if week_nr > 53 or week_nr < 1:
        error_handler("Invalid week_nr: " + str(week_nr))
