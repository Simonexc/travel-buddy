#!/bin/bash

# Update and install necessary packages
sudo apt-get update
sudo apt-get install -y python3-pip python3-dev git

# clone repository if travel-buddy dir doesn't exist
if [ ! -d "travel-buddy" ]; then
    git clone https://github.com/Simonexc/travel-buddy.git
    cd travel-buddy
else
   cd travel-buddy
   git fetch origin
   git pull
fi
sudo pip3 install -r requirements.txt

# Fetch secrets from Secret Manager and set them as environment variables
export DISCORD_TOKEN=$(gcloud secrets versions access latest --secret="discord-token")
export DB_PASSWORD=$(gcloud secrets versions access latest --secret="db-password")
export DISCORD_GUILD=$(gcloud secrets versions access latest --secret="discord-guild")
export GCP_PLACES_API_KEY=$(gcloud secrets versions access latest --secret="gcp-places-api-key")
export PROJECT_ID=$(gcloud secrets versions access latest --secret="project-id")
export REGION=$(gcloud secrets versions access latest --secret="region")
export SPANNER_ID=$(gcloud secrets versions access latest --secret="spanner-id")
export SPANNER_DATABASE_ID=$(gcloud secrets versions access latest --secret="spanner-database-id")

# Run your bot using Python
nohup python3 bot.py &
