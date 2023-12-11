# ##############
# #
# #  TESSERACT OCR
# #
# #############
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import pytesseract
import imghdr
import xml.etree.ElementTree as ET
import time
from openai import OpenAI
import shlex
import re
import ast 
combined_keyword_list = []

# Function to extract text from an image using pytesseract
def extract_text_from_image(image_url, config=None):
    try:
        response = requests.get(image_url)
        img_data = BytesIO(response.content)

        image_type = imghdr.what(img_data)
        if image_type in ['jpeg', 'png']:
            img = Image.open(img_data)
        elif image_type == 'svg+xml':
            svg_tree = ET.parse(BytesIO(response.content))
            text_elements = svg_tree.findall('.//{http://www.w3.org/2000/svg}text')
            text = ' '.join(element.text.strip() for element in text_elements)
            return text
        else:
            # print(f"Unsupported image type: {image_type}")
            return ""
        
        text = pytesseract.image_to_string(img, config=config)
        return text

    except Exception as e:
        # print(f"Error extracting text from image: {e}")
        return ""

# Function to get all image URLs from HTML content
def get_all_image_urls(html_content, base_url):
    image_urls = []
    soup = BeautifulSoup(html_content, 'html.parser')
    img_tags = soup.find_all('img', src=True)

    for img_tag in img_tags:
        src = img_tag['src']
        image_url = src if src.startswith(('http://', 'https://')) else f"{base_url.rstrip('/')}/{src.lstrip('/')}"
        image_urls.append(image_url)

    return image_urls

# Function to check for text, size changes, and keyword matches
def check_for_text_size_and_keywords(url, text_config=None, size_change_threshold=30, interval_seconds=60, openai_api_key=None, hardcoded_keywords=None):
    try:
        # Make an initial GET request to the URL
        initial_response = requests.get(url)

        # Check if the request was successful (status code 200)
        if initial_response.status_code == 200:
            initial_size = len(initial_response.content)

            # Fetch keyword list from OpenAI API
            if openai_api_key:
            
                # api_keyword_list = []
                client = OpenAI(api_key = openai_api_key)
                chat_completion = client.chat.completions.create(messages = [{"role":"user","content":"imagine you are a cyber security researcher and you want to educate businesses about website defacement attacks. provide response in the following format, a single array of 15 items, only containing hacktivist groupnames, keywords and hashtags, do not provide anything else and only provide factual or historical results based on actual hacktivists attacks from 2020 to 2023:"}],model="gpt-3.5-turbo",)
                api_keyword_list = ast.literal_eval(chat_completion.choices[0].message.content)
                # print ("keyword list: " + api_keyword_list)
                # print (type(api_keyword_list))

            else:
                print("No OpenAI API key provided. Skipping API keyword matching.")
                

            # Use a combination of OpenAI API keywords and hardcoded keywords
            combined_keyword_list = api_keyword_list + (hardcoded_keywords or [])
            # print ("all keywords are: ")
        
            print("keyword list: ")
            print(combined_keyword_list)
            print("Initial check completed. Waiting for changes...")

            # Enter the loop for continuous monitoring
            while True:
                try:
                    response = requests.get(url)

                    # Check if the request was successful (status code 200)
                    if response.status_code == 200:
                        current_size = len(response.content)

                        size_change_percentage = ((current_size - initial_size) / initial_size) * 100
                    
                        print (" check #1 - check web content for keywords")
                        # print (type(response.text))
                        #check if keywords are in webpage textual content
                        if (response.text):
                            for keyword in combined_keyword_list:
                            
                                if keyword.lower() in response.text:
                                    print("**********************************************")
                                    print(f"Defacement Keyword match found in web text: {keyword}")
                                    print("**********************************************")
                        else:
                            print ("no defacement keyword found in web text")

                        print("check #2")
                        if abs(size_change_percentage) > size_change_threshold:
                            print("potential defacement detected")
                            print(f"Page size has changed by {size_change_percentage:.2f}%! (Current Size: {current_size} bytes)")
                            initial_size = current_size
                        else:
                            print(f"Page size has not changed significantly. (Current Size: {current_size} bytes)")

                        image_urls = get_all_image_urls(response.text, url)
                        print("")
                        print ("check #3)")
                        if image_urls:
                            print(f"Found {len(image_urls)} images on the page. Matching defacement keywords against OCR extracted keywords from images")

                            for image_url in image_urls:
                                image_text = extract_text_from_image(image_url, config=text_config)
                                if image_text:
                                    # print("**********************************************")
                                    # print(f"Text extracted from image ({image_url}):")
                                    # print (image_text)
                                    

                                    # Check for keyword matches
                                    for keyword in combined_keyword_list:
                                        if keyword.lower() in image_text.lower():
                                            print(f"Text extracted from image ({image_url}):")
                                            print (image_text)
                                            print("**********************************************")
                                            print(f"Defacement Keyword match found: {keyword}")
                                            print("**********************************************")
                                            print("")
                                            

                                # else:
                                #     print(f"No text extracted from the image ({image_url}).")

                        else:
                            print("No images found on the page.")
                        
                    else:
                        print(f"Failed to fetch the page. Status code: {response.status_code}")

                except Exception as e:
                    print(f"An error occurred: {e}")

                print ("---- end of this loop ----")
                time.sleep(interval_seconds)

        else:
            print(f"Failed to fetch the initial page. Status code: {initial_response.status_code}")

    except Exception as e:
        print(f"An error occurred during the initial check: {e}")

# Example usage:
# url_to_check = "https://www.helpnetsecurity.com/2013/10/08/avira-avg-whatsapp-sites-defaced-by-palestinian-hacktivists/"
url_to_check = "https://www.blackhatethicalhacking.com/articles/hacking-stories/lizard-squad-the-infamous-hacking-group-that-brought-xbox-and-playstation-networks-to-their-knees/"
#url_to_check = "https://www.reflectiz.com/blog/defacement-by-anonymous-websites-supply-chain/"
openai_api_key = ""  # Replace with your OpenAI API key

# Example configuration option for pytesseract (adjust as needed)
tesseract_config = '--psm 6'  # Page segmentation mode: Assume a uniform block of text

# Example of hardcoded keywords (replace with your own list)
# hardcoded_keywords = ["palestine","Palestinians","hackers"]
hardcoded_keywords = []
# Run the function for continuous monitoring
print("site to monitor: ")
print(url_to_check)
print(" ")
print("there will be 3 checks performed: #1) check if generated defacement keywords are found on textual content #2)check if size of webpage changed drastically since last check #3) check if OCR extracted keywords from images matches generated keywords")
check_for_text_size_and_keywords(url_to_check, text_config=tesseract_config, openai_api_key=openai_api_key, hardcoded_keywords=hardcoded_keywords)
