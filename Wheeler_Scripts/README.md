# Subsetting the Wheeler Recreation Form for Work Duty and Emergency Contacts
The Wheeler Recreation Registration Form is amazinly comprehensive, but not really friendly for downstream efforts like setting up Swim Registration, Work Duty forms, and Emergency contacts. These scripts attempt to restructure and subet the form for different use cases.

The reformat_registration.py script takes in the downloaded Member registration in CSV format. It reheaders the CSV file, and the subsets it into two outputs: a work_duties_full.csv and and emergency_contacts.csv.

## Requirements
For running this script, you will need:

1. The downloaded CSV (comma separated) of the Registration form (I've called it registration.csv for the example below)
2. Python3 installed

## Usage
python3 reformat_registration.py registration.csv

