FROM nginx:latest
LABEL maintainer 'Aluno Cod3r'

RUN echo '<h1>Sem conteudo</h1>' > /usr/share/nginx/html/conteudo.html
# copiar qualquer arquivo html para a pasta de destino
COPY *.html /usr/share/nginx/html/
