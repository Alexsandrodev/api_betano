from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime
import re
from app.utils import jsonData
import logging


def dataAtualizacao():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

import re

def Format_name(text):
    match text:
        case  "copaAmerica":
            return "Copa America"
        
        case "tacaGloriaEterna":
            return "Taça Glória eterna"
        
        case "euro":
            return "Euro"
        
        case "britishDerbies":
            return "British Derbies"

        case "ligaEspanhola":
            return "Liga Espanhola"
        
        case "scudettoItaliano":
            return "Scudetto Italiano"
        
        case "campeonatoItaliano":
            return "Campeonato Italiano"
        
        case "copaDasEstrelas":
            return "Copa das estrelas"



def gethtml(campeonato):
    url = "https://www.betano.bet.br/virtuals/futebol/"
    liga = Format_name(campeonato)
    
    options = Options()
    options.add_argument("--headless")  # Sem interface gráfica
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    
    
    button_sim = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-qa="age-verification-modal-ok-button"]'))
    )


    
    button_sim.click()
        
    button_x = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="button"]'))
    )
        
    button_x.click()
        
    camp = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, f"{liga}"))
    )
    camp.click()
    camp.click()
    
    
    button_results = WebDriverWait (driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-qa='virtuals-results-toggle-button']"))
        
        )
    button_results.click()
    
    sleep(1)

    page_source = driver.page_source
        
    driver.quit()
    
    return page_source
