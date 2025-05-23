from datetime import datetime

def clean_currency(item: str) -> float:
    '''
    remove anything from the item that prevents it from being converted to a float
    '''    
    return float(str(item).replace('$', '').replace(',', ''))

def extract_year_mdy(timestamp):
    '''
    use the datatime.strptime to parse the date and then extract the year
    '''
    try:
        return datetime.strptime(timestamp, '%m/%d/%Y %H:%M:%S').year
    except (ValueError, TypeError):
        return None

def clean_country_usa(item: str) ->str:
    '''
    This function should replace any combination of 'United States of America', USA' etc.
    with 'United States'
    '''
    if not isinstance(item, str):
        return item
    item_cleaned = item.strip().lower()
    possibilities = ['united states of america', 'usa', 'us', 'united states', 'u.s.']
    if item_cleaned in possibilities:
        return 'United States'
    return item.strip()


if __name__=='__main__':
    print("""
        Add code here if you need to test your functions
        comment out the code below this like before sumbitting
        to improve your code similarity score.""")

