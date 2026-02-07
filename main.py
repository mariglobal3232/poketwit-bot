import tweepy
import requests
import random
import os
import time

# --- SETUP: SECRETS ---
# Make sure to add these in the "Secrets" (padlock icon) menu in Replit!
api_key = os.environ['API_KEY']
api_secret = os.environ['API_SECRET']
access_token = os.environ['ACCESS_TOKEN']
access_secret = os.environ['ACCESS_SECRET']

# --- AUTHENTICATE ---
# V1.1 is needed for media upload (images)
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_secret)
api = tweepy.API(auth)
# V2 is needed for posting the text
client = tweepy.Client(
    consumer_key=api_key,
    consumer_secret=api_secret,
    access_token=access_token,
    access_token_secret=access_secret
)

def get_retro_mon():
    # Only Gen 1 (1-151) because that's where the "Retro" art exists
    poke_id = random.randint(1, 151)
    
    # 1. Get the Sprite (Visuals)
    # We specifically want the "Red/Blue" generation sprite
    url_pokemon = f"https://pokeapi.co/api/v2/pokemon/{poke_id}"
    data_pokemon = requests.get(url_pokemon).json()
    name = data_pokemon['name'].capitalize()
    
    # This path is specific to the old Gameboy visuals
    sprite_url = data_pokemon['sprites']['versions']['generation-i']['red-blue']['front_transparent']
    
    # 2. Get the Flavor Text (Lore)
    url_species = f"https://pokeapi.co/api/v2/pokemon-species/{poke_id}"
    data_species = requests.get(url_species).json()
    
    # Find the entry specifically from "Red" version
    flavor_text = "No entry found."
    for entry in data_species['flavor_text_entries']:
        if entry['version']['name'] == 'red':
            # Clean up the text (remove weird newlines from the old data)
            flavor_text = entry['flavor_text'].replace('\n', ' ').replace('\f', ' ')
            break
            
    return name, sprite_url, flavor_text

def job():
    print("Traveling back to 1996...")
    try:
        name, image_url, text = get_retro_mon()
        
        print(f"Found: {name}")
        
        # Download the image
        filename = "retro.png"
        request = requests.get(image_url, stream=True)
        if request.status_code == 200:
            with open(filename, 'wb') as image:
                for chunk in request:
                    image.write(chunk)
            
            # Upload Image (V1.1 API)
            media = api.media_upload(filename)
            
            # Create Tweet (V2 API)
            tweet_text = f"#{name} (1996)\n\nPokedex Entry:\n{text}\n\n#Pokemon #RetroGaming"
            client.create_tweet(text=tweet_text, media_ids=[media.media_id])
            
            print("Tweet sent!")
        else:
            print("Could not download image.")
            
    except Exception as e:
        print(f"Error: {e}")

# Run it once
job()
