from calendar import monthrange
from datetime import date
from dateutil.relativedelta import relativedelta


def get_last_date_in_month(day: date):
    return day + relativedelta(
        day=monthrange(date.today().year, date.today().month)[1]
    )