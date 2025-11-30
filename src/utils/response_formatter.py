import json

def wrap_to_hackrx_schema(parsed_json: dict) -> dict:
    return {
        "is_success": True,
        "data": {
            "pagewise_line_items": parsed_json.get("pagewise_line_items", [])
        }
    }


def format_to_required_schema(parsed_json: dict) -> dict:
    # Remove token_usage if exists
    if "token_usage" in parsed_json:
        del parsed_json["token_usage"]
    
    # Navigate to data
    data_section = parsed_json.get("data", {})

    total_amount = 0
    total_items = 0

    for page in data_section.get("pagewise_line_items", []):
        
        # Remove page_type if present
        if "page_type" in page:
            del page["page_type"]

        # Sum all bill items
        for item in page.get("bill_items", []):
            try:
                total_amount += float(item.get("item_amount", 0))
                total_items += 1
            except:
                pass

    # Update counts and totals
    data_section["total_item_count"] = total_items
    data_section["reconciled_amount"] = round(total_amount, 2)

    parsed_json["data"] = data_section
    return parsed_json
