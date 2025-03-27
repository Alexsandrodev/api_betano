from sqlalchemy import Column, Integer, String, JSON
from .database import Base

class Campeonato(Base):
    __tablename__ = "campeonatos"

    id = Column(Integer, primary_key=True, index=True)
    campeonato = Column(String, unique=True, nullable=False)
    resultados = Column(JSON)