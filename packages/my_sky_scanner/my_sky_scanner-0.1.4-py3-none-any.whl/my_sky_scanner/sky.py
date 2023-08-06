"""
My Sky Scanner
~~~~~~~~~~~~

This module is an API wrapper for the ryanair api (maybe some others airline companies in the future)

:copyright: no copyright
:license: MIT, see LICENSE for more details.

"""

import requests
from datetime import datetime, timedelta

from trip import Flight, Trip, TripError

BOOKING_API_URL = "https://www.ryanair.com/api/booking/v4/en-gb/availability"
DATE_FORMAT = "%Y-%m-%d"
ISO86_01_FORMAT_TZ = "%Y-%m-%dT%H:%M:%S.%f%z"
ISO86_01_FORMAT_NO_TZ = "%Y-%m-%dT%H:%M:%S.%f"


def get_raynair_info(trip: Trip):
    """Get all the flight available for a given trip

    Args:
        trip (Trip): A trip containing all the infos needed to make the api call

    Returns:
        _type_: _description_
    """

    params = prepare_params(trip)

    resp = requests.get(url=BOOKING_API_URL, params=params)
    data = resp.json()

    return data


def get_cheapest_flight(trip: Trip):
    """
    Return the cheapest flight for a given trip

    flight["regularFare"]["fares"][i]["cheapest"] tag added


    Args:
        trip (Trip): _description_

    Returns:
        _type_: _description_
    """

    params = prepare_params(trip)

    params["FlexDaysBeforeOut"] = 0
    params["FlexDaysOut"] = 0

    resp = requests.get(url=BOOKING_API_URL, params=params)
    data = resp.json()

    outTrip = data["trips"][0]["dates"][0]

    cheapest_flight = get_mock_flight()

    for flight in outTrip["flights"]:
        for fare in flight["regularFare"]["fares"]:
            if fare["type"] == "ADT" and fare["amount"] < cheapest_flight["regularFare"]["fares"][0]["amount"]:
                fare["cheapest"] = 1
                cheapest_flight = flight
            else:
                fare["cheapest"] = 0

    return cheapest_flight


def get_one_day_flights(trip: Trip):
    """Retrieve all the flight for a giver trip leaving the airport in the dateOut, no flex

    Args:
        trip (Trip): A trip
    """

    params = prepare_params(trip)

    params["DateIn"] = ""
    params["FlexDaysBeforeIn"] = 0
    params["FlexDaysIn"] = 0
    params["FlexDaysBeforeOut"] = 0
    params["FlexDaysOut"] = 0
    params["RoundTrip"] = "false"

    resp = requests.get(url=BOOKING_API_URL, params=params)
    data = resp.json()

    # currency = data["currency"]  # use this for the current currency

    return data["trips"][0]["dates"][0]["flights"]


def get_flights_list(trip: Trip):
    """
    Return all the flights for a given trip in a list in chronological order

    Args:
        trip (Trip): _description_

    Returns:
        _type_: _description_
    """

    params = prepare_params(trip)

    resp = requests.get(url=BOOKING_API_URL, params=params)
    data = resp.json()

    # currency = data["currency"]  # use this for the current currency

    flights = []

    for date in data["trips"][0]["dates"]:
        for flight in date["flights"]:
            flights.append(flight)

    return flights


def get_flights_between_two_dates(trip: Trip, date2: datetime | str):
    """
        This method gets all the flight between the trip.dateOut and the date2
        sorted from the cheapest to the most expansive


    Args:
        trip (:obj:`Trip`): a trip

        date2 (:obj:`datetime` | :obj:`str`):

    Returns:
        :obj:`list`: All the flights in the timespan given
    """

    params = prepare_params(trip)

    if not isinstance(date2, datetime):
        if not bool(datetime.strptime(date2, DATE_FORMAT)):
            raise TripError("The date you inserted is not valid, format requested 'YYYY-MM-DD' ")
        else:
            date2 = datetime.strptime(date2, DATE_FORMAT)

    date1 = trip.get_dateOut()
    diff = (date2.date() - date1.date()).days

    all_flights = []

    if diff < 0:
        # date2 is before outDate
        # it doesn't make any sense
        return all_flights

    for x in range(diff + 1):
        all_flights_one_day = get_one_day_flights(trip)
        all_flights.extend(all_flights_one_day)

        # update trip.dateOut with following day
        date1 = date1 + timedelta(days=1)
        trip.dateOut = date1

    sorted = sort_cost_asc(all_flights)
    return sorted


