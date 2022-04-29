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

sales = SHEET.worksheet('sales')
data = sales.get_all_values()

def get_sales_data():
    """
    Get sales data from the user
    """
    while True:
        print('Please enter sales data from the last market')
        print('The sales data must be six numbers, separated by a comma')
        print('Example: 10, 20, 30, 40, 50, 60\n')

        data_str = input('Enter your data here: ')

        sales_data = data_str.split(',')
        print(sales_data)

        if validate_data(sales_data):
            print('Data valid!')
            break
    return sales_data

def validate_data(values):
    """
    Inside try, convert all string values to integers.
    Raise ValueError if strings cannot be converted to int, 
    or len of string not equal to 6
    """

    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f'Exactly 6 values required, you provided only {len(values)}'
                )
    except ValueError as e:
        print(f'Invalid data: {e}, Please try again.\n')
        return False
    return True

# def update_sales_worksheet(data):
#     """
#     Function to update the sales worksheet
#     """
#     print('Updating sales worksheet...\n')
#     sales_worksheet = SHEET.worksheet('sales')
#     sales_worksheet.append_row(data)
    
#     print('Sales worksheet updated successfully\n')

# def update_surplus_worksheet(data):
#     """
#     Add function to update the surplus worksheet
#     """

#     print('Updating surplus data\n')
#     surplus_worksheet = SHEET.worksheet("surplus")
#     surplus_worksheet.append_row(data)
#     print('Surplus data updated successfully')

def update_worksheet(data, worksheet):

    """
    Function to accept calculated data and update the respective worksheet
    """
    print(f'Updating {worksheet} data...\n')
    updating_worksheet = SHEET.worksheet(worksheet)
    updating_worksheet.append_row(data)
    print(f'{worksheet} data updated successfully\n')


def calculate_surplus_data(sales_row):
    """
    Function to calculate surplus
    """
    print('Calculating surplus data...\n')
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]
    surplus_row = []
    for stock, sale in zip(stock_row, sales_row):
        surplus = int(stock) - sale 
        surplus_row.append(surplus)
    return surplus_row

def get_last_5_entries_sales():
    """
    Function to get the last 5 sales entries
    
    """
    print('Getting the last 5 sales entries...\n')
    sales = SHEET.worksheet('sales')
    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns   

def calculate_stock_data(data):
    """
    Function to calculate the average of the last sales entries  and return it
    as stock data
    """
    print('Calculating stock data...\n')
    new_stock_data = []
    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        new_stock_data.append(round(average * 1.1))
    return new_stock_data
  

def main():
    """
    Run all programme
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, 'sales')

    surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(surplus_data, 'surplus')
    last_5_entries_sales = get_last_5_entries_sales()
    stock_data = calculate_stock_data(last_5_entries_sales)
    update_worksheet(stock_data, 'stock')
    

print('Welcome to Love Sandwiches Data Automation!')
main()

