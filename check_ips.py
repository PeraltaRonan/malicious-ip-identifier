import os
import csv
import requests

input_file = "../output/ips.txt"
output_file = "../output/ip_report.csv"

API_KEY = os.getenv("ABUSEIPDB_API_KEY")
API_URL = "https://api.abuseipdb.com/api/v2/check"

if not API_KEY:
    print("Error: ABUSEIPDB_API_KEY environment variable not set.")
    exit(1)


with open(input_file, "r") as f:
    ips = [line.strip() for line in f if line.strip()]

def is_private_ip(ip: str) -> bool:
    return (
        ip.startswith("10.") or
        ip.startswith("192.168.") or
        ip.startswith("172.16.") or ip.startswith("172.17.") or ip.startswith("172.18.") or
        ip.startswith("172.19.") or ip.startswith("172.2") or ip.startswith("172.3") or
        ip.startswith("127.")
    )

results = []

for ip in ips:
    if is_private_ip(ip):
        print(f"Skipping private IP {ip}")
        continue

    print(f"Checking {ip}...")

    headers = {
        "Key": API_KEY,
        "Accept": "application/json"
    }

    params = {
        "ipAddress": ip,
        "maxAgeInDays": 90
    }

    try:
        response = requests.get(API_URL, headers=headers, params=params, timeout=10)

        if response.status_code != 200:
            print(f"API error for {ip}: HTTP {response.status_code}")
            continue

        data = response.json().get("data", {})

        results.append({
            "IP": ip,
            "ConfidenceScore": data.get("abuseConfidenceScore"),
            "Country": data.get("countryCode"),
            "TotalReports": data.get("totalReports"),
            "IsWhitelisted": data.get("isWhitelisted")
        })

    except Exception as e:
        print(f"Error checking {ip}: {e}")

if not results:
    print("No results returned from API. Check your API key and internet access.")
    exit(1)

with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = results[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)

print(f"Report has been saved in {output_file}.")
