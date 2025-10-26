#!/usr/bin/env python3
import json
import urllib.request
import urllib.error
import sys
from pathlib import Path

# ===== Arguments =====
if len(sys.argv) != 4:
    print(f"Usage: {sys.argv[0]} <logfile> <request_logfile> <webhook_url>")
    sys.exit(1)

last_logfile = Path(sys.argv[1])
last_request_logfile = Path(sys.argv[2])
WEBHOOK_URL = sys.argv[3]

try:
    teams_title = "Restic Last Backup Log"
    teams_message = last_logfile.read_text(encoding="utf-8", errors="ignore")
    teams_message = teams_message.replace("\n", "\n\n")

    payload = json.dumps({
        "title": teams_title,
        "text": teams_message
    }).encode("utf-8")

    req = urllib.request.Request(
        WEBHOOK_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as resp:
            response_body = resp.read().decode("utf-8", errors="ignore")
            status_code = resp.getcode()
    except urllib.error.HTTPError as e:
        status_code = e.code
        response_body = e.read().decode("utf-8", errors="ignore")
    except urllib.error.URLError as e:
        status_code = 0
        response_body = str(e)

    last_request_logfile.write_text(
        f"Status code: {status_code}\n{response_body}",
        encoding="utf-8"
    )

    if 200 <= status_code < 300:
        print("Microsoft Teams notification successfully sent.")
    else:
        print(f"Sending Microsoft Teams notification FAILED. Check {last_request_logfile} for further information.")
        sys.exit(1)

except Exception as e:
    print(f"Error sending Microsoft Teams notification: {e}")
    sys.exit(1)
