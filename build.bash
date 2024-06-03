#!/usr/bin/bash

docker compose up -d
sleep 5
bash migration.bash
bash start.bash
