import psycopg2
import os
import redis
import json
from bottle import Bottle, request

class Sender(Bottle):
    def __init__(self):
        super().__init__()
        self.route('/', method='POST', callback=self.send)

        redis_host = os.getenv('REDIS_HOST', 'queue')
        self.fila = redis.StrictRedis(host=redis_host, port=6379, db=0)

        db_host = os.getenv('DB_HOST', 'db')
        db_user = os.getenv('DB_USER', 'postgres')
        db_name = os.getenv('DB_NAME', 'sender')
        db_password = os.getenv('DB_PASSWORD', 'postgres')
        DSN = f'dbname={db_name} user={db_user} host={db_host}, password={db_password}'
        self.conn = psycopg2.connect(DSN)

    def register_message(assunto, mensagem):
        cur = self.conn.cursor()
        SQL = 'INSERT INTO emails (assunto, mensagem) VALUES (%s, %s)'
        cur.execute(SQL, assunto, mensagem)
        self.conn.commit()
        cur.close()
        print("Mensagem registrada com sucesso!")

    def send():
        assunto = request.forms.get('assunto')
        mensagem = request.forms.get('mensagem')
        self.register_message(assunto, mensagem)
        return 'Mensagem enfileirada! Assunto: {} Mensagem {}'.format(assunto, mensagem)

if __name__ == '__main__':
    sender = Sender()
    sender.run(host='0.0.0.0', port=8080, debug=True)