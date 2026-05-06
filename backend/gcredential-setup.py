import os
from pathlib import Path

def setup_google_credentials() -> None:
    """
    Load the service account JSON from the environment variable
    and write it to a temp file, then point GOOGLE_APPLICATION_CREDENTIALS
    to that file so Google libraries can use it.
    """
    service_account_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not service_account_json:
        # No creds set in environment – optionally log or just return
        return

    creds_path = Path("/tmp/google-service-account.json")
    creds_path.write_text(service_account_json)

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(creds_path)