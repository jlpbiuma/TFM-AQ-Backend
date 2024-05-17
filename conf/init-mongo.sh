#!/bin/bash
mongosh -u "$MONGO_INITDB_ROOT_USERNAME" -p "$MONGO_INITDB_ROOT_PASSWORD" <<EOF
use AQ
db.createCollection("Usuario");
db.createCollection("Sensor");
db.createCollection("Dispositivo");
EOF
