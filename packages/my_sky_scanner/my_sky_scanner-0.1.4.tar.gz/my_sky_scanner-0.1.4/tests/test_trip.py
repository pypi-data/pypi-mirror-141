from datetime import datetime, timedelta
from trip import Flight, Trip, TripError
from unittest import mock
import sky, unittest, pytz, json, os


# This method will be used by the mock to replace requests.get
def mocked_requests_get(*args, **kwargs):

    APP_BASE_PATH = os.environ.get("APP_BASE_PATH")

    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if kwargs["url"] == sky.BOOKING_API_URL:
        with open(APP_BASE_PATH + "res/json/ryanair_response.json", "r") as f:
            json_data = json.load(f)
        return MockResponse(json_data, 200)

    # elif kwargs["url"] == "http://someotherurl.com/anothertest.json":
    #     return MockResponse({"key2": "value2"}, 200)

    return MockResponse(None, 404)


class TestTrip(unittest.TestCase):
    def create_tomorrow_trip(self, one_way: bool, dateOut: str = None, datein: str = None):
        trip = Trip(
            adults=1,
            dateOut=dateOut or datetime.now(pytz.timezone("Europe/Rome")) + timedelta(days=1),
            origin="MXP",
            destination="STN",
        )

        if one_way:
            return trip
        else:
            trip.dateIn = datein or datetime.now(pytz.timezone("Europe/Rome")) + timedelta(days=10)
            return trip

    def test_create_trip_with_no_arguments(self):
        trip: Trip = Trip()
        self.assertEqual(trip.adults, 1)
        self.assertEqual(trip.children, 0)
        self.assertEqual(trip.infants, 0)
        self.assertEqual(trip.teens, 0)
        self.assertEqual(trip.dateIn, "")
        self.assertEqual(trip.dateOut, "")
        self.assertEqual(trip.origin, "")
        self.assertEqual(trip.destination, "")
        self.assertEqual(trip.includeConnectingFlights, "false")
        self.assertEqual(trip.flexDaysBeforeIn, 2)
        self.assertEqual(trip.flexDaysIn, 2)
        self.assertEqual(trip.roundTrip, "false")
        self.assertEqual(trip.flexDaysBeforeOut, 2)
        self.assertEqual(trip.flexDaysOut, 2)
        self.assertEqual(trip.toUs, "AGREED")

    def test_cant_assign_mistyped_date(self):
        trip: Trip = Trip()

        self.assertRaises(ValueError, setattr, trip, "dateOut", "2022-1032")
        self.assertRaises(ValueError, setattr, trip, "dateOut", "2022-10-32")
        self.assertRaises(ValueError, setattr, trip, "dateOut", "2022-2-29")
        self.assertRaises(ValueError, setattr, trip, "dateOut", "2022-30-6")

    def test_cant_book_negative_number(self):
        trip: Trip = Trip()

        self.assertRaises(ValueError, setattr, trip, "adults", -1)

    def test_cant_book_more_than_ten(self):
        trip: Trip = Trip()

        self.assertRaises(ValueError, setattr, trip, "adults", 11)

    def test_assign_date(self):
        trip: Trip = Trip()

        correct_format = "%Y-%m-%d"
        bad_format = "%d-%m-%Y"

        # string
        # today_date = datetime.now(pytz.timezone("Europe/Rome")).strftime("%Y-%m-%d")

        # convert a string to datetime and stringified again changing the format
        # d = datetime.strptime("2011-06-09", "%Y-%m-%d")
        # d.strftime("%d-%m-%Y")

        # datetime object
        today_date = datetime.now(pytz.timezone("Europe/Rome"))
        yesterday_date = datetime.now(pytz.timezone("Europe/Rome")) + timedelta(days=-1)

        # assigning badly formatted date
        self.assertRaises(ValueError, setattr, trip, "dateOut", today_date.strftime(bad_format))

        # assigning yesterday date
        self.assertRaises(ValueError, setattr, trip, "dateOut", yesterday_date)
        self.assertRaises(ValueError, setattr, trip, "dateOut", yesterday_date.strftime(bad_format))
        self.assertRaises(ValueError, setattr, trip, "dateOut", yesterday_date.strftime(correct_format))

        # assigning correctly formatted date
        trip.dateOut = today_date
        self.assertEqual(trip.dateOut, today_date.strftime(correct_format))
        self.assertNotEqual(trip.dateOut, today_date.strftime(bad_format))

        trip2 = Trip()
        trip2.dateOut = today_date.strftime(correct_format)
        self.assertEqual(trip2.dateOut, today_date.strftime(correct_format))

    def test_assign_inDate(self):
        trip: Trip = Trip()
        correct_format = "%Y-%m-%d"
        today_date = datetime.now(pytz.timezone("Europe/Rome"))
        tomorrow_date = datetime.now(pytz.timezone("Europe/Rome")) + timedelta(days=1)
        yesterday_date = datetime.now(pytz.timezone("Europe/Rome")) + timedelta(days=-1)

        trip.dateOut = today_date

        # assigning inDate one day before outDate
        self.assertRaises(ValueError, setattr, trip, "dateIn", yesterday_date)
        self.assertRaises(ValueError, setattr, trip, "dateIn", yesterday_date.strftime(correct_format))

        trip.dateIn = tomorrow_date
        self.assertEqual(trip.dateIn, tomorrow_date.strftime(correct_format))

        trip2: Trip = Trip()
        self.assertRaises(TripError, setattr, trip2, "dateIn", tomorrow_date)

    # test-driven development
    @mock.patch("requests.get", side_effect=mocked_requests_get)
    def test_get_cheapest_flight(self, mock_get):
        trip = self.create_tomorrow_trip(one_way=True)

        all_flights = sky.get_one_day_flights(trip)

        cheapest_flight = sky.get_cheapest_flight(trip)
        cheapest_fare = sky.get_cheapest_fare(cheapest_flight)

        for flight in all_flights:
            for fare in flight["regularFare"]["fares"]:
                self.assertGreaterEqual(fare["amount"], cheapest_fare["regularFare"]["fares"][0]["amount"])

    @mock.patch("requests.get", side_effect=mocked_requests_get)
    def test_get_cheapest_flight_between_two_dates(self, mock_get):

        # TODO da scrivere un test decente

        date1 = datetime.now(pytz.timezone("Europe/Rome")) + timedelta(days=10)
        date2 = datetime.now(pytz.timezone("Europe/Rome")) + timedelta(days=15)
        trip = self.create_tomorrow_trip(one_way=True, dateOut=date1.strftime(sky.DATE_FORMAT))

        flights = sky.get_flights_between_two_dates(trip, date2)
        cheapest_flight = flights[0]

        for flight in flights:
            for fare in flight["regularFare"]["fares"]:
                self.assertGreaterEqual(fare["amount"], cheapest_flight["regularFare"]["fares"][0]["amount"])

        myList = sky.get_flights_object(flights)

        myList1 = sky.get_flights_object(cheapest_flight)

    @mock.patch("requests.get", side_effect=mocked_requests_get)
    def test_get_flex_flight(self, mock_get):

        # TODO da scrivere un test decente

        trip = self.create_tomorrow_trip(True)
        flights = sky.get_cheapest_flight_flex(trip)


if __name__ == "__main__":
    unittest.main()
