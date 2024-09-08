# Ammar Mand CIS345 Tu/Th 10:30-11:45 Final GUI
import json
import requests
from bs4 import BeautifulSoup
from tkinter import *
from PIL import Image, ImageTk
from airportevents import *

# File we will store query results in
log_file_name = "queries.json"

# Functions to parse specific delay types...

"""
DTD for airport closure lists (from FAA)
<!ELEMENT Airport_Closure_List         (Airport*)>
<!ELEMENT Airport                      (ARPT, Reason, Start, Reopen)>
"""
def parse_airport_closures(airport_name, closure_list_tag):

  master_closure_list = []

  # Loop through the Airport elements
  airport_tags = closure_list_tag.find_all("airport")
  for cur_airport in airport_tags:

    # Check the airport name against our target
    if cur_airport.find("arpt").text.strip().lower() == airport_name.lower():

        # Grab the 3 attributes: closure reason, start and reopen datetimes
        cur_closure_dict = {
            "type" : "airport_closure",
            "reason" : cur_airport.find("reason").text.strip(),
            "start" : cur_airport.find("start").text.strip(),
            "reopen" : cur_airport.find("reopen").text.strip()
        }

        # Append to master
        master_closure_list.append(cur_closure_dict)

  return master_closure_list

"""
DTD for ground stop lists (from FAA)
<!ELEMENT Ground_Stop_List             (Program*)>
<!ELEMENT Program                      (ARPT, Reason, End_Time)>
"""
def parse_ground_stops(airport_name, groundstop_list_tag):

  master_stop_list = []

  # Loop through Program elements
  program_tags = groundstop_list_tag.find_all("program")
  for stop_program in program_tags:

    # Check the airport name against our target
    if stop_program.find("arpt").text.strip().lower() == airport_name.lower():

        # Grab reason and end time
        cur_stop_dict = {
            "type" : "ground_stop",
            "reason" : stop_program.find("reason").text.strip(),
            "endtime" : stop_program.find("end_time").text.strip()
        }

        # Append to master
        master_stop_list.append(cur_stop_dict)

  return master_stop_list

"""
DTD for ground delay lists (from FAA)
<!ELEMENT Ground_Delay_List            (Ground_Delay*)>
<!ELEMENT Ground_Delay                 (ARPT, Reason, Avg, Max)>
"""
def parse_ground_delays(airport_name, grounddelay_list_tag):

  master_grounddelay_list = []

  # Loop through Ground_Delay elements
  ground_delay_tags = grounddelay_list_tag.find_all("ground_delay")
  for ground_delay in ground_delay_tags:

    # Check the airport name against our target
    if ground_delay.find("arpt").text.strip().lower() == airport_name.lower():

        # Get reason, average delay, max delay
        cur_ground_delay = {
            "type" : "ground_delay",
            "reason" : ground_delay.find("reason").text.strip(),
            "avg" : ground_delay.find("avg").text.strip(),
            "max" : ground_delay.find("max").text.strip()
        }

        # Append
        master_grounddelay_list.append(cur_ground_delay)

  return master_grounddelay_list

"""
DTD for arrival/departure delay lists (from FAA)
<!ELEMENT Arrival_Departure_Delay_List (Delay*)>
<!ELEMENT Delay                        (ARPT, Reason, Arrival_Departure, Arrival_Departure?)>

<!ELEMENT Arrival_Departure            (Min, Max, Trend)>
<!ATTLIST Arrival_Departure Type       (Arrival|Departure) #REQUIRED>
"""
def parse_ad_delays(airport_name, is_departing, ad_list_tag):

  master_list = []

  # Loop through the Delay elements
  delay_tags = ad_list_tag.find_all("delay")
  for cur_delay in delay_tags:

    # Check the airport name against our target
    if cur_delay.find("arpt").text.strip().lower() == airport_name.lower():

        # As in the DTD excerpt and XML example above, there is a separate substructure for delays to arrivals and delays to departure (whichever exist(s))
        # We will extract the information (Min, Max, and Trend) from each into a subdictionary
        cur_ad_dict = {
            "type" : "arrival_departure_delay",
            "reason" : "",
            "arrival_delay" : {},
            "departure_delay" : {}

        }

        # Grab the delay reason
        cur_ad_dict["reason"] = cur_delay.find("reason").text.strip()

        # If they exist, will be one structure for arrival delays and one for departure. Type attribute holds either "Arrival" or "Departure"
        arrivals_and_departs = cur_delay.find_all("arrival_departure")
        for arrive_or_depart in arrivals_and_departs:

            if (arrive_or_depart.get("type").strip().lower() == "arrival" and is_departing == False):
                cur_ad_dict["arrival_delay"]["min"] = arrive_or_depart.find("min").text.strip()
                cur_ad_dict["arrival_delay"]["max"] = arrive_or_depart.find("max").text.strip()
                cur_ad_dict["arrival_delay"]["trend"] = arrive_or_depart.find("trend").text.strip()

            else:
                cur_ad_dict["departure_delay"]["min"] = arrive_or_depart.find("min").text.strip()
                cur_ad_dict["departure_delay"]["max"] = arrive_or_depart.find("max").text.strip()
                cur_ad_dict["departure_delay"]["trend"] = arrive_or_depart.find("trend").text.strip()

        # Append current delay to master list
        master_list.append(cur_ad_dict)

  return master_list

