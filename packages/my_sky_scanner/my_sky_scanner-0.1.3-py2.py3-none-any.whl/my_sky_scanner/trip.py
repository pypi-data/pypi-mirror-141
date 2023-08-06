from datetime import datetime
import json
import pytz

DATE_FORMAT = "%Y-%m-%d"
ISO86_01_FORMAT_TZ = "%Y-%m-%dT%H:%M:%S.%f%z"
ISO86_01_FORMAT_NO_TZ = "%Y-%m-%dT%H:%M:%S.%f"


class Trip:
    """
    A class used to represent a Trip

    Attributes
    ----------
        adults (:obj:`int`, optional)
            Number of adults (age >= 16)

        teens (:obj:`int`, optional)
            Number of teens (12 <= age <= 15)

        children (:obj:`int`, optional)
            Number of children (2 <= age <= 11)

        infants (:obj:`int`, optional)
            Number of infants (age <= 2)

        dateIn (:obj:`string`, optional)
            Return flight date, blank means no return flight
            format -> "yyyy-mm-dd"

        dateOut (:obj:`string`)
            Departure flight date
            format -> "yyyy-mm-dd"

        destination (:obj:`string`)
            The iata code of the destination airport

        origin (:obj:`string`)
            The iata code of the origin airport

        includeConnectingFlights (:obj:`string` 'true'|'false')
            if false only looks for fast-track, otherwise looks for indirect flights

        flexDaysBeforeIn (:obj:`int`, optional, range [0,3])
            Specify how flexible is your return date (before)
            example: if FlexDaysBeforeIn=3 and DateIn='2010-10-25' you will receive flights infos of 24, 23 and 22 October 2010

        flexDaysIn  (:obj:`int`, optional, range [0,3])
            Specify how flexible is your return date (after)
            example: if FlexDaysIn=3 and DateIn='2010-10-25' you will receive flights infos of 26, 27 and 28 October 2010

        roundTrip (:obj:`string` 'true'|'false')
            it must be set to true if want to get return flights info, false otherwise

        flexDaysBeforeOut (:obj:`int`, optional, range [0,3])
            Specify how flexible is your departure date (before)
            example: if FlexDaysBeforeOut=3 and DateOut='2010-10-20' you will receive flights infos of 19, 18 and 17 October 2010

        flexDaysOut (:obj:`int`, optional, range [0,3])
            Specify how flexible is your departure date (after)
            example: if FlexDaysOut=3 and DateOut='2010-10-20' you will receive flights infos of 21-22-23 October 2010

    Methods
    -------
    says(sound=None)
        Prints the animals name and what sound it makes
    """

    def __init__(
        self,
        adults=None,
        teens=None,
        children=None,
        infants=None,
        dateOut=None,
        dateIn=None,
        origin=None,
        destination=None,
        includeConnectingFlights=None,
        flexDaysBeforeIn=None,
        flexDaysIn=None,
        roundTrip=None,
        flexDaysBeforeOut=None,
        flexDaysOut=None,
        toUs=None,
    ) -> None:
        self._adults = adults or 1
        self._teens = teens or 0
        self._children = children or 0
        self._infants = infants or 0
        self._dateOut = dateOut or ""
        self._dateIn = dateIn or ""
        self._origin = origin or ""
        self._destination = destination or ""
        self._includeConnectingFlights = includeConnectingFlights or "false"
        self._flexDaysBeforeIn = flexDaysBeforeIn or 2
        self._flexDaysIn = flexDaysIn or 2
        self._roundTrip = roundTrip or "false"
        self._flexDaysBeforeOut = flexDaysBeforeOut or 2
        self._flexDaysOut = flexDaysOut or 2
        self._toUs = toUs or "AGREED"

    @property
    def adults(self):
        return self._adults

    @adults.setter
    def adults(self, how_many_adt):
        if how_many_adt < 0:
            raise ValueError("Can't search a trip for a negative number of person")
        elif how_many_adt > 10:
            raise ValueError("Can't search a trip for more than 10 people")
        self._adults = how_many_adt

    @property
    def teens(self):
        return self._teens

    @teens.setter
    def teens(self, how_many_teen):
        if how_many_teen < 0:
            raise ValueError("Can't search a trip for a negative number of person")
        self._teens = how_many_teen

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, how_many_chd):
        if how_many_chd < 0:
            raise ValueError("Can't search a trip for a negative number of children")
        self._children = how_many_chd

    @property
    def infants(self):
        return self._infants

    @infants.setter
    def infants(self, how_many_inf):
        if how_many_inf < 0:
            raise ValueError("Can't search a trip for a negative number of person")
        self._infants = how_many_inf

    @property
    def dateOut(self):
        return self._dateOut

    @dateOut.setter
    def dateOut(self, dateOut: datetime | str):

        format = "%Y-%m-%d"

        if dateOut == "":
            self._dateOut = ""
        elif isinstance(dateOut, datetime):
            if dateOut.date() >= datetime.now(pytz.timezone("Europe/Rome")).date():
                self._dateOut = dateOut.strftime(format)
            else:
                raise ValueError("You can't travel in time, do you? Please insert a valid date")
        else:
            time_error = False
            try:
                if bool(datetime.strptime(dateOut, format)):
                    if datetime.strptime(dateOut, format).date() >= datetime.now(pytz.timezone("Europe/Rome")).date():
                        self._dateOut = dateOut
                    else:
                        time_error = True
                        raise ValueError()

            except ValueError:
                if time_error:
                    raise ValueError("You can't travel in time, do you? Please insert a valid date")
                else:
                    raise ValueError("The date you inserted is not valid, format requested 'YYYY-MM-DD' ")

    @property
    def dateIn(self):
        return self._dateIn

    @dateIn.setter
    def dateIn(self, dateIn: datetime | str):

        format = "%Y-%m-%d"
        if dateIn == "":
            self._dateIn = ""
        elif self.dateOut == "":
            raise TripError("You need to set the departure date before setting the return date")
        elif isinstance(dateIn, datetime):
            if dateIn.date() >= datetime.strptime(self._dateOut, format).date():
                self._dateIn = dateIn.strftime(format)
                self._roundTrip = "True"
            else:
                raise ValueError("You can't come back before you even go. Please insert a valid date")

        else:
            time_error = False
            try:
                if bool(datetime.strptime(dateIn, format)):
                    if datetime.strptime(dateIn, format).date() >= datetime.strptime(self._dateOut, format).date():
                        self._dateIn = dateIn
                        self._roundTrip = "True"
                    else:
                        time_error = True
                        raise ValueError()

            except ValueError:
                if time_error:
                    raise ValueError("You can't travel in time, do you? Please insert a valid date")
                else:
                    raise ValueError("The date you inserted is not valid, format requested 'YYYY-MM-DD' ")

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, origin):
        self._origin = origin

    @property
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, destination):
        self._destination = destination

    @property
    def includeConnectingFlights(self):
        return self._includeConnectingFlights

    @includeConnectingFlights.setter
    def flexDaysBeforeIn(self, includeConnectingFlights):
        self._includeConnectingFlights = includeConnectingFlights

    @property
    def flexDaysBeforeIn(self):
        return self._flexDaysBeforeIn

    @flexDaysBeforeIn.setter
    def flexDaysBeforeIn(self, flexDaysBeforeIn):
        self._flexDaysBeforeIn = flexDaysBeforeIn

    @property
    def flexDaysIn(self):
        return self._flexDaysIn

    @flexDaysIn.setter
    def flexDaysIn(self, flexDaysIn):
        self._flexDaysIn = flexDaysIn

    @property
    def roundTrip(self):
        return self._roundTrip

    @roundTrip.setter
    def roundTrip(self, roundTrip):
        self._roundTrip = roundTrip

    @property
    def flexDaysBeforeOut(self):
        return self._flexDaysBeforeOut

    @flexDaysBeforeOut.setter
    def flexDaysBeforeOut(self, flexDaysBeforeOut):
        self._flexDaysBeforeOut = flexDaysBeforeOut

    @property
    def flexDaysOut(self):
        return self._flexDaysOut

    @flexDaysOut.setter
    def flexDaysOut(self, flexDaysOut):
        self._flexDaysOut = flexDaysOut

    @property
    def toUs(self):
        return self._toUs

    @toUs.setter
    def toUs(self, toUs):
        self._toUs = toUs

    def toString(self):
        return (
            "Trip info\n"
            + "Origin: "
            + self.origin
            + "\nDestination: "
            + self.destination
            + "\nAdults: "
            + str(self.adults)
            + "\nChildren: "
            + str(self.children)
            + "\nDeparture date: "
            + self.dateOut
            + "\nReturn date: "
            + self.dateIn
        )

    def get_dateOut(self) -> datetime:
        return datetime.strptime(self.dateOut, DATE_FORMAT)

    def get_dateIn(self) -> datetime:
        return datetime.strptime(self.dateIn, DATE_FORMAT)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class TripError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Flight:
    """
    A class used to represent a Flight

    Attributes
    ----------
        flightKey (:obj:`str`, optional)
            The flight's key

        flightOperator (:obj:`str`, optional)
            The flight operator

        flightNumber (:obj:`str`, optional)
            The flight number

        takeOffLocalTime (:obj:`datetime`, optional)
            Number of infants (age <= 2)

        landingLocalTime (:obj:`datetime`, optional)
            Return flight date, blank means no return flight
            format -> "yyyy-mm-dd"

        takeOffUTC (:obj:`datetime`, optional)
            Departure flight date
            format -> "yyyy-mm-dd"

        landingUTC (:obj:`datetime`, optional)
            The iata code of the destination airport

        adtFareAmount (:obj:`float`, optional)
            The iata code of the origin airport

    """

    def __init__(
        self,
        flightKey=None,
        flightOperator=None,
        flightNumber=None,
        takeOffLocalTime=None,
        landingLocalTime=None,
        takeOffUTC=None,
        landingUTC=None,
        adtFareAmount=None,
    ) -> None:
        self._flightKey = flightKey
        self._flightOperator = flightOperator
        self._flightNumber = flightNumber
        self._takeOffLocalTime = (
            takeOffLocalTime
            if isinstance(takeOffLocalTime, datetime)
            else datetime.strptime(takeOffLocalTime, ISO86_01_FORMAT_NO_TZ)
        )
        self._landingLocalTime = (
            landingLocalTime
            if isinstance(landingLocalTime, datetime)
            else datetime.strptime(landingLocalTime, ISO86_01_FORMAT_NO_TZ)
        )
        self._takeOffUTC = (
            takeOffUTC if isinstance(takeOffUTC, datetime) else datetime.strptime(takeOffUTC, ISO86_01_FORMAT_TZ)
        )
        self._landingUTC = (
            landingUTC if isinstance(landingUTC, datetime) else datetime.strptime(landingUTC, ISO86_01_FORMAT_TZ)
        )
        self._adtFareAmount = adtFareAmount

    @property
    def flightKey(self):
        return self._flightKey

    @flightKey.setter
    def flightKey(self, key):
        self._flightKey = key

    @property
    def flightOperator(self):
        return self._flightOperator

    @flightOperator.setter
    def flightOperator(self, operator):
        self._flightOperator = operator

    @property
    def flightNumber(self):
        return self._flightNumber

    @flightNumber.setter
    def flightNumber(self, number):
        self._flightNumber = number

    @property
    def takeOffLocalTime(self):
        return self._takeOffLocalTime

    @takeOffLocalTime.setter
    def takeOffLocalTime(self, time):
        self._takeOffLocalTime = datetime.strptime(time, ISO86_01_FORMAT_NO_TZ)

    @property
    def landingLocalTime(self):
        return self._landingLocalTime

    @landingLocalTime.setter
    def landingLocalTime(self, time):
        self._landingLocalTime = datetime.strptime(time, ISO86_01_FORMAT_NO_TZ)

    @property
    def takeOffUTC(self):
        return self._takeOffUTC

    @takeOffUTC.setter
    def takeOffUTC(self, time):
        self._takeOffUTC = datetime.strptime(time, ISO86_01_FORMAT_TZ)

    @property
    def landingUTC(self):
        return self._landingUTC

    @landingUTC.setter
    def landingUTC(self, time):
        self._landingUTC = datetime.strptime(time, ISO86_01_FORMAT_TZ)

    @property
    def adtFareAmount(self):
        return self._adtFareAmount

    @adtFareAmount.setter
    def adtFareAmount(self, amount):
        self._adtFareAmount = amount

    def __str__(self):
        return (
            "Flight key: "
            + self.flightKey
            + "\nFlight Operator: "
            + self.flightOperator
            + "\nFlight Number: "
            + self.flightNumber
            + "\nTake-off local time: "
            + datetime.strftime(self.takeOffLocalTime, ISO86_01_FORMAT_NO_TZ)
            + "\nLanding local time: "
            + datetime.strftime(self.landingLocalTime, ISO86_01_FORMAT_NO_TZ)
            + "\nTake-off UTC time: "
            + datetime.strftime(self.takeOffUTC, ISO86_01_FORMAT_TZ)
            + "\nLanding UTC time: "
            + datetime.strftime(self.landingUTC, ISO86_01_FORMAT_TZ)
            + "\nCost: "
            + str(self.adtFareAmount)
        )
