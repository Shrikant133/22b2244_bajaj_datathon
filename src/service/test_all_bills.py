import json
from src.service.bill_extractor import extract_bill_from_pdf
from src.utils.response_formatter import *
import glob

TRAIN_PATH = "TRAINING_SAMPLES/*.pdf"

for file in glob.glob(TRAIN_PATH):
    print("\n==============================")
    print("TESTING:", file)

    raw_output, _ = extract_bill_from_pdf(file)
    parsed_json = json.loads(raw_output)

    wrapped = wrap_to_hackrx_schema(parsed_json)
    formatted = format_to_required_schema(wrapped)

    print("TOTAL ITEMS:", formatted["data"]["total_item_count"])
    print("RECON AMT:", formatted["data"]["reconciled_amount"])
