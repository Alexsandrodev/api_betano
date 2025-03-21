from app.scraping import scraping
from bs4 import BeautifulSoup
from app.utils import jsonData
from collections import defaultdict

def formatar_dados(element, soup):
    teams = element.find_all("div", class_="tw-text-xs tw-font-regular tw-leading-s tw-whitespace-nowrap tw-text-ellipsis tw-overflow-hidden")
    timeA = teams[0].get_text().strip()
    timeB = teams[1].get_text().strip()
            
            
    try:
        horario = element.find("span", class_="tw-block tw-text-xs tw-font-regular tw-leading-s").get_text()
    except: 
        header = soup.find("div", class_ = "tw-text-xs tw-leading-s tw-flex tw-flex-col tw-justify-center tw-py-n tw-select-none tw-relative tw-bg-n-13-steel tw-items-center")
        horario = header.find("span", class_ = "tw-text-n-94-dirty-snow").get_text()
            
    horario = horario.strip()
        
    hora, minuto = horario.split(":")
    
    match_info = {
                "TimeA": timeA,
                "TimeB": timeB,
                "Horario": horario,
                "Hora": hora,
                "Minuto": minuto
            }
    
    return match_info

def scrape_data(campeonato:str):
    print("Scraping data from: ", campeonato)
    arquivo = f"{campeonato}.json"
    
    page_source = scraping.gethtml(campeonato)

    
    soup = BeautifulSoup(page_source, "lxml")
    matches_by_hour = defaultdict(list)
    
    elements = soup.find_all("div", {"data-testid": "VirtualsUpcomingEvent"})
    
    for element in elements:
        match_info = formatar_dados(element, soup)
        hora = match_info["Hora"]
            
        matches_by_hour[hora].append(match_info)

    dados = {
            "ultimaAtualizacao": scraping.dataAtualizacao(),
            "Linhas": matches_by_hour 
        }
        
    jsonData.salvar_dados(dados, arquivo)
    
