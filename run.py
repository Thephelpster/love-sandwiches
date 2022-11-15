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

#def update_sales_worksheet(data):
#    """
#    update sales worksheet, add new row with the list data provided
#    """
#    print("updated sales worksheet...\n")
#    sales_worksheet = SHEET.worksheet("sales")
#    sales_worksheet.append_row(data)
#    print("sales worksheet updated successfully.\n")

#def update_surplus_worksheet(data):
#    """
#    update surplus worksheet, add new row with the list data provided
#    """
#    print("update surplus worksheet...\n")
#    surplus_worksheet = SHEET.worksheet("surplus")
#    surplus_worksheet.append_row(data)
#    print("surplus worksheet updated succesfully.\n")

def update_worksheet(data, worksheet):
    """
    recieves a list of integers to be inserted into a worksheet
    update the relevant worksheet with the data provided
    """
    print(f"updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")


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

def get_last_5_entries_sales():
    """
    collects collums of data from sales worksheet,collecting
    the last 5 entries for each sandwich and returns the data
    as a list of lists
    """    
    sales = SHEET.worksheet("sales")

    columns = []
    for ind in range(1,7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    
    return columns

def calculate_stock_data(data):
    """
    calculate the average stock for each item type,adding 10%
    """
    print("calculating stock data...")
    new_stock_data = []
    
    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data

def main():
    """
    run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")

print("welcome to love sandwiches automation")
main()

