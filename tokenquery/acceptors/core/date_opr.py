import datetime
import dateutil.parser

# date  (Iso format)
# '2013-12-25T19:20:41.391393'


def date_is(token_input, operation_input):
    # simple version compare two strings
    if 'T' in token_input:
        date1 = token_input.split('T')[0]
    else:
        date1 = token_input

    if 'T' in operation_input:
        date2 = operation_input.split('T')[0]
    else:
        date2 = operation_input

    if date1 == date2:
        return True

    return False


def date_is_after(token_input, operation_input):
    # simple version compare two strings
    if 'T' in token_input:
        date1 = token_input.split('T')[0]
    else:
        date1 = token_input

    if 'T' in operation_input:
        date2 = operation_input.split('T')[0]
    else:
        date2 = operation_input

    if date1 > date2:
        return True

    return False


def date_is_before(token_input, operation_input):
    # simple version compare two strings
    if 'T' in token_input:
        date1 = token_input.split('T')[0]
    else:
        date1 = token_input

    if 'T' in operation_input:
        date2 = operation_input.split('T')[0]
    else:
        date2 = operation_input

    if date1 < date2:
        return True

    return False


def date_y_is(token_input, operation_input):
    if 'T' in token_input:
        date1 = token_input.split('T')[0]
        year = date1.split('-')[0]
    else:
        year = token_input.split('-')[0]

    if year == operation_input:
        return True
    return False


def date_m_is(token_input, operation_input):
    if 'T' in token_input:
        date1 = token_input.split('T')[0]
        month = date1.split('-')[1]
    else:
        month = token_input.split('-')[1]
    if month == operation_input:
        return True
    return False


def date_d_is(token_input, operation_input):
    if 'T' in token_input:
        date1 = token_input.split('T')[0]
        day = date1.split('-')[2]
    else:
        day = token_input.split('-')[2]
    if day == operation_input:
        return True
    return False

# def date_is_x_days_before(token_input, operation_input):
#     # utc = pytz.UTC
#     # publish_date = dateutil.parser.parse(selected_date)
#     # event_start = utc.localize(dateutil.parser.parse(event_start_date))
#     # margin = datetime.timedelta(days=margin_days)
#     # if event_start - margin <= publish_date
#     #     return True
#     # else:
#     #     return False
