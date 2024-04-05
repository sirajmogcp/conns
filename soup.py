from bs4 import BeautifulSoup
import requests
import http.client
import shutil
import os
from google.cloud import storage
def get_product(product_url):
    image=""
    descrption=""
    feature=""
    response = requests.get(product_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Make request to the product page
    response = requests.get(product_url)

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract product image
    image_element = soup.find("img", class_="more-img")  # This may vary depending on your theme
    
    if image_element:
        product_image_url = image_element["src"]
        
        image= download_image(product_image_url, "conn-sb")
        
    description_element = soup.find("div", class_="marketing_information")  # Replace class with the correct one on your website
    if description_element:
        product_description = description_element.text.strip()
        descrption= product_description
    
    description_bullets = soup.find("div", class_="bullet_section")  # Replace class with the correct one on your website
    if description_bullets:
        
        list_items = description_bullets.find_all('li')

        # Extract text, strip it, and separate
        text_list = [item.text.strip() for item in list_items]

        # Join the text pieces with commas
        result = ', '.join(text_list)


        descrption= product_description + " " + result
        
    features_div = soup.find("div", class_="features")  # Replace class with the correct one on your website
    # If the div exists, proceed
    
    if features_div:
        text = ''
        # Loop through all child elements
        for element in features_div.children:
            # Extract text from <strong> and <br> tags and add with a space
            if element.name in ['strong', 'br']:
               text += element.text.strip() + ' '
        # Remove the trailing space
        result = text.rstrip()
        print(result)
        feature= result
    else:
        print("Div with id 'features' not found.")
            

    specifications = []        
    table = soup.find("table", class_="table")
    table_data = []
    for row in table.find_all("tr"):
        cells = row.find_all("td")
        if cells:
          table_data.append([cell.text.strip() for cell in cells])

    # Extract data from hidden inputs:
    hidden_inputs = soup.find_all("input", class_="specs_technical_details")
    hidden_data = {
        input["data-name"]: input.get("data-weight").strip() for input in hidden_inputs
    }

    # Combine both data sets:
    specifications = table_data + list(hidden_data.items())

    
    return image,descrption,feature,specifications
        


def download_image(url, bucket_name):
    """Downloads an image from a URL and saves it to a Google Cloud Storage bucket.

    Args:
        url: The URL of the image to download.
        bucket_name: The name of the Google Cloud Storage bucket to save the image to.
    """

    # Get image filename from URL
    filename = url.split("/")[-1]

    # Download image content
    response = requests.get(url)

    # Create GCS client 
    storage_client = storage.Client()

    # Get bucket object
    bucket = storage_client.bucket(bucket_name)

    # Create blob object with the filename
    blob = bucket.blob(filename)

    # Upload image content to the blob
    blob.upload_from_string(response.content)
    imagepath = f"gs://{bucket_name}/{filename}"
    return imagepath
    
