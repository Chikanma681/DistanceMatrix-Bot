from typing import Any, Text, Dict, List
import requests,json
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import os

api_key = os.environ.get('api')
class ActionDistanceMatrix(Action):

    def name(self) -> Text:
        return "action_find_distance"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        start_location = tracker.get_slot("start_city")
        end_location = tracker.get_slot("end_city")
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&"
        request_value =  requests.get(url+"origins="+start_location+"&destinations="+end_location+"&key="+api_key)
        access = request_value.json()

        time_text = access['rows'][0]['elements'][0]['duration']['text']
        distance_text = access['rows'][0]['elements'][0]['distance']['text']
        
        if (start_location or end_location) is None:
            rv = "Sorry we couldn't we find the distance matrix.\nWe couldn't identify either your current location or destination"
        else:
            try:
                rv = f"The distance between {start_location} and {end_location} is {time_text}"
            except:
                rv = "Sorry we couldn't we find the distance matrix.\nPlease try rephrasing"

        dispatcher.utter_message(text=rv)

        return []
