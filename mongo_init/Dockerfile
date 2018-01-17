FROM mongo
COPY export_servers.json /docker-entrypoint-initdb.d/import_servers.json
CMD mongoimport --host mongodb --db servers --collection machines --type json --file /docker-entrypoint-initdb.d/import_servers.json --jsonArray 