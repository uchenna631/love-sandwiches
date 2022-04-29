import gspread
from google.oauth2.service_account import Credentials

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
    
data = get_sales_data()