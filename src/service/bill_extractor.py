from google import genai
from google.genai import types
import io
import httpx

client = genai.Client(api_key="AIzaSyBFzEpUqipRBNWnNxxfrjY53mJCEck62gU")

def extract_bill_from_pdf(pdf_url: str):
    """Returns the final HackRx JSON from Gemini."""
    
    # Download file
    doc_io = io.BytesIO(httpx.get(pdf_url).content)

    sample_doc = client.files.upload(
        file=doc_io,
        config=dict(mime_type="application/pdf")
    )

    # First call: Page-wise OCR
    ocr_instructions = """
    You are an OCR Model that extracts text from scanned documents (PDFs).

    TASK:
    - Extract text accurately from each page of the document.
    - Return the result in a valid JSON format.

    OUTPUT FORMAT (Example):
    {
    "pages": [
        {
        "page_number": 1,
        "text": "Extracted text from page 1..."
        },
        {
        "page_number": 2,
        "text": "Extracted text from page 2..."
        }
    ]
    }

    NOTES:
    - Maintain page order.
    - Do not merge text from different pages.
    - Return only the JSON output, no explanations.
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[sample_doc],
        config=types.GenerateContentConfig(system_instruction=ocr_instructions)
    )
    ocr_usage = response.usage_metadata
    ocr_json_text = response.text

    # Second call: Structured bill extraction
    parsing_instructions = """
    You are a medical bill line-item extractor.

    INPUT:
    - OCR JSON containing pages with text.

    TASK:
    - For each page, extract only billable line items and quantities.

    OUTPUT FORMAT (STRICT):
    {
    "pagewise_line_items": [
        {
        "page_no": "string",
        "bill_items": [
            {
            "item_name": "string",
            "item_amount": float,
            "item_rate": float,
            "item_quantity": float
            }
        ]
        }
    ]
    }

    RULES:
    - Include ONLY billable items:
    room charges, consultations, services, lab tests, medicines.
    - Exclude:
    totals, discounts, advances, Sub Total, Grand Total, Net Payable, Pharmacy Charge.
    - Deduplicate SAME item(s) on the SAME page:
    item_quantity = sum
    item_amount = sum
    item_rate stays same.
    - Maintain original page order.
    - If a page contains no billable items:
    include empty bill_items array.

    IMPORTANT:
    - Do NOT include fields other than those in the format.
    - Do NOT include is_success, data, total counts, or reconciled amount.
    - NO backticks or markdown fences — return ONLY JSON.
    - The JSON MUST be syntactically valid.
    """
    
    response2 = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=ocr_json_text,
        config=types.GenerateContentConfig(system_instruction=parsing_instructions)
    )
    
    parse_usage = response2.usage_metadata
    
    usage = {
    "input_tokens": (ocr_usage.prompt_token_count if ocr_usage else 0) +
                    (parse_usage.prompt_token_count if parse_usage else 0),
    "output_tokens": (ocr_usage.candidates_token_count if ocr_usage else 0) +
                     (parse_usage.candidates_token_count if parse_usage else 0),
    "total_tokens": (ocr_usage.total_token_count if ocr_usage else 0) +
                    (parse_usage.total_token_count if parse_usage else 0)
    }


    raw_text = response2.text
    text = raw_text.strip()

    # Remove Markdown code fences if present
    if text.startswith("```json"):
        text = text[len("```json"):].strip()
    if text.startswith("```"):
        text = text[len("```"):].strip()
    if text.endswith("```"):
        text = text[:-3].strip()

    return text, usage
