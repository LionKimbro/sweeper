# Capture library

`src/sweeperagent/requests.py` is the S1 capture machine. `make_request()`
validates the caller's request record, generates identity and creation time,
and fills the stable version 1 fields. `create_request()` serializes that
record and publishes it under `db/sweep-requests/<uuid>.json` using a same-
directory temporary file and an exclusive hard link. The temporary file and
directory are synced where the platform supports it.

The request data format is specified in
[`../raw/0002__request-format-v1.json`](../raw/0002__request-format-v1.json).
Capture does not scan, dispatch, or execute requests.
