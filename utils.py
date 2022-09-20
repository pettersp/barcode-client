from datetime import datetime

DATE_FORMAT_DATABASE = '%a, %d %b %Y %H:%M:%S GMT'
DATE_FORMAT_GUI = '%d. %B %Y'


def format_price_for_gui(price):
    return str(price) + ' NOK'


def format_date_for_gui(date):
    dt_obj = datetime.strptime(date, DATE_FORMAT_DATABASE)
    return dt_obj.strftime(DATE_FORMAT_GUI)


def convert_to_display_text(elem):
    return str(elem).replace('_', ' ').capitalize()


def calculate_num_days_in_fridge(purchase_date):
    dt_obj = datetime.strptime(purchase_date, DATE_FORMAT_DATABASE)
    delta = datetime.today() - dt_obj
    return delta.days