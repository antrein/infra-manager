import json
from typing import List

from src.models.dns import GetDnsRecord

def sanitize_dns_list(json_content: dict) -> str:
    try:
        # Extract the "result" key, which contains the list of DNS records
        dns_records_json = json_content.get("result", [])

        # Convert each DNS record JSON into a DnsRecord instance
        dns_records = [GetDnsRecord(**record) for record in dns_records_json]

        # Serialize the list of DNS records to JSON
        json_data = [record.dict() for record in dns_records]

        return json_data

    except ValueError as e:
        # Handle JSON parsing errors
        print(f"Error parsing JSON: {e}")

    except Exception as e:
        # Handle other exceptions
        print(f"Error processing DNS records: {e}")