# Master query function
def query_airport(airport_name, is_departing=True):
    # To be returned
    delays_returned = []

    # Perform request + parse XML content
    req_headers = { "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36" }
    response = requests.get(url = "https://nasstatus.faa.gov/api/airport-status-information", headers = req_headers)
    response.raise_for_status()

    xml_content = response.content
    soup = BeautifulSoup(xml_content, "lxml")

    # Loop through Delay_type elements. We will handle airport closures, ground stops, ground delays, and arrival/departure delays
    delay_types = soup.find_all("delay_type")
    for cur_delay_type in delay_types:

        cur_delay_type_results = []
        list_type = cur_delay_type.find("name").next_sibling.name.strip().lower()

        # Handle delay type accordingly
        match list_type:
            case 'airport_closure_list':
                cur_delay_type_results = parse_airport_closures(airport_name, cur_delay_type)

            case 'ground_stop_list':
                cur_delay_type_results = parse_ground_stops(airport_name, cur_delay_type)

            case 'ground_delay_list':
                cur_delay_type_results = parse_ground_delays(airport_name, cur_delay_type)

            case 'arrival_departure_delay_list':
                cur_delay_type_results = parse_ad_delays(airport_name, is_departing, cur_delay_type)

        # Append the result to our master list
        if cur_delay_type_results != []:
            delays_returned.append(cur_delay_type_results)

    return delays_returned

# Update the output label when called to
def update_output(delay_list):
    list_text = ", ".join([str(obj) for obj in delay_list]) # COMPARE WITH OVERRIDDEN __STR__ PERFORMANCE...
    output_label.config(text=list_text)

# Saves the given AirportQuery instance to JSON log file defined above
def save_airport_query_to_disk(query_instance):
    with open(log_file_name, 'a') as log_handle:
        query_dict = {
            'query_time' : query_instance.query_time,
            'airport' : query_instance.airport_name,
            'is_departing' : query_instance.departing,
            'events_list' : query_instance.delay_list
        }
        json.dump(query_dict, log_handle)

# Exit button
def close():
    win.destroy()

# Search button
def search_click():
    
    is_departing = True
    if radio_selected.get() == "Arriving":
        is_departing = False

    # Perform query, create class instance
    delay_list = query_airport(airport_name.get(), is_departing)
    query_result = AirportQuery(airport_name.get(), is_departing, delay_list)

    # Update output label
    update_output(delay_list)

    # Save results to JSON file
    save_airport_query_to_disk(query_result)

# App entrypoint
win = Tk()

# Tkinter vars
airport_name = StringVar()
radio_selected = StringVar()

win.title('Delay Status App')
win.geometry('610x500')
win.columnconfigure(0, weight=1) # content displayed in the center
win.config(bg='black')

canvas = Canvas(win, width=300, height=180, bg='black')
canvas.grid(columnspan=3, pady=10)

logo = Image.open('airport.jpg')
new_width = 300
new_height = 150
img = logo.resize((new_width, new_height), Image.LANCZOS)
img.save('airport.png')
logo = ImageTk.PhotoImage(img)
logo_label = Label(image=logo)
logo_label.image = logo
logo_label.grid(columnspan=3, column=0, row=0, pady=10)

# Airport name entry
airport_label = Label(win, text="Please enter your airport via abbreviated code: ", fg='white', bg='black')
airport_label.grid(columnspan=2, column=0, row=1, pady=10, sticky='w')

airport_entry = Entry(win, textvariable=airport_name, width=30)
airport_entry.grid(row=1, column=2, columnspan=1)

# Select departing or arriving
trip_type_label = Label(win, text="Please choose whether you are departing or arriving: ", fg='white', bg='black')
trip_type_label.grid(columnspan=2, column=0, row=3, pady=10, rowspan=2, sticky='w')

option1 = Radiobutton(win, text="Departing", variable=radio_selected, value="Departing", bg='black')
option1.grid(row=3, column=2, columnspan=1, rowspan=1) 

option2 = Radiobutton(win, text="Arriving", variable=radio_selected, value="Arriving", bg='black')
option2.grid(row=4, column=2, columnspan=1, rowspan=1) 

# Output label
output_label = Label(win, text="(Relevant delays and closures will be returned here)", fg='white', bg='black', wraplength=400, anchor='n')
output_label.grid(columnspan=3, rowspan=4, column=0, row=5, pady=10, sticky='nsew')

# Search + Exit buttons
search_button = Button(win, command=search_click, font=("Arial", 16), text='Search', width=15)
search_button.grid(column=0, row=12, pady=20, padx=(35, 0), sticky=W)


exit_button = Button(win, command=close, font=("Arial", 16), text='Exit', width=15)
exit_button.grid(column=2, row=12, pady=20, padx=(0, 35), sticky=E)

# Listen...
win.mainloop()