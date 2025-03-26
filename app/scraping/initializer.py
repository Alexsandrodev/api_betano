from app.scraping import scraping
from bs4 import BeautifulSoup
from app.utils import json_data
from collections import defaultdict
from time import time

def format_data(element, soup):
    teams = element.find_all("div", class_="tw-text-xs tw-font-regular tw-leading-s tw-whitespace-nowrap tw-text-ellipsis tw-overflow-hidden")
    teamA = teams[0].get_text().strip()
    teamB = teams[1].get_text().strip()
            
    try:
        match_time = element.find("span", class_="tw-block tw-text-xs tw-font-regular tw-leading-s").get_text()
    except: 
        header = soup.find("div", class_ = "tw-text-xs tw-leading-s tw-flex tw-flex-col tw-justify-center tw-py-n tw-select-none tw-relative tw-bg-n-13-steel tw-items-center")
        match_time = header.find("span", class_ = "tw-text-n-94-dirty-snow").get_text()
            
    match_time = match_time.strip()
        
    hour, minute = match_time.split(":")
    
    match_info = {
                "TimeA": teamA,
                "TimeB": teamB,
                "Horario": match_time,
                "Hora": hour,
                "Minuto": minute
            }
    
    return match_info

def scrape_data(championship: str):
    print("Scraping data from: ", championship)
    file_name = f"{championship}.json"
    
    selenium_time = time()
    page_source = scraping.get_html(championship)
    print(f"Execution time for selenium: {time() - selenium_time:.2f}s'")
    
    soup = BeautifulSoup(page_source, "lxml")
    matches_by_hour = defaultdict(list)
    
    elements = soup.find_all("div", {"data-testid": "VirtualsUpcomingEvent"})
    
    for element in elements:
        match_info = format_data(element, soup)
        hour = match_info["Hora"]
            
        matches_by_hour[hour].append(match_info)

    data = {
            "ultimaAtualizacao": scraping.data_atualizacao(),
            "Linhas": matches_by_hour 
        }
        
    json_data.save_data(data, file_name)