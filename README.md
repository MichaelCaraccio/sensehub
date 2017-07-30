# Sensehub

## Docker

### Requirements
- Docker
- docker-compose

### How to start

- `git clone https://github.com/MichaelCaraccio/sensehub.git`
- `cd sensehub`
- Change the configuration in `.env-example`, `application/.env-example` and `mysql/.env-example`
- Rename them (respectively `.env`, `application/.env` and `mysql/.env`)
- `docker-compose up`
- `application/seed.sh` from an other terminal

### Thanks

Thank you https://github.com/vishnubob/wait-for-it !
