import pytest
from airportevents import AirportQuery

class TestAirportQuery:
    def test_details(self):
        a1 = AirportQuery('PHX', False, [])
        print('Testing details of AirportQuery 1')
        assert('PHX', False, []) == (a1.airport_name, a1.departing, a1.delay_list)

        a2 = AirportQuery("LAX", True, ['TestDelay'])
        print('Testing details of AirportQuery 2')
        assert("LAX", True, ['TestDelay']) == (a2.airport_name, a2.departing, a2.delay_list)

        a3 = AirportQuery("", False, [])
        print('Testing details of AirportQuery 3')
        assert("", False, []) == (a3.airport_name, a3.departing, a3.delay_list)

if __name__ == "__main__":
  pytest.main()  # Run tests if script is executed directly