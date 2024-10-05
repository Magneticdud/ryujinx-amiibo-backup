import requests
import json

def download_and_save_json(url, filename):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Parse the JSON content
        data = response.json()
        
        # Save the JSON data to a file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"Successfully downloaded and saved the JSON data to {filename}")
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while downloading the data: {e}")
    except json.JSONDecodeError:
        print("The content at the URL is not valid JSON")
    except IOError as e:
        print(f"An error occurred while saving the file: {e}")

# URL to download from
url = "https://amiibo.ryujinx.org/"

# Filename to save the JSON data
filename = "amiibo.json"

# Call the function to download and save the JSON
download_and_save_json(url, filename)
#manually place it in ryujinx\portable\system\amiibo