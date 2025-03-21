import asyncio
import time
import aiohttp
import pytest

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Função assíncrona que faz uma requisição por segundo durante 10 segundos
async def make_requests():
    async with aiohttp.ClientSession() as session:
        for _ in range(10):  # 10 requisições por thread
            async with session.get("http://localhost:3000/scrape/copaAmerica") as response:
                print(f"Status: {response.status}")
            await asyncio.sleep(1)  # Espera 1 segundo antes da próxima requisição

# Teste principal
@pytest.mark.asyncio
async def test_multiple_connections():
    start_time = time.perf_counter()

    tasks = []
    for _ in range(100):  # 100 conexões simultâneas
        tasks.append(make_requests())

    await asyncio.gather(*tasks)

    end_time = time.perf_counter()
    print(f"Teste concluído em {end_time - start_time:.2f} segundos")

# Executa o teste
if __name__ == "__main__":
    asyncio.run(test_multiple_connections())
