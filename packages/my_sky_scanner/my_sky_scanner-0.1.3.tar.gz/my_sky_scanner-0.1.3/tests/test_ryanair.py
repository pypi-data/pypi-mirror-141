import unittest
from sky import Trip, get_raynair_info


class TestRyanair(unittest.TestCase):
    def test_api_call_is_returning_flight(self):

        trip: Trip = Trip(10, 0, 0, 0, "2022-6-10", None, "MXP", "SUF")
        json = get_raynair_info(trip)

        self.assertNotEqual(0, len(json["trips"]))


if __name__ == "__main__":
    unittest.main()
