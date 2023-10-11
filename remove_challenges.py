import psutil
import re
import requests
import base64

# Find the LeagueClientUx.exe process
league_process = None
for process in psutil.process_iter(attrs=["pid", "name", "cmdline"]):
    if process.info["name"] == "LeagueClientUx.exe":
        league_process = process
        break

if league_process is not None:
    # Extract the port and auth token from the command line
    command_line = " ".join(league_process.info["cmdline"])
    port_match = re.search(r"--app-port=(\S+?)(\"|\s)", command_line)
    auth_token_match = re.search(r"--remoting-auth-token=(\S+?)(\"|\s)", command_line)

    if port_match and auth_token_match:
        port = port_match.group(1)
        auth_token = auth_token_match.group(1)

        # Define the API URL
        url = f"https://127.0.0.1:{port}/lol-challenges/v1/update-player-preferences/"

        # Define the request headers
        headers = {
            "Authorization": "Basic "
            + base64.b64encode(f"riot:{auth_token}".encode("ascii")).decode("ascii")
        }

        # Disable SSL verification due to self-signed certificates
        session = requests.Session()
        session.verify = False

        # Define the request payload
        payload = {"challengeIds": []}

        # Send the request
        response = session.post(url, headers=headers, json=payload)

        # Output the response
        print(response.text)
    else:
        print("Something went wrong finding the port and auth from LoL.")
else:
    print(
        "LeagueClientUx.exe process not found. Make sure you have League of Legends opened!"
    )
