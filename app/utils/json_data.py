import os
import json
from pathlib import Path

# Define o caminho base para os dados
BASE_DIR = Path(__file__).parent.parent / "data"
BASE_DIR.mkdir(exist_ok=True)  

def save_data(dados, file_path):
    """Salva os dados em um arquivo JSON no diretório app/data"""
    file_path = BASE_DIR / file_path
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        print(f"Dados salvos em: {file_path}")
    except Exception as e:
        print(f"Erro ao salvar dados: {str(e)}")
        raise

def load_data(file_path):
    """Carrega dados de um arquivo JSON"""
    file_path = BASE_DIR / file_path
    if file_path.exists():
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar dados: {str(e)}")
            return {}
    return {}