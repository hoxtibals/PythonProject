#!/bin/bash

# Set the path to your CHANGELOG.md file
changelog_file="copy_gitLog.md"

# Fetch commit comments and append them to the changelog file
git log --format="- %s (by %an at %ad)" >>"$changelog_file"
