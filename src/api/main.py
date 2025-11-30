import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.utils.response_formatter import format_to_required_schema
from src.service.bill_extractor import extract_bill_from_pdf
from src.utils.response_formatter import wrap_to_hackrx_schema

app = FastAPI()

class RequestBody(BaseModel):
    document: str

@app.post("/extract-bill-data")
async def extract_bill_data(req: RequestBody):
    raw_output, token_usage = extract_bill_from_pdf(req.document)

    try:
        parsed_json = json.loads(raw_output)
    except:
        # Auto-repair: Try removing stray characters and reparse
        repaired = raw_output.replace("\n", "").replace("\\", "")
        parsed_json = json.loads(repaired)

    wrapped_json = wrap_to_hackrx_schema(parsed_json)
    formatted_json = format_to_required_schema(wrapped_json)

    formatted_json["is_success"] = True
    formatted_json["token_usage"] = token_usage     # ✔ Add token usage tracking

    return formatted_json
