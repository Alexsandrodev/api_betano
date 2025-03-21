import json
from app.utils import jsonData
from app.scraping import scraping
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from app.scraping.inicializador import formatar_dados
from time import sleep

def extract_match_data(element):
    if not element:
        return {"error": "Elemento não encontrado"}

    try:
        # Extraindo horário
        horario = element.find("span", class_="tw-flex tw-text-xs tw-leading-s tw-text-n-94-dirty-snow tw-px-n tw-py-l tw-border-solid tw-border-r tw-border-n-8-dark-steel").get_text().strip()
        hora, minuto = horario.split(":")

        # Extraindo times
        times = element.find_all("div", class_="tw-font-bold tw-flex-1 tw-text-center tw-overflow-hidden tw-text-ellipsis")
        timeA = times[0].get_text().strip()
        timeB = times[1].get_text().strip()


        # Extraindo resultados
        resultados_HT = element.find("div", class_="tw-font-bold tw-text-l tw-leading-l tw-mx-n").get_text().strip()
        resultado_FT = element.find("div", class_="tw-text-xs tw-leading-s tw-text-n-75-smokey").get_text().strip()

        resultado_FT = resultado_FT.replace("(", "").replace(")", "").strip()

        return {
            "TimeA": timeA,
            "TimeB": timeB,
            "Horario": horario,
            "Hora": hora,
            "Minuto": minuto,
            "Resultado_HT": resultados_HT,
            "Resultado_FT": resultado_FT
        }
    except Exception as e:
        return {"error": str(e)}


def buscar_resultados(campeonato, nome_arquivo):
    """Busca e atualiza os resultados usando Selenium."""
    dados_existentes = jsonData.carregar_dados(nome_arquivo)  # Carrega dados existentes

    # Verifica a última atualização dos dados e remove o último índice se necessário
    ultima_atualizacao = dados_existentes.get("ultimaAtualizacao")
    
    if ultima_atualizacao:
        try:
            # Convertendo a data para o formato correto
            ultima_atualizacao = datetime.strptime(ultima_atualizacao, "%d/%m/%Y %H:%M:%S")  
            
            if (datetime.now() - ultima_atualizacao) > timedelta(hours=24):
                # Remover o último índice de dados antigos se passou 24h
                if "Linhas" in dados_existentes and dados_existentes["Linhas"]:
                    for hora, linhas in dados_existentes["Linhas"].items():
                        if linhas:  
                            dados_existentes["Linhas"][hora] = linhas[:-1]  
        except ValueError as e:
            print(f"Erro ao converter data: {e}")

    page_source = scraping.gethtml(campeonato)
        
    soup = BeautifulSoup(page_source, "lxml")

    elements = soup.find_all("div", class_="tw-flex tw-items-center tw-justify-center tw-mt-m tw-mb-n tw-mx-n tw-text-white tw-text-xs tw-leading-s tw-select-none tw-rounded-s tw-border tw-border-solid tw-transition-colors tw-duration-base tw-ease-out tw-cursor-pointer tw-bg-n-17-black-pearl tw-border-n-17-black-pearl")
    
    jogos = soup.find_all("div", {"data-testid": "VirtualsUpcomingEvent"})
    
    dados_extraidos = [extract_match_data(element) for element in elements]
    
    dados_extraidos_dict = {
        (d["TimeA"], d["TimeB"], d["Hora"]): d for d in dados_extraidos
    }

    for hora, linhas in dados_existentes['Linhas'].items():
        for dados in linhas:
            chave = (dados["TimeA"], dados["TimeB"], dados["Hora"])
            if chave in dados_extraidos_dict:
                dados_existentes["ultimaAtualizacao"] = scraping.dataAtualizacao()
                dados.update(dados_extraidos_dict[chave])
    
    for jogo in jogos:
        novo_jogo = formatar_dados(jogo, soup)

        hora = novo_jogo["Hora"]    
        if hora not in dados_existentes["Linhas"]:
            dados_existentes["Linhas"][hora] = []

        if novo_jogo not in dados_existentes["Linhas"][hora]:
            dados_existentes["Linhas"][hora].append(novo_jogo)
    
    return dados_existentes


def agendamento_atualizacao(campeonato, nome_arquivo):
    """Função agendada para buscar resultados."""
    print(f'\nBuscando resultados para {nome_arquivo}...')
    jogos = buscar_resultados(campeonato, nome_arquivo)
    if jogos != None:
        jsonData.salvar_dados(jogos, nome_arquivo)

