import requests
import json
import os

def download_and_save_json(url, filename):
    try:
        # Check if the file already exists
        if os.path.exists(filename):
            overwrite = input(f"The file '{filename}' already exists. Do you want to overwrite it? (y/n): ").lower()
            if overwrite != 'y':
                print("Download cancelled. Existing file was not overwritten.")
                return True

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
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while downloading the data: {e}")
    except json.JSONDecodeError:
        print("The content at the URL is not valid JSON")
    except IOError as e:
        print(f"An error occurred while saving the file: {e}")
    
    return False

def download_image(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Successfully downloaded: {filename}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")

def process_json_and_download_images(json_filename):
    # Create images directory if it doesn't exist
    os.makedirs('images', exist_ok=True)

    try:
        with open(json_filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'amiibo' in data and isinstance(data['amiibo'], list):
            for amiibo in data['amiibo']:
                if 'image' in amiibo and amiibo['image']:
                    image_url = amiibo['image']
                    image_filename = os.path.join('images', os.path.basename(image_url))
                    download_image(image_url, image_filename)
        else:
            print("The JSON structure is not as expected. Couldn't find 'amiibo' array.")
    except UnicodeDecodeError:
        print(f"Error reading the file {json_filename}. Trying with different encoding...")
        try:
            with open(json_filename, 'r', encoding='latin-1') as f:
                data = json.load(f)
            
            if 'amiibo' in data and isinstance(data['amiibo'], list):
                for amiibo in data['amiibo']:
                    if 'image' in amiibo and amiibo['image']:
                        image_url = amiibo['image']
                        image_filename = os.path.join('images', os.path.basename(image_url))
                        download_image(image_url, image_filename)
            else:
                print("The JSON structure is not as expected. Couldn't find 'amiibo' array.")
        except Exception as e:
            print(f"Failed to read the JSON file: {e}")


# URL to download from
url = "https://amiibo.ryujinx.org/"

# Filename to save the JSON data
filename = "amiibo.json"

# Call the function to download and save the JSON
# Download and save the JSON
if download_and_save_json(url, filename):
    # If JSON was successfully downloaded and saved, process it and download images
    getimages = input(f"Do you want to download all the images? (y/n): ").lower()
    if getimages == 'y':
        process_json_and_download_images(filename)
print("Ok, done. Now manually place the json in ryujinx\portable\system\\amiibo")

#TODO: change the urls in the json to some local path, but that would change according to who's running this program. It's just faster to do it with search&replace in notepad