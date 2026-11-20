# Contact Validation Script (Python + pandas)

A small, reusable script that cleans a contact list. It checks every row for a valid
**email** and a valid **Egyptian mobile number**, adds two True/False columns, and splits
the data into two CSV files.

## What it does

1. Reads a CSV with the columns `id, name, email, phone`
2. Adds `email_valid` and `phone_valid` (True/False)
3. Writes:
   - `valid_contacts.csv`: both email and phone are valid
   - `invalid_contacts.csv`: at least one is invalid
4. Checks that no rows were lost (valid + invalid = total) and prints a summary

## Validation rules

| Field | Valid when |
|-------|-----------|
| Email | One `@`, a non-empty username, and a domain with a dot and a 2+ letter ending (`name@company.org`) |
| Phone | Egyptian mobile: `01X########` or `+201X########`, where X is 0, 1, 2 or 5 (Vodafone, Etisalat, Orange, WE) |

Typical failures it catches: missing `@`, double `@@`, empty username, incomplete domain
(`name@gmail`, `name@.com`), spaces, too-short or too-long numbers, letters in numbers,
non-Egyptian country codes and invalid prefixes (e.g. `017`).

Leading and trailing spaces are trimmed before checking. The original values are never modified.

## Usage

```bash
pip install -r requirements.txt

python validate_contacts.py data/sample_contacts.csv --out-dir sample_output
```

Optional: add `--reasons` to include `email_issue` and `phone_issue` columns that explain
why a value failed.

Example summary:

```
Total rows        : 20
Valid (both OK)   : 8
Invalid (>=1 bad) : 12
  invalid emails  : 6
  invalid phones  : 7
```

## Example output

Input row | `email_valid` | `phone_valid` | File
---|---|---|---
`user1@company.org`, `01012345678` | True | True | valid_contacts.csv
`user3gmail.com`, `01112345678` | False | True | invalid_contacts.csv
`user4@outlook.com`, `12345` | True | False | invalid_contacts.csv
`user5@@gmail.com`, `+1555123456` | False | False | invalid_contacts.csv

## Project structure

```
contact-validator/
├── validate_contacts.py     # main script
├── test_validate.py         # quick checks for the validation rules
├── requirements.txt
├── data/sample_contacts.csv # 20 fictional contacts for demo
└── sample_output/           # results of running the script on the sample
```

## Tests

```bash
python test_validate.py
```

## Notes

- All sample data is fictional.
- The file is read as text (`dtype=str`) so phone numbers keep their leading zero.
- Want different rules (landlines, spaces such as `+20 10 1234 5678`, duplicate detection)?
  The rules live in two small functions at the top of the script and are easy to change.

## Tech

Python 3, pandas, regular expressions.
