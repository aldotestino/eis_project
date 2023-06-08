#! /bin/bash
echo "--> 🚀 Starting db, api, frontend..."
docker compose build && docker compose up -d && echo "--> ✅ Succesfully started!" || (echo "--> ❌ Something wrong happened! Exiting..." && exit)
sleep 5
echo "--> 🚀 Starting sensor..."
pm2 start ./sensor/ecosystem.config.js && echo "--> ✅ Succesfully started!" || (echo "--> ❌ Something wrong happened! Exiting..." && echo "--> ✋ Stopping containers:" && docker container stop db api frontend && exit)