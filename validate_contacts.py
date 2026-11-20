#!/usr/bin/env python3
"""
Contact validation: check emails and Egyptian mobile numbers in a CSV.

Adds two columns (email_valid, phone_valid), then splits the data into:
  - valid_contacts.csv   : both email and phone are valid
  - invalid_contacts.csv : at least one of them is invalid

Usage:
    python validate_contacts.py data/sample_contacts.csv
    python validate_contacts.py contacts.csv --out-dir output --reasons
"""
import argparse
import re
import sys
from pathlib import Path

import pandas as pd

# Email: local part, one "@", domain with at least one dot and a 2+ letter TLD.
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}$")

# Egyptian mobile: 01X######## or +201X########, X in {0,1,2,5}
# (Vodafone 010, Etisalat 011, Orange 012, WE 015).
PHONE_RE = re.compile(r"^(?:\+20|0)1[0125]\d{8}$")


def email_reason(value) -> str:
    """Return '' if the email is valid, otherwise a short reason."""
    if pd.isna(value) or str(value).strip() == "":
        return "empty"
    v = str(value).strip()
    if " " in v:
        return "contains spaces"
    if v.count("@") == 0:
        return "missing @"
    if v.count("@") > 1:
        return "more than one @"
    if v.startswith("@"):
        return "empty username"
    if not EMAIL_RE.match(v):
        return "invalid domain"
    return ""


def phone_reason(value) -> str:
    """Return '' if the phone is a valid Egyptian mobile, otherwise a short reason."""
    if pd.isna(value) or str(value).strip() == "":
        return "empty"
    v = str(value).strip()
    if re.search(r"[A-Za-z]", v):
        return "contains letters"
    if not re.fullmatch(r"\+?\d+", v):
        return "contains invalid characters"
    if v.startswith("+") and not v.startswith("+20"):
        return "not an Egyptian country code"
    if not PHONE_RE.match(v):
        return "wrong length or invalid prefix"
    return ""


def validate(df: pd.DataFrame, add_reasons: bool = False) -> pd.DataFrame:
    """Return a copy of df with email_valid / phone_valid (and optional reasons)."""
    out = df.copy()
    e_reason = out["email"].apply(email_reason)
    p_reason = out["phone"].apply(phone_reason)
    out["email_valid"] = e_reason.eq("")
    out["phone_valid"] = p_reason.eq("")
    if add_reasons:
        out["email_issue"] = e_reason
        out["phone_issue"] = p_reason
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Validate emails and Egyptian mobile numbers.")
    ap.add_argument("input", help="Input CSV with columns: id, name, email, phone")
    ap.add_argument("--out-dir", default=".", help="Where to write the output files")
    ap.add_argument("--reasons", action="store_true",
                    help="Also add email_issue / phone_issue columns explaining failures")
    args = ap.parse_args(argv)

    # dtype=str keeps leading zeros in phone numbers (01012345678 stays intact).
    df = pd.read_csv(args.input, dtype=str, keep_default_na=False)
    missing = {"id", "name", "email", "phone"} - set(df.columns)
    if missing:
        print(f"Missing required columns: {sorted(missing)}", file=sys.stderr)
        return 1

    result = validate(df, add_reasons=args.reasons)
    both_ok = result["email_valid"] & result["phone_valid"]
    valid, invalid = result[both_ok], result[~both_ok]

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    valid.to_csv(out_dir / "valid_contacts.csv", index=False)
    invalid.to_csv(out_dir / "invalid_contacts.csv", index=False)

    # Sanity check: nothing lost, nothing duplicated.
    assert len(valid) + len(invalid) == len(df), "Row count mismatch!"

    print(f"Total rows        : {len(df)}")
    print(f"Valid (both OK)   : {len(valid)}")
    print(f"Invalid (>=1 bad) : {len(invalid)}")
    print(f"  invalid emails  : {(~result['email_valid']).sum()}")
    print(f"  invalid phones  : {(~result['phone_valid']).sum()}")
    print(f"Files written to  : {out_dir.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
