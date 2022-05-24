# EcommerceBackend

## Local development
### Build
- `docker-compose up -d --build`
### Monitoring logs
- `docker-compose logs -f -t <service-name>` (db, web, traefik)

### Entering containers
- `docker-compose web exec /bin/bash`
- `docker-compose exec db psql --username=ecommerce --dbname=ecommerce_db`
