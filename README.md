# Sensehub

## Docker

### Requirements
- Docker
- docker-compose

### How to start

- `git clone https://github.com/MichaelCaraccio/sensehub.git`
- `cd sensehub`
- Change the configuration in `.env-example`, `application/.env-example` and `mysql/.env-example` and rename them (respectively `.env`, `application/.env` and `mysql/.env`)
- Rename `application/passwords-example.py`to `application/passwords.py` and edit it by adding your owner users
- Launch the application : `docker-compose up`
- Seed the database with : `application/seed.sh` from an other terminal

### Thanks

Thank you https://github.com/vishnubob/wait-for-it !
