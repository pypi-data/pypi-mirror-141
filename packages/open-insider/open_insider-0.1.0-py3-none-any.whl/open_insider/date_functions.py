import pandas as pd

def date_28d(date_x):
    
    '''
    Docstring: Return the date for 28 days from a given date
    
    :param date_x: The given date to start counting from
    :type date_x: date

    '''
    return date_x + pd.Timedelta(f"{28} days")