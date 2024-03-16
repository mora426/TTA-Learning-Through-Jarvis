# This Python code provides functionality to retrieve song lyrics using the Musixmatch API.
# It sends a request to the Musixmatch API to search for a track based on the provided query 
# and it also sends another request to get the lyrics of the track using the track ID obtained earlier.
# It effectively integrates with the Musixmatch API to fetch track information and lyrics. However, 
# it grabs only the first track returned by API search and relies on Musixmatch API for
# data retrieval, which can be affected if the API changes or becomes unavailable.

# The objective: Improve user engagement with a service that gives lyrics from songs
# Increase User Interaction:
#  -  Key Result 1- Increase the number of user queries for song lyrics
#  -  Key Result 2- Increase the number of shares of song lyrics on social media platforms
# Enhance User Satisfaction: 
#  -  Key Result 3- Decrease the average response time to user queries for lyrics
#  -  Key Result 4- Increase the accuracy of lyrics

# Key performance indicators:
#  -  Number of User Queries for Song Lyrics -> This KPI tracks the total number of 
#     requests made to get a song's lyrics. 
#  -  Response Time to User Queries -> This KPI measures the average time taken to respond to user
#     queries for lyrics. 
#  -  Accuracy of Lyrics -> This KPI assesses the accuracy of the recieved lyrics compared
#     to the original song lyrics. 

import requests
import config
import os
from bs4 import BeautifulSoup
from templates.generic import *
from templates.text import TextTemplate

# Retrieves Musixmatch API key from environment variables or config
MUSIX_KEY = os.environ.get('MUSIX_API_KEY', config.MUSIX_API_KEY)

def process(input, entities):
    output = {}
    try:
        # Extracts the user's query for lyrics
        query = entities['lyrics'][0]['value']

        # Payload for track search API request
        payload = {
            'apikey': MUSIX_KEY,
            'q_track': query,
        }
        
        # Sends request to Musixmatch API to search for track
        r = requests.get('http://api.musixmatch.com/ws/1.1/track.search',params=payload)
        data = r.json()

        # Retrieves lyrics URL and track ID from API response
        lyrics_url = data['message']['body']['track_list'][0]['track']['track_share_url']
        track_id = data['message']['body']['track_list'][0]['track']['track_id']

        #payload for lyrics retrieval API request
        payload = {
            'apikey': MUSIX_KEY,
            'track_id': track_id,
        }

        # Sends request to Musixmatch API to get lyrics
        r = requests.get('http://api.musixmatch.com/ws/1.1/track.lyrics.get',params=payload)
        data = r.json()
        # Extracts and formats lyrics from API response
        lyrics = '\n'.join(data['message']['body']['lyrics']['lyrics_body'].split('\n')[:-1])

        # Creats elements for response template
        title = query
        item_url = lyrics_url
        subtitle = lyrics

        # Creates a generic template for the response
        template = GenericTemplate()
        template.add_element(title=title, item_url=item_url, subtitle=subtitle, buttons=[])

        #the output dictionary
        output['input'] = input
        output['output'] = template.get_message()
        output['success'] = True

    # Handles errors and returns error message
    except: 
        error_message = 'There was some error while retrieving data from genius.com'
        error_message += '\n Please ask me somrthing else, like:'
        error_message += '\n Lyrics for the song Wish you were here'
        output['error_msg'] = TextTemplate(error_message).get_message()
        output['success'] = False
    return output
