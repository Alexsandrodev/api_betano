from apscheduler.schedulers.background import BackgroundScheduler
from app.utils import dados_jogos
from app.scraping import atualizador
from app.utils import dados_jogos

scheduler = BackgroundScheduler()
scheduler.add_job(
    atualizador.agendamento_atualizacao,
    'cron',
    minute = ','.join(map(str, dados_jogos.minutosCopaAmerica)),
    second = 40,
    args=[dados_jogos.campeonatos[0], "copaAmerica.json"]
)  # Copa America

scheduler.add_job(
    atualizador.agendamento_atualizacao,
    'cron',
    minute = ','.join(map(str, dados_jogos.minutosTacaGloriaEterna)),
    second = 40,
    args=[dados_jogos.campeonatos[1], "tacaGloriaEterna.json"]
)  # Taca Gloria Eterna

scheduler.add_job(
    atualizador.agendamento_atualizacao,
    'cron',
    minute = ','.join(map(str, dados_jogos.minutosEuro)),
    second = 40,
    args=[dados_jogos.campeonatos[2], "euro.json"]
)  # euro

scheduler.add_job(
    atualizador.agendamento_atualizacao,
    'cron',
    minute = ','.join(map(str, dados_jogos.minutosBritishDerbies)),
    second = 40,
    args=[dados_jogos.campeonatos[3], "britishDerbies.json"]
)  # British Derbies

scheduler.add_job(
    atualizador.agendamento_atualizacao,
    'cron',
    minute = ','.join(map(str, dados_jogos.minutosLigaEspanhola)),
    second = 40,
    args=[dados_jogos.campeonatos[4], "ligaEspanhola.json"]
)  # Liga Espanhola

scheduler.add_job(
    atualizador.agendamento_atualizacao,
    'cron',
    minute = ','.join(map(str, dados_jogos.minutosScudettoItaliano)),
    second = 40,
    args=[dados_jogos.campeonatos[5], "scudettoItaliano.json"]
)  # Scudetto Italiano

scheduler.add_job(
    atualizador.agendamento_atualizacao,
    'cron',
    minute = ','.join(map(str, dados_jogos.minutosCampeonatoItaliano)),
    second = 40,
    args=[dados_jogos.campeonatos[6], "campeonatoItaliano.json"]
)  # Campeonato Italiano

scheduler.add_job(
    atualizador.agendamento_atualizacao,
    'cron',
    minute = ','.join(map(str, dados_jogos.minutosCopaDasEstrelas)),
    second = 40,
    args=[dados_jogos.campeonatos[7], "copaDasEstrelas.json"]
)  # Copa Das Estrelas