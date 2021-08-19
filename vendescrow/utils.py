import datetime
import os
import random
import string
import re

import math
from django.core.mail import EmailMessage
from django.utils import timezone
from django.utils.text import slugify
from django.utils.html import strip_tags
from twilio.rest import Client

from vendescrow import email_settings


def get_last_month_data(today):
    """
    Simple method to get the datetime objects for the
    start and end of last month.
    """
    this_month_start = datetime.datetime(today.year, today.month, 1)
    last_month_end = this_month_start - datetime.timedelta(days=1)
    last_month_start = datetime.datetime(last_month_end.year, last_month_end.month, 1)
    return last_month_start, last_month_end


def get_trial_days():
    return timezone.now() + timezone.timedelta(days=30)


def addDays(date_, num_of_days):
    return date_ + timezone.timedelta(days=num_of_days)


def get_fileType(filepath):
    import os
    filename, file_extension = os.path.splitext(filepath)
    return file_extension


def get_month_data_range(months_ago=1, include_this_month=False):
    """
    A method that generates a list of dictionaries
    that describe any given amount of monthly data.
    """
    today = datetime.datetime.now().today()
    dates_ = []
    if include_this_month:
        # get next month's data with:
        next_month = today.replace(day=28) + datetime.timedelta(days=4)
        # use next month's data to get this month's data breakdown
        start, end = get_last_month_data(next_month)
        dates_.insert(0, {
            "start": start.timestamp(),
            "end": end.timestamp(),
            "start_json": start.isoformat(),
            "end": end.timestamp(),
            "end_json": end.isoformat(),
            "timesince": 0,
            "year": start.year,
            "month": str(start.strftime("%B")),
        })
    for x in range(0, months_ago):
        start, end = get_last_month_data(today)
        today = start
        dates_.insert(0, {
            "start": start.timestamp(),
            "start_json": start.isoformat(),
            "end": end.timestamp(),
            "end_json": end.isoformat(),
            "timesince": int((datetime.datetime.now() - end).total_seconds()),
            "year": start.year,
            "month": str(start.strftime("%B"))
        })
    # dates_.reverse()
    return dates_


def get_filename(path):  # /abc/filename.mp4
    return os.path.basename(path)


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_id_generator(instance):
    """
    This is for a Django project with an key field
    """
    size = random.randint(30, 45)
    key = random_string_generator(size=size)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=key).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return key


def unique_key_generator(instance):
    """
    This is for a Django project with an key field
    """
    size = random.randint(30, 45)
    key = random_string_generator(size=size)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(transaction_key=key).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return key


def unique_order_id_generator(instance):
    """
    This is for a Django project with an order_id field
    """
    order_new_id = random_string_generator()

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(order_id=order_new_id).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return order_new_id


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        try:
            slug = slugify(instance.user)
        except Exception as e:
            slug = slugify(instance.trade_creator.username)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=15)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def unique_slug_generator_by_email(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    slug = new_slug if new_slug is not None else slugify(instance.email)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(email=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator_by_email(instance, new_slug=new_slug)
    return slug


def unique_slug_by_name(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    slug = new_slug if new_slug is not None else slugify(instance.name)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def digitExtract(char):
    return ''.join(filter(str.isdigit, char))
    # return re.findall(r'\d+', char) - would return data as a list encapsulated data


def removeNCharFromString(num_of_char, string_data):
    size = len(string_data)
    # Slice string to remove last N characters from string
    return string_data[:size - num_of_char]


def secondWordExtract(char):
    """
    extract the second word from a string sequence
    :type char: str
    """
    return char.split(' ', 2)[1]


def switch_month(month):
    switcher = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12,
    }
    return switcher.get(month, "Invalid Argument")


def count_words(html_string):
    # html_string = """
    # <h1>This is a title</h1>
    # """
    word_string = strip_tags(html_string)
    matching_words = re.findall(r'\w+', word_string)
    return len(matching_words)


def get_read_time(html_string):
    count = count_words(html_string)
    read_time_min = math.ceil(count / 200.0)  # assuming 200wpm reading
    # read_time_sec = read_time_min * 60
    # read_time = str(datetime.timedelta(seconds=read_time_sec))
    # read_time = str(datetime.timedelta(minutes=read_time_min))
    return int(read_time_min)


def round_decimals_down(number: float, decimals: int = 5):
    """
    Returns a value rounded down to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return math.floor(number)

    factor = 10 ** decimals
    return math.floor(number * factor) / factor


# Send SMS Using Twilio
def send_sms(message_body: str, recipient_phone: str) -> str:
    account_sid = "AC9b3f94478614261fe94d83274dff3969"
    auth_token = "7ff3d4e8d5ba35196c9613cecbaf2336"
    client = Client(account_sid, auth_token)
    message = client.messages.create(body=message_body,from_='+16099105791',to=recipient_phone)
    return message.sid


# Send Email Using Sendgrid
def send_email(subject: str, html, recipient_list: list):
    message = EmailMessage(
        subject, html, email_settings.EMAIL_HOST_USER, recipient_list
    )
    message.fail_silently = False
    message.send()