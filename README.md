<header>
  <h1> 
    Curso de Docker
    <img style='width: 50px;' src='https://github.com/marcosgregorio/curso-docker/assets/78617642/c4003348-128b-46b2-8210-44cb9ff9651a'/>     
  </h1> 
 
  </header>
<div style='display:flex'>
  <img src='https://img.shields.io/badge/Docker-blue' />
  <img src='https://img.shields.io/badge/Python-3.6-blue' />
  <img src='https://img.shields.io/badge/Postgres-9.6-purple' />
  <img src='https://img.shields.io/badge/Redis-3.2-red' />
</div>

Repositorio com aulas do curso de docker da Cod3r.
Tambem se foi feito um projeto de envio de emails em formato de micro-services e gerenciados com o docker.

| 🪧 Informações        | 🚀                                                |
| --------------------- | ------------------------------------------------- |
| ✨ Nome               | Docker: Ferramenta essencial para desenvolvedores |
| 🏷️ Tecnologias usadas | Docker, Docker compose, Python, Mongo, Postgres   |

### 💡 Email-Worker-Compose

Durante minha prática com o Docker, fiz um exercício que reunia quase tudo o que o Docker tem a oferecer:
Imagens, containers e a orquestração desses containers.

### 🏘️ Arquitetura da aplicação

  <img style='width:550px; height:450px' src='https://github.com/marcosgregorio/weather-forecast/assets/78617642/b9678099-43f5-42e4-b2a2-a78db6c96d44'>

Componentes:

<li>Servidor web</li>
<li>Banco de dados</li>
<li>Gerenciamento de filas</li>
<li>Workers para o envio de e-mail (escalável)</li>
<li>Aplicação principal</li>

#

_A aplicação inteira é isolada, no sentido de que, cada container é isolado em sua propria rede
e apenas os containers que possuem acesso a aquela rede conseguem 'ver'/acessar aquele outro container_

### 🐳 Descrevendo a composição dos serviços com docker-compose

![compose code ‑ Made with FlexClip](https://github.com/marcosgregorio/weather-forecast/assets/78617642/a828a440-2584-484a-be8b-73cff55b4b83)

A descrição dos multiplos containers foi feita utilizando um arquivo docker-compose aonde se foi separada os `services`,
`volumes` e portas de rede (`networks`).

### 🐘 Banco de dados

Foi utilizado scripts e volumes para popular o banco dentro do container

#### docker-compose.yml

```yml
version: "3"
volumes:
  dados:
services:
  db:
    image: postgres:9.6
  volumes:
    # Volume dos dados
    - dados:/var/lib/postgresql/data
    # Scripts
    - ./scripts:/scripts
    - ./scripts/init.sql:/docker-entrypoint-initdb.d/init.sql
```

Esse script roda logo ao subir o container do postgres com sucesso.

Para conferir se o banco foi inicializado corretamente, rode o comando:

```bash
docker compose exec db psql -U postgres -f /scripts/check.sql
```

### 🖥️ Proxy reverso

Ocorreu o uso da injeção da configuração do nginx para fazer um proxy reverso.
Assim não deixando mais exposto a porta da aplicação backend.

### 🖥️ 📨 💻 Redes

Foi criado uma dependencia das redes para cada serviço. Assim, isolando cada container.

```yml
version: "3"
volumes:
  dados:
networks:
  banco:
  web:
  fila:
  # ...
```

### ⚙️ Filas e escalabilidade

Houve a necessidade de se criar pseudo-filas usando o redis, subindo multiplas
instância dos containers de serviço `worker`.

#### A conexao com a fila do Redis

```yml
networks:
  # ...
  - fila:
```

#### Serviço do redis

```yml
queue:
  image: redis:3.2
  networks:
    - fila
```

#### Multiplas instancias

```yml
worker:
  build: worker ①
    volumes:
      # Worker
      - ./worker:/worker
  working_dir: /worker
  command: worker.py
  networks:
    - fila
  depends_on:
    - queue
    - app
```

Uso da instrução build no lugar do image para indicar a necessidade de executar um build, neste caso do arquivo `worker/Dockerfile`

_Escalando os workers e especializando o log_

```bash
docker compose up -d
docker compose scale worker=3 &
docker compose logs -f -t worker
```

```Dockerfile
FROM python:3.6
LABEL maintainer 'Juracy Filho <juracy at gmail.com>'

ENV PYTHONUNBUFFERED 1
RUN pip install redis==2.10.5

ENTRYPOINT ["/usr/local/bin/python"]
```

### ⚙️ Boas práticas — Variáveis de ambiente

```yml
app:
  image: python:3.6
  environment:
    - DB_NAME=email_sender
    # ...
```

### ⚙️ Override

Por fim, foi utilizado o override com o arquivo `docker-compose.override.yml` para se fazer uma sobreescrita nas variáveis de ambiente. Pois assim, fica de uma forma mais isolada as variáveis e os serviços.

```yml
version: "3"
services:
  app:
    environment:
      - DB_NAME=email_sender
```
