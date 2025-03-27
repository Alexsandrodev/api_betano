import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
    vus: 100,               // 100 usuários virtuais (simultâneos)
    duration: '30s',        // Duração do teste
  };
  
  export default function () {
    const res = http.get('http://localhost/scrape/euro'); // Altere "123" conforme necessário
    check(res, {
      'Status 200': (r) => r.status === 200, // Verifica se a resposta é HTTP 200
    });
    sleep(1); // Intervalo de 1 segundo entre requisições por VU
  }