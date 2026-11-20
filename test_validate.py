"""Run with:  python test_validate.py   (no extra libraries needed)"""
from validate_contacts import email_reason, phone_reason

GOOD_EMAILS = ["a.b1@company.org", "x_y+z@mail.example.co.uk"]
BAD_EMAILS = {"namegmail.com": "missing @", "a@@gmail.com": "more than one @",
              "@yahoo.com": "empty username", "a@gmail": "invalid domain",
              "a@.com": "invalid domain", "a b@gmail.com": "contains spaces", "": "empty"}
GOOD_PHONES = ["01012345678", "+201012345678", "01112345678", "01212345678", "01512345678"]
BAD_PHONES = {"12345": "wrong length or invalid prefix", "+1555123456": "not an Egyptian country code",
              "01712345678": "wrong length or invalid prefix", "0101234abcd": "contains letters",
              "010-123-4567": "contains invalid characters", "0111111111111": "wrong length or invalid prefix",
              "": "empty"}

for e in GOOD_EMAILS: assert email_reason(e) == "", e
for e, r in BAD_EMAILS.items(): assert email_reason(e) == r, (e, email_reason(e))
for p in GOOD_PHONES: assert phone_reason(p) == "", p
for p, r in BAD_PHONES.items(): assert phone_reason(p) == r, (p, phone_reason(p))
print("All tests passed.")