def get_cheapest_flight_flex(trip: Trip):
    """
        This method gets all the available flights for the trip.outDate
        and takes into accounte the flex parameters before and after
        the departure date

        Returned flights list sorted from the cheapest to the most expensive


    Args:
        trip (:obj:`Trip`): a trip

    Returns:
        :obj:`list`: All the flights available
    """

    params = prepare_params(trip)

    resp = requests.get(url=BOOKING_API_URL, params=params)
    data = resp.json()

    flights = [flight for date in data["trips"][0]["dates"] for flight in date["flights"]]

    sorted = sort_cost_asc(flights)
    return sorted


### utils method ###
def get_cheapest_fare(flight):

    # Questo metodo potrebbe essere inutile visto che anche se ogni "flight" puo avere diverse "fares"
    # in realtà queste si differenziano solo per il "type"
    # Es: se cerco un volo solo per un adulto, allora avrè una sola fare mentre se lo cerco per un adulto
    #       e un bambino allora len["fares"] == 2 e ["fares"][0]["type"] == "ADT" e ["fares"][0]["type"] == "CHD"

    """If a given flight has more than one regular fare, than remove every fare except for the cheapest

    Args:
        :obj:`dict` : flight

    Returns:
        :obj:`dict` : flight with only one fare, the cheapest
    """

    for fare in flight["regularFare"]["fares"]:
        if fare["cheapest"] == 0:
            flight["regularFare"]["fares"].remove(fare)

    return flight


def get_mock_flight():
    """Build a flight tuple with the same structure as the one retrieved fron the api

    Returns:
        :obj:`dict`: a flight with no info and with one fare set to 999999
    """

    return dict({"regularFare": {"fares": [{"amount": 999999}]}})


def sort_cost_asc(flights: list):
    """Sort a list of flights, from the cheapest to the most expensive

    Args:
        :obj:`list`(:obj:`dict`) : a list of flights

    Returns:
        :obj:`list`(:obj:`dict`) : the sorted list
    """

    return sorted(flights, key=lambda f: f["regularFare"]["fares"][0]["amount"])


def get_flights_object(flights: list | dict):
    """Build flight object from the list passed as args and return in list

    Args:
        :obj:`list`(:obj:`dict`) || :obj:`dict` : a list of flights

    Returns:
        :obj:`list`(:obj:`Flight`) : a list of all the flights given as parameter
    """

    # se passo un solo oggetto inve di una lista lo metto in una lista
    # e lo preparo per l'iterazione successiva
    if not isinstance(flights, list):
        flights = [flights]

    flights_list = []

    for flight in flights:
        flights_list.append(
            Flight(
                flightKey=flight["flightKey"],
                flightOperator=flight["operatedBy"],
                flightNumber=flight["flightNumber"],
                takeOffLocalTime=flight["time"][0],
                landingLocalTime=flight["time"][1],
                takeOffUTC=flight["timeUTC"][0],
                landingUTC=flight["timeUTC"][1],
                adtFareAmount=flight["regularFare"]["fares"][0]["amount"],
            )
        )

    return flights_list


def prepare_params(trip: Trip):

    return dict(
        ADT=trip.adults,
        CHD=trip.children,
        DateIn=trip.dateIn,
        DateOut=trip.dateOut,
        Destination=trip.destination,
        Origin=trip.origin,
        TEEN=trip.teens,
        IncludeConnectingFlights=trip.includeConnectingFlights,
        FlexDaysBeforeIn=trip.flexDaysBeforeIn,
        FlexDaysIn=trip.flexDaysIn,
        RoundTrip=trip.roundTrip,
        FlexDaysBeforeOut=trip.flexDaysBeforeOut,
        FlexDaysOut=trip.flexDaysOut,
        ToUs=trip.toUs,
    )
