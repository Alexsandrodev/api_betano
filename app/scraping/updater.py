import json
from app.db import operations
from app.scraping import scraping
from bs4 import BeautifulSoup
from datetime import datetime
from app.scraping.initializer import format_data
from time import time
import gc

def extract_match_data(element):
    """Highly optimized version of data extraction"""
    try:
        # Consolidated extraction in a single operation
        team_elements = element.find_all("div", class_="tw-font-bold tw-flex-1 tw-text-center tw-overflow-hidden tw-text-ellipsis")
        time_element = element.find("span", class_="tw-flex tw-text-xs tw-leading-s tw-text-n-94-dirty-snow tw-px-n tw-py-l tw-border-solid tw-border-r tw-border-n-8-dark-steel")
        result_ht = element.find("div", class_="tw-font-bold tw-text-l tw-leading-l tw-mx-n")
        result_ft = element.find("div", class_="tw-text-xs tw-leading-s tw-text-n-75-smokey")

        return {
            "TimeA": team_elements[0].get_text().strip(),
            "TimeB": team_elements[1].get_text().strip(),
            "Horario": time_element.get_text().strip(),
            "Hora": time_element.get_text().strip().split(":")[0],
            "Minuto": time_element.get_text().strip().split(":")[1],
            "Resultado_HT": result_ht.get_text().strip(),
            "Resultado_FT": result_ft.get_text().strip("() ")
        }
    except Exception as e:
        return {"error": str(e)}

def fetch_results(championship, name_db):
    """Fetches and updates results using Selenium."""
    existing_data = operations.load_results(name_db) 

    page_source = scraping.get_html(championship)
    
    soup = BeautifulSoup(page_source, "lxml")

    elements = soup.find_all("div", class_="tw-flex tw-items-center tw-justify-center tw-mt-m tw-mb-n tw-mx-n tw-text-white tw-text-xs tw-leading-s tw-select-none tw-rounded-s tw-border tw-border-solid tw-transition-colors tw-duration-base tw-ease-out tw-cursor-pointer tw-bg-n-17-black-pearl tw-border-n-17-black-pearl")
    
    matches = soup.find_all("div", {"data-testid": "VirtualsUpcomingEvent"})
    
    extracted_data = [extract_match_data(element) for element in elements]
    
    extracted_data_dict = {
        (d["TimeA"], d["TimeB"], d["Hora"]): d for d in extracted_data
    }

    for hora, linhas in existing_data['Linhas'].items():
        for dados in linhas:
            chave = (dados["TimeA"], dados["TimeB"], dados["Hora"])
            if chave in extracted_data_dict:
                existing_data["ultimaAtualizacao"] = scraping.data_atualizacao()
                dados.update(extracted_data_dict[chave])
    
    for jogo in matches:
        novo_jogo = format_data(jogo, soup)

        hora = novo_jogo["Hora"]    
        if hora not in existing_data["Linhas"]:
            existing_data["Linhas"][hora] = []
        
        if len(existing_data["Linhas"][hora]) > 2 and existing_data["Linhas"][hora][0]["Hora"] == novo_jogo["Hora"]: 
            existing_data["Linhas"][hora].pop(0)  
        
        if novo_jogo not in existing_data["Linhas"][hora]:
            existing_data["Linhas"][hora].append(novo_jogo)
    
    return existing_data

def schedule_update(championship, name_db):
    """Final optimized function"""
    print(f'\nBuscando resultados para {name_db}...')
    start_time = time()
    
    try:
        matches = fetch_results(championship, name_db)
        if matches is not None:
            operations.save_data(matches, name_db)
    except Exception as e:
        print(f"Erro durante atualização: {str(e)}")
    finally:
        print(f'Tempo total para {name_db}: {time() - start_time:.2f}s')
        gc.collect()
