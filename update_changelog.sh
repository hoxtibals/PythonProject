#!/bin/bash

# Set the path to your CHANGELOG.md file
changelog_file="CHANGELOG.md"

# Fetch commit comments and append them to the changelog file
git log --format="- %s" >>"$changelog_file"
