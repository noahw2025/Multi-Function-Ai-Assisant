import openai
import subprocess
import re
import webbrowser
import spotipy
import json
import os
from spotipy.oauth2 import SpotifyOAuth
import requests
from bs4 import BeautifulSoup



OPENAI_API_KEY = "KEY"
SPOTIPY_CLIENT_ID = "KEY"
SPOTIPY_CLIENT_SECRET = "KEY"
SPOTIPY_REDIRECT_URI = "KEY"
API_KEY = "KEY"
SEARCH_ENGINE_ID = "KEY"
huggingface_api_url = "KEY"
HUGGINGFACE_API_KEY = "KEY"

# Set your OpenAI API key
openai.api_key = OPENAI_API_KEY


def generate_image_with_huggingface(prompt):
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
    }
    data = {
        "inputs": prompt
    }

    response = requests.post(huggingface_api_url, headers=headers, json=data)

    if response.status_code == 200:
        # Save the generated image
        with open("generated_image.png", "wb") as f:
            f.write(response.content)
        print("Image successfully generated and saved as 'generated_image.png'.")
        return "generated_image.png"
    else:
        print(f"Failed to generate image. Status code: {response.status_code}, Response: {response.text}")
        return None

def create_spotify_client():
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=SPOTIPY_CLIENT_ID,
            client_secret=SPOTIPY_CLIENT_SECRET,
            redirect_uri=SPOTIPY_REDIRECT_URI,
            scope='playlist-modify-public user-read-recently-played '
                  'user-top-read user-library-read',
            cache_path='.cache'
        ))
        return sp
    except spotipy.exceptions.SpotifyException as e:
        # Clear cache and retry
        if os.path.exists('.cache'):
            os.remove('.cache')
        raise Exception(f"Spotify Auth Error: {str(e)}")
# Temporary variables to store the last GPT-4 response and code
last_output = ""
last_code = ""
message_history = []


# Function to extract code between ### markers
def extract_code(text):
    pattern = r"###(.*?)###"
    matches = re.findall(pattern, text, re.DOTALL)
    if matches:
        return matches[0].strip()
    else:
        return None


# Function to save the last generated code to a file
def save_code_to_file(filename="output.py"):
    global last_code
    if last_code:
        try:
            with open(filename, 'w') as file:
                file.write(last_code)
            print(f"Code successfully saved to {filename}")
        except Exception as e:
            print(f"Error saving code: {e}")
    else:
        print("No code to save.")


# Function to open the file in PyCharm
def open_code_in_pycharm(file_name="output.py"):
    try:
        subprocess.run(["pycharm.bat", file_name], check=True)
        print(f"Opened {file_name} in PyCharm successfully.")
    except FileNotFoundError:
        try:
            subprocess.run(["pycharm64.exe", file_name], check=True)
            print(f"Opened {file_name} in PyCharm (fallback to pycharm64.exe).")
        except Exception as e:
            print(f"Failed to open {file_name} in PyCharm: {e}")


# Function to run the code in terminal and output results/errors
def run_code_in_terminal(file_name="output.py"):
    try:
        result = subprocess.run(["python", file_name], capture_output=True, text=True)
        if result.stdout:
            print(f"Output:\n{result.stdout}")
        if result.stderr:  # If errors are captured
            print(f"Errors detected:\n{result.stderr}")
    except Exception as e:
        print(f"Error running the code: {e}")


# Function to perform a Google search

def google_search(query):
    try:
        url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}"
        response = requests.get(url)
        data = response.json()

        # Check for search results
        if 'items' in data:
            search_results = []
            for item in data['items'][:5]:  # Get top 5 results
                search_results.append(item['link'])
            return search_results
        else:
            return "No search results found."
    except Exception as e:
        return f"Error during Google search: {e}"

# Scrape content from the web page
def scrape_web_content(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Remove unnecessary scripts and styles
            for script in soup(["script", "style"]):
                script.decompose()

            # Get text content
            text = soup.get_text(separator=' ')
            # Clean up the text
            text = ' '.join(text.split())  # Removes excessive whitespace
            return text[:2000]  # Return the first 2000 characters for summarization
        else:
            return f"Error fetching the web page: {response.status_code}"
    except Exception as e:
        return f"Error during web scraping: {e}"


# Spotify Functions

# Function to create a Spotify playlist based on intent and reference song
def create_playlist_from_reference(sp, playlist_name, reference_song, num_songs):
    try:
        results = sp.search(q=reference_song, type='track', limit=1)
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            print(f"Found reference song: {track['name']} by {track['artists'][0]['name']}")

            # Get recommended tracks based on reference song
            recommendations = sp.recommendations(seed_tracks=[track['id']], limit=num_songs)
            track_ids = [track['id']] + [rec['id'] for rec in recommendations['tracks']]

            # Create playlist
            user_id = sp.me()['id']
            playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
            sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist['id'], tracks=track_ids)
            print(f"Playlist '{playlist_name}' created successfully with {len(track_ids)} tracks.")
        else:
            print(f"No results found for the reference song '{reference_song}'")
    except Exception as e:
        print(f"Error creating playlist: {e}")


# Function to get user's top artists
def get_top_artists(sp, limit=20, time_range='medium_term'):
    try:
        artists = sp.current_user_top_artists(limit=limit, time_range=time_range)['items']
        artist_list = [artist['name'] for artist in artists]
        print("Top Artists:", ", ".join(artist_list))
        return artist_list
    except Exception as e:
        print(f"Spotify API Error: {e}")
        return []


# Function to get user's top tracks
def get_top_tracks(sp, limit=20, time_range='medium_term'):
    try:
        tracks = sp.current_user_top_tracks(limit=limit, time_range=time_range)['items']
        track_list = [f"{track['name']} by {', '.join([artist['name'] for artist in track['artists']])}" for track in
                      tracks]
        print("Top Tracks:", "\n".join(track_list))
        return track_list
    except Exception as e:
        print(f"Spotify API Error: {e}")
        return []


# Function to handle Spotify intents
# Create the Spotify client globally
sp = create_spotify_client()

# Function to handle Spotify intents
def handle_spotify_intent(intent, param, num_songs=None):
    if intent == "#createspotifyplaylist":
        create_playlist_from_reference(sp, param['playlist_name'], param['reference_song'], num_songs)
    elif intent == "#gettopartists":
        get_top_artists(sp)  # Now 'sp' is defined
    elif intent == "#gettoptracks":
        get_top_tracks(sp)

# Function to interact with GPT-4 and get the response
def gpt4_interaction(prompt):
    try:
        # Add the user's message to the message history
        message_history.append({"role": "user", "content": prompt})

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=message_history,
            max_tokens=500,
            temperature=0.7
        )
        assistant_message = response['choices'][0]['message']['content'].strip()

        # Add the assistant's response to the message history
        message_history.append({"role": "assistant", "content": assistant_message})

        return assistant_message
    except Exception as e:
        print(f"Error during GPT-4 interaction: {e}")
        return ""


# Function to handle the response, save the last response in memory, and check for intent
def handle_response(response):
    global last_output, last_code
    print("GPT-4 Response:")
    print(response)
    last_output = response  # Store the response in the temporary variable

    # Extract code from response if present
    code = extract_code(response)
    if code:
        last_code = code  # Store the extracted code

    # Check for intent markers in the response
    if "#savefilenow" in response:
        print("Saving the code as requested...")
        save_code_to_file()
    if "#openpycharmnow" in response:
        open_code_in_pycharm()
    if "#runcodenow" in response:
        print("Running the code in terminal...")
        run_code_in_terminal()
    if "#searchgooglenow" in response:
        search_query = extract_search_query(response).strip('[]')  # Clean up the query
        if search_query:
            print(f"Recognized intent to search for: {search_query}")
            search_results = google_search(search_query)

            if isinstance(search_results, list):
                print("Top search results:")
                web_content = ""

                for result in search_results:
                    print(result)
                    # Scrape each website's content
                    page_content = scrape_web_content(result)
                    web_content += page_content + "\n"

                # Summarize the scraped content with GPT-4
                gpt4_summary = gpt4_interaction(f"Summarize the following content:\n{web_content}")
                print("GPT-4 Summary:")
                print(gpt4_summary)
            else:
                print(search_results)
    # Handle Spotify intents
    if "#createspotifyplaylist" in response:
        playlist_name = extract_spotify_param(response, "#createspotifyplaylist")
        reference_song = extract_spotify_param(response, "#referencetrack")
        num_songs = extract_spotify_param(response, "#numtracks")

        # Clean up and convert num_songs to an integer
        if num_songs:
            num_songs = int(re.sub(r'\D', '', num_songs))  # Remove non-numeric characters and convert to int
        else:
            num_songs = 10  # Default to 10 if not provided or extracted incorrectly

        handle_spotify_intent("#createspotifyplaylist", {"playlist_name": playlist_name, "reference_song": reference_song}, num_songs)
    if "#gettopartists" in response:
        handle_spotify_intent("#gettopartists", None)
    if "#gettoptracks" in response:
        handle_spotify_intent("#gettoptracks", None)
    if "#createimage" in response:
        image_prompt = extract_image_prompt(response)
        if image_prompt:
            print(f"Recognized intent to create an image for: {image_prompt}")
            image_path = generate_image_with_huggingface(image_prompt)
            if image_path:
                print(f"Image successfully generated at {image_path}")
            else:
                print("Failed to generate image.")


def extract_image_prompt(response):
    pattern = r"#createimage (.+)$"
    match = re.search(pattern, response)
    if match:
        return match.group(1).strip()
    else:
        return None

# Function to extract the search query from GPT-4 response
def extract_search_query(response):
    pattern = r"#searchgooglenow (.+)$"
    match = re.search(pattern, response)
    if match:
        return match.group(1).strip()
    else:
        return None

# Function to extract Spotify parameters from GPT-4 response
def extract_spotify_param(response, intent):
    pattern = fr"{intent} (.+)$"
    match = re.search(pattern, response)
    if match:
        return match.group(1).strip()
    else:
        return None


# Initialize the message history with the system prompt
message_history = [
    {"role": "system", "content": "You are an advanced AI assistant. Recognize intent based on inputs. "
                                  "For code outputs, always wrap the code with ### at the beginning and end. "
                                  "If you recognize an intent to save a file, print #savefilenow. If you recognize "
                                  "If you recognize an intent to create an image, print #createimage [image_prompt]."
                                  "an intent to open the code in PyCharm, print #openpycharmnow. "
                                  "If you recognize an intent to run the code in terminal, print #runcodenow. "
                                  "If you recognize an intent to perform a Google search, print #searchgooglenow [query]. "
                                  "For Spotify, if you recognize an intent to create a playlist, print #createspotifyplaylist [playlist_name] "
                                  "#referencetrack [track_name] #numtracks [num_songs]. "
                                  "If you recognize an intent to get top artists, print #gettopartists. "
                                  "If you recognize an intent to get top tracks, print #gettoptracks."}
]

# Main loop for interaction
# Spotify Client Initialization
sp = create_spotify_client()

# Main loop for interaction
if __name__ == "__main__":
    while True:
        try:
            user_input = input("You: ")

            if user_input.lower() in ["exit", "quit"]:
                print("Exiting...")
                break

            elif user_input.lower() == "save to file":
                # Trigger the save action for the last code
                save_code_to_file()

            else:
                # Interact with GPT-4
                response = gpt4_interaction(user_input)
                handle_response(response)  # 'sp' is globally available now
        except KeyboardInterrupt:
            print("\nExiting...")
            break
