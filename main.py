import time
import random
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('capsule_farmer.log'),
        logging.StreamHandler()
    ]
)

def setup_driver():
    """Setup headless Firefox driver"""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    service = Service('geckodriver.exe')  # Path to your geckodriver
    driver = webdriver.Firefox(service=service, options=options)
    return driver

def harvest_capsules():
    """Main function to harvest capsules"""
    logging.info("Starting capsule harvesting...")
    driver = setup_driver()
    
    try:
        # Navigate to lolesports.com
        driver.get("https://lolesports.com")
        logging.info("Navigated to lolesports.com")
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        capsules = []
        for i in range(5):
            time.sleep(1)
            # Simulate watching a match
            logging.info(f"Watching match {i+1}/5")
            # Add your actual capsule harvesting logic here
            capsule = random.randint(1, 100)
            logging.info(f"Harvested capsule with value: {capsule}")
            capsules.append(capsule)
            
        logging.info(f"Harvesting complete. Total capsules: {len(capsules)}")
        return capsules
        
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise
    finally:
        driver.quit()

if __name__ == "__main__":
    try:
        Path("./logs/").mkdir(parents=True, exist_ok=True)
        harvest_capsules()
    except KeyboardInterrupt:
        logging.info("Program terminated by user")
    except Exception as e:
        logging.error(f"Program terminated due to error: {str(e)}")
