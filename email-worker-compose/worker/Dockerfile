FROM python:3.6
LABEL maintainer 'Marcos'

# sem usar o buffer para printar mensagens
ENV PYTHONUNBUFFERED 1 
RUN pip install redis==2.10.5

# especifica um executavel padrao
ENTRYPOINT [ "/usr/local/bin/python" ]
