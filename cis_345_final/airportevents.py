from time import strftime

class AirportQuery:

    def __init__(self, airport_name, departing=True, delay_list=[]):

        # Init instance vars
        current_datetime = strftime("%Y-%m-%d %H:%M:%S")

        self.airport_name = airport_name
        self.query_time = current_datetime
        self.departing = departing
        self.delay_list = delay_list

    # Getters
    @property
    def airport_name(self):
        return self.__airport_name
    
    @property
    def query_time(self):
        return self.__query_time
    
    @property
    def departing(self):
        return self.__departing
    
    @property
    def delay_list(self):
        return self.__delay_list
    
    # Setters
    @airport_name.setter
    def airport_name(self, new_name):
        self.__airport_name = new_name

    @query_time.setter
    def query_time(self, new_time):
        self.__query_time = new_time

    @departing.setter
    def departing(self, new_departing):
        self.__departing = new_departing

    @delay_list.setter
    def delay_list(self, new_delay_list):
        self.__delay_list = new_delay_list

    def __str__(self):
        return f'{self.query_time}\n{self.airport_name} (Departing: {self.departing})\n{self.delay_list}'