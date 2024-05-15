create DATABASE email_sender;

\c email_sender

CREATE TABLE emails (
    id serial not NULL,
    data timestamp not null default CURRENT_TIMESTAMP,
    assunto varchar(100) not null,
    mensagem varchar (250) not null
)