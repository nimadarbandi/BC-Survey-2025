#!/bin/bash

# Path to the CSV file
DATAFILE="CSV/BC-title-abs.csv"
KEYWORD_FILE="keywords.txt"

# Check if the keywords file exists
if [[ ! -f "$KEYWORD_FILE" ]]; then
    echo "Error: keywords.txt not found!"
    exit 1
fi

# Read keywords from file into an array
keywords=()
while IFS= read -r line || [[ -n "$line" ]]; do
    keywords+=("$line")
done < "$KEYWORD_FILE"

# Create a temporary file to store **unique matching lines** (avoids overcounting in total)
tempfile=$(mktemp)
> "$tempfile"  # Clear the temp file

# Count occurrences for each keyword
for keyword in "${keywords[@]}"; do
    count=$(grep -E "$keyword" "$DATAFILE" | tee -a "$tempfile" | wc -l)
    printf "   %-25s: %d\n" "$keyword" "$count"
done

# Count **unique** matching papers (avoiding duplicates)
unique_total=$(sort -u "$tempfile" | wc -l)

# Display the **corrected** total
printf "Total without duplicates: %d\n" "$unique_total"

# Clean up temporary file
mv "$tempfile" ./

