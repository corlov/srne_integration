pg_dump -U postgres -h 127.0.0.1 -d solar_controller_telemetry --schema-only -f db_structure.sql


psql -U postgres -h 127.0.0.1 -d solar_controller_telemetry
\i /path/to/your/db_structure.sql
