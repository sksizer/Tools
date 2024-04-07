#!/bin/bash

# Check for unstaged changes
if ! git diff --exit-code > /dev/null; then
    echo "There are unstaged changes."
    exit 1
fi

# Check for staged but uncommitted changes
if ! git diff --cached --exit-code > /dev/null; then
    echo "There are staged but uncommitted changes."
    exit 1
fi

echo "No unstaged or uncommitted changes detected."
exit 0
