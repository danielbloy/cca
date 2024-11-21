#!/bin/bash

# NOTE: First time setup of the host machines:
# Install mkdocs:
#   sudo apt install mkdocs
#
# Install the material theme:
#   sudo apt install python3-pip
#   pip install mkdocs-material
#

# Runs the update job on the hour, every hour. To edit, use "crontab -e" with this value.
# 0 * * * * /root/codeclubadventures.com/scripts/update-repos.sh

# Update the repo
cd /root/codeclubadventures.com
git pull

# Build the Hugo site in the correct location
mkdocs build --site-dir /var/www/codeclubadventures.com
