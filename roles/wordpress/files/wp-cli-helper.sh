#!/bin/bash

exec docker-compose exec -T -u 33:33 wordpress-cli wp "$@"
