pg_dump -U postgres -h 127.0.0.1 -d solar_controller_telemetry --schema-only -f db_structure.sql


psql -U postgres -h 127.0.0.1 -d solar_controller_telemetry
\i /path/to/your/db_structure.sql


В виде SQL-скрипта:
pg_dump -h localhost -p 5432 -U postgres -F p -f backup3.sql solar_controller_telemetry
