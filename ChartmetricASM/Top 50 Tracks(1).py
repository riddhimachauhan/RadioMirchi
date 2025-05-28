#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from datetime import datetime, timedelta
import json

import requests

REFRESH_TOKEN = "Write_token_here"

def refresh_access_token(refresh_token=REFRESH_TOKEN):
    url = "https://api.chartmetric.com/api/token"
    headers = {"Content-Type": "application/json"}
    data = {"refreshtoken": refresh_token}  
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        token = response.json().get('token')
        print("Access token:", token)
        return token
    else:
        print("Error:", response.status_code)
        print(response.text)
        return None

access_token = refresh_access_token()


# In[3]:


#TOP 50 SONG DETAILS ONLY
def fetch_top_tracks(api_token, params):
    url = "https://api.chartmetric.com/api/charts/spotify"
    headers = {"Authorization": f"Bearer {api_token}"}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get('obj', {}).get('data', [])
    else:
        print("Fetch error:", response.status_code)
        return []

api_token = refresh_access_token()
if api_token:
    today = datetime.today().strftime('%Y-%m-%d')
    yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    params = {
        "date":yesterday,
        "country_code": "US",
        "interval": "daily",
        "type": "plays"
    }
    tracks = fetch_top_tracks(api_token, params)
    if tracks:
        for i, track in enumerate(tracks[:50], 1):
            print(f"{i}. {track.get('name', 'Unknown')}")
    else:
        print("No tracks found.")


# 

# In[ ]:


#TOP 50 SONGS BY GENRE
import requests

