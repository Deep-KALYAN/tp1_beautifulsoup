from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
 
 
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get("https://www.doctolib.fr/")
wait = WebDriverWait(driver, 30)
 
try :
    reject_btn = wait.until(
        EC.element_to_be_clickable((By.ID, "didomi-notice-disagree-button"))
    )
    reject_btn.click()
    wait.until(EC.invisibility_of_element_located((By.ID, "didomi-notice-disagree-button")))
except:
    pass 

#---------------speciality----------
wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR,
        "input.searchbar-input.searchbar-query-input"))
)
place_input_specialist = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR,
        "input.searchbar-input.searchbar-query-input"))
)
place_input_specialist.clear()
place_input_specialist.send_keys("dentiste")
wait.until(
    EC.text_to_be_present_in_element_value(
        (By.CSS_SELECTOR, "input.searchbar-input.searchbar-query-input"),
        "dentiste"
    )    
)

try:
    # Wait for the dropdown container to be present
    dropdown = wait.until(
        EC.presence_of_element_located((By.ID, "search-query-input-results-container"))
    )
    
    # Find all li elements within the dropdown
    li_elements = dropdown.find_elements(By.TAG_NAME, "li")
    
    # Verify there are at least 2 li elements
    if len(li_elements) >= 1:
        # Click the second li element (index 1)
        li_elements[0].click()
        print("Successfully clicked the first li element")
    else:
        print("Not enough li elements found")
        
except Exception as e:
    print(f"Error occurred: {e}")

#------------------city-----------
wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR,
        "input.searchbar-input.searchbar-place-input"))
)
 
place_input = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR,
        "input.searchbar-input.searchbar-place-input"))
)
 
place_input.clear()
place_input.send_keys("75001")


wait.until(
    EC.text_to_be_present_in_element_value(
        (By.CSS_SELECTOR, "input.searchbar-input.searchbar-place-input"),
        "75001"
    )    
)

try:
    # Wait for the dropdown container to be present
    dropdown = wait.until(
        EC.presence_of_element_located((By.ID, "search-place-input-results-container"))
    )
    
    # Find all li elements within the dropdown
    li_elements = dropdown.find_elements(By.TAG_NAME, "li")
    
    # Verify there are at least 2 li elements
    if len(li_elements) >= 2:
        # Click the second li element (index 1)
        li_elements[1].click()
        print("Successfully clicked the second li element")
    else:
        print("Not enough li elements found")
        
except Exception as e:
    print(f"Error occurred: {e}")


#----------------------------click result button-----------------
search_button = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "span.searchbar-submit-button-label"))
)
# place_input.send_keys(Keys.ENTER)
search_button.click()
 
#----------search ------total and all the doctors------------------
time.sleep(20)
cards = driver.find_elements(By.CSS_SELECTOR, "div.dl-card")
print(f"Found results count on first page: {len(cards)}")

# Extract all the information of each doctor
results = []


for card in cards:
    try:
        print(card)
        name = card.find_element(By.CSS_SELECTOR, 'h2').text.strip()    
        specialty = card.find_element(By.CSS_SELECTOR, 'p[data-design-system-component="Paragraph"]').text.strip()
        profile_link = card.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
        img_elem = card.find_element(By.CSS_SELECTOR, 'img')
        image_url = img_elem.get_attribute('src') or img_elem.get_attribute('data-src')
        
        # Address
        address_parts = card.find_elements(By.CSS_SELECTOR, 'div.flex.flex-wrap.gap-x-4 p')
        address = ", ".join([p.text for p in address_parts])
        
        # Availability (if any)
        availability_elems = card.find_elements(By.CSS_SELECTOR, 'div[data-test-id="availabilities-container"] span.dl-pill span span')
        availability = [el.text.strip() for el in availability_elems if el.text.strip() != ""]

        results.append({
            "name": name,
            "specialty": specialty,
            "profile_link": profile_link,
            "image_url": f"https:{image_url}" if image_url.startswith("//") else image_url,
            "address": address,
            "availability": availability or None,
        })
    except Exception as e:
        print("Error parsing card:", e)

#----------div.search-results-list-view div.dl-card-content---------
time.sleep(20)
 
driver.quit()
# Show results
print(len(results))
for r in results:
    print(r)