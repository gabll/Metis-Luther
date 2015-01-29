import datetime as dt

def iso_year_start(iso_year):
    "The gregorian calendar date of the first day of the given ISO year"
    fourth_jan = dt.date(iso_year, 1, 4)
    delta = dt.timedelta(fourth_jan.isoweekday()-1)
    return fourth_jan - delta 

def iso_to_gregorian(iso_year, iso_week, iso_day):
    "Gregorian calendar date for the given ISO year, week and day"
    year_start = iso_year_start(iso_year)
    return year_start + dt.timedelta(days=iso_day-1, weeks=iso_week-1)

def get_season(release_date):
    """Return the season given release date
    release_date: datetime.date object
    Season limits in: http://boxofficemojo.com/about/boxoffice.htm"""
    year = release_date.year
    #Winter season
    first_winter_day = iso_to_gregorian(year, 2, 0)
    last_winter_day = dt.date(year,3,1)
    while not last_winter_day.weekday() == 3:
        last_winter_day += dt.timedelta(days=1)
    if release_date >= first_winter_day and release_date <= last_winter_day:
        return "Winter"
    #Spring season
    first_spring_day = last_winter_day + dt.timedelta(days=1)
    last_spring_day = dt.date(year,5,1)
    while not last_spring_day.weekday() == 3:
        last_spring_day += dt.timedelta(days=1)
    if release_date >= first_spring_day and release_date <= last_spring_day:
        return "Spring"
    #Summer season
    first_summer_day = last_spring_day + dt.timedelta(days=1)
    last_summer_day = dt.date(year,9,1)
    while not last_summer_day.weekday() == 0:
        last_summer_day += dt.timedelta(days=1)
    if release_date >= first_summer_day and release_date <= last_summer_day:
        return "Summer"
    #Fall season
    first_fall_day = last_summer_day + dt.timedelta(days=1)
    last_fall_day = dt.date(year,11,1)
    while not last_fall_day.weekday() == 3:
        last_fall_day += dt.timedelta(days=1)
    if release_date >= first_fall_day and release_date <= last_fall_day:
        return "Fall"
    #Holiday season
    return "Holiday"
