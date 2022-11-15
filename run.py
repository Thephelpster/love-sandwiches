import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    Get sales figures input from user.
    run a while loop to collect a valid string of data from the user
    via the terminal, whihc must be a string o 6 number separated by commas. 
    the loop will repeatedly request data until it is valid.
    """
    while True:
        print("please enter sales data from the last market.")
        print("data should be six numbers, seperated by comas.")
        print("example: 10,20,30,40,50,60\n")

        data_str = input("enter your data here: ")

        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("data is valid")
            break
    return sales_data

def validate_data(values):
    """
    inside the try, converts all string values into integers.
    raises valueerror if strings cannot be converted into int,
    or if ther aren't exsactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) !=6:
            raise ValueError(
                f"exactly 6 values required. you provided {len(values)}"
            )
    except ValueError as e:
        print(f"invalid data: {e}, please try again.\n")
        return False

    return True

def update_sales_worksheet(data):
    """
    update sales worksheet, add new row with the list data provided
    """
    print("updated sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("sales worksheet updated successfully.\n")

def update_surplus_worksheet(data):
    """
    update surplus worksheet, add new row with the list data provided
    """
    print("update surplus worksheet...\n")
    surplus_worksheet = SHEET.worksheet("surplus")
    surplus_worksheet.append_row(data)
    print("surplus worksheet updated succesfully.\n")

def calculate_surplus_data(sales_row):
    """
    compare sales with stock and calculate the surplus for each item type.

    the surplus is defined as the sales figure subtracted from the stock:
    -positive surplus indicated waste
    -negative surplus indcated extra made when stock was out.
    """
    print("calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    
    return surplus_data

def main():
    """
    run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    update_surplus_worksheet(new_surplus_data)

print("welcome to love sandwiches automation")
main()