def get_genres(api_token):
    url = "https://api.chartmetric.com/api/genre"
    headers = {"Authorization": f"Bearer {api_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        genres = response.json().get('obj', [])
        return genres
    else:
        print("Error fetching genres:", response.status_code, response.text)
        return []

def fetch_tracks_by_genre(api_token, genre_id, limit=50):
    url = "https://api.chartmetric.com/api/track/list/filter"
    headers = {"Authorization": f"Bearer {api_token}"}
    params = [
        ("genres[]", genre_id),
        ("sortColumn", "score"),
        ("limit", str(limit))
    ]
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        #print(data) 
        return data
    else:
        print("Error fetching tracks:", response.status_code, response.text)
        return []
def main():
    api_token = refresh_access_token()
    if not api_token:
        print("Failed to get API token")
        return

    genres = get_genres(api_token)
    if not genres:
        print("No genres found")
        return

    print("Available Genres and IDs:")
    for genre in genres:
        print(f"{genre['name']} (ID: {genre['id']})")

    try:
        chosen_genre_id = int(input("\nEnter the genre ID to fetch top 50 songs: "))
    except ValueError:
        print("Invalid input. Please enter a valid genre ID number.")
        return

    track_data = fetch_tracks_by_genre(api_token, chosen_genre_id)
    if not track_data:
        print("No tracks found for this genre.")
        return

    for idx, track in enumerate(track_data.get("obj", []), 1):
        print(f"{idx}. {track.get('name', 'Unknown')}")

if __name__ == "__main__":
    main()


# In[ ]:


import requests
from datetime import datetime, timedelta
import json

REFRESH_TOKEN = "xWfzKOpi3LwWdt8uirHzlJ38t8i6GaGI0GEN6JDKnYVmYiE84h1p3FedCuDmj2Mw"

def refresh_access_token(refresh_token=REFRESH_TOKEN):
    url = "https://api.chartmetric.com/api/token"
    headers = {"Content-Type": "application/json"}
    data = {"refreshtoken": refresh_token}  
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        token = response.json().get('token')
        #print("Access token:", token)
        return token
    else:
        print("Error:", response.status_code)
        print(response.text)
        return None

access_token = refresh_access_token()

def get_min_release_date(option):
    today = datetime.today()
    if option == "Last 1 Week":
        return (today - timedelta(days=7)).strftime('%Y-%m-%d')
    elif option == "Last 1 Month":
        return (today - timedelta(days=30)).strftime('%Y-%m-%d')
    elif option == "Last 1 Year":
        return (today - timedelta(days=365)).strftime('%Y-%m-%d')
    elif option == "All Time":
        return None
    else:
        raise ValueError("Invalid option for release date filter.")

def top_tracks(api_token, params):
    url = "https://api.chartmetric.com/api/track/list/filter"
    headers = {"Authorization": f"Bearer {api_token}"}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Fetch error:", response.status_code, response.text)
        return None

def is_valid_release_date(date_str):
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        return date <= datetime.today()
    except Exception:
        return False

def filter_tracks_by_release_date(tracks_json):
    filtered = []
    for track in tracks_json.get("obj", []):
        albums = track.get("album", [])
        if any(is_valid_release_date(album.get("release_date", "")) for album in albums):
            filtered.append(track)
    return filtered

def main():
    print("Choose Release Date Filter:")
    print("1. Last 1 Week")
    print("2. Last 1 Month")
    print("3. Last 1 Year")
    print("4. All Time")
    option_map = {
        "1": "Last 1 Week",
        "2": "Last 1 Month",
        "3": "Last 1 Year",
        "4": "All Time"
    }
    choice = input("Enter choice (1-4): ").strip()
    filter_option = option_map.get(choice, "All Time")

    min_release_date = get_min_release_date(filter_option)

    api_token = refresh_access_token()
    if api_token:
        params = {
            "limit": 75,
            "sortColumn": "latest.spotify_plays",
            "sortOrderDesc": True,
        }
        if min_release_date:
            params["min_release_date"] = min_release_date

        tracks_json = top_tracks(api_token, params)
        if tracks_json:
            filtered_tracks = filter_tracks_by_release_date(tracks_json)[:50]

            print(f"\nTop {len(filtered_tracks)} Songs ({filter_option}):")
            for i, track in enumerate(filtered_tracks, 1):
                print(f"{i}. {track.get('name', 'Unknown Title')}")
        else:
            print("No tracks found.")
    else:
        print("Could not get API token.")

if __name__ == "__main__":
    main()



# In[ ]:


# TOP 50 SONGS BY GENRE
import requests

REFRESH_TOKEN = "xWfzKOpi3LwWdt8uirHzlJ38t8i6GaGI0GEN6JDKnYVmYiE84h1p3FedCuDmj2Mw"

def refresh_access_token(refresh_token=REFRESH_TOKEN):
    url = "https://api.chartmetric.com/api/token"
    headers = {"Content-Type": "application/json"}
    data = {"refreshtoken": refresh_token}
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.json().get('token')
    else:
        print("Error:", response.status_code)
        print(response.text)
        return None

def get_genres(api_token):
    url = "https://api.chartmetric.com/api/genre"
    headers = {"Authorization": f"Bearer {api_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('obj', [])
    else:
        print("Error fetching genres:", response.status_code, response.text)
        return []

def fetch_tracks_by_genre(api_token, genre_id, limit=50):
    url = "https://api.chartmetric.com/api/track/list/filter"
    headers = {"Authorization": f"Bearer {api_token}"}
    params = [
        ("genres[]", genre_id),
        ("sortColumn", "score"),
        ("limit", str(limit))
    ]
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching tracks:", response.status_code, response.text)
        return []

def main():
    api_token = refresh_access_token()
    if not api_token:
        print("Failed to get API token")
        return

    genres = get_genres(api_token)
    if not genres:
        print("No genres found")
        return

    keyword = input("Enter a genre name (or part of it): ").strip().lower()
    matching_genres = [g for g in genres if keyword in g['name'].lower()]

    if not matching_genres:
        print("No matching genres found.")
        return

    if len(matching_genres) == 1:
        selected_genre = matching_genres[0]
        print(f"\nFound 1 genre: {selected_genre['name']} (ID: {selected_genre['id']})")
    else:
        print("\nMultiple matching genres found:")
        for idx, genre in enumerate(matching_genres, 1):
            print(f"{idx}. {genre['name']} (ID: {genre['id']})")
        try:
            choice = int(input("Select the genre number from the list above: "))
            selected_genre = matching_genres[choice - 1]
        except (ValueError, IndexError):
            print("Invalid choice.")
            return

    print(f"\nFetching top 50 songs for: {selected_genre['name']}...\n")
    track_data = fetch_tracks_by_genre(api_token, selected_genre['id'])

    if not track_data or not track_data.get("obj"):
        print("No tracks found for this genre.")
        return

    for idx, track in enumerate(track_data["obj"], 1):
        print(f"{idx}. {track.get('name', 'Unknown')}")

if __name__ == "__main__":
    main()


# In[ ]:





# In[ ]:




