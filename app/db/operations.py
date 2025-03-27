from sqlalchemy.exc import SQLAlchemyError
from .database import SessionLocal
from .models import Campeonato

def save_data(results, name_db):
    """Salva ou atualiza resultados de campeonatos"""
    db = SessionLocal()
    try:
        registro = db.query(Campeonato).filter(Campeonato.campeonato == name_db).first()
        
        if registro:
            registro.resultados = results
            print(f"Campeonato '{name_db}' atualizado")
        else:
            novo_registro = Campeonato(campeonato=name_db, resultados=results)
            db.add(novo_registro)
            print(f"Campeonato '{name_db}' criado")
        
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Erro no banco de dados: {str(e)}")
        return False
    finally:
        db.close()

def load_results(name_db):
    """Carrega resultados de um campeonato"""
    db = SessionLocal()
    try:
        resultado = db.query(Campeonato).filter(Campeonato.campeonato == name_db).first()
        return resultado.resultados if resultado else None
    except SQLAlchemyError as e:
        print(f"Erro ao carregar dados: {str(e)}")
        return None
    finally:
        db.close()