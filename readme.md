

# HackRx Datathon — Billing Extraction API

### **Author:** Shrikant Dighole

### **Service Name:** billing_extraction

### **Deployment Endpoint:**

```
POST https://two2b2244-bajaj-datathon.onrender.com/extract-bill-data
```

---

## 1️⃣ Problem Statement

Hospitals generate invoices with:

* Multiple pages
* Different layouts (Bill Detail / Pharmacy / Final Bill)
* Multiple sub-totals, summary sections
* Duplicate charge entries and aggregated totals

The Datathon challenge is to:

> Extract **all individual bill line items** with **no misses** and **no double counting**, while computing accurate **total_item_count** and **reconciled_amount** aligned with the **actual bill total**.

**Primary Performance Metric**

> |Actual Bill Total − AI Reconciled Total| → **Aim for ZERO**

---

## 2️⃣ Objective of This System

This solution:
✔ Reads PDF from **any public URL**
✔ Extracts **all billable** (item_name, quantity, rate, amount) entries
✔ Eliminates:

* Page summary totals
* Final total/Grand total duplication
* Repeated line items within same page

✔ Produces **HackRx-approved JSON schema**
✔ Reports **token usage** per request
✔ Works across mixed document formats

---

## 3️⃣ Tech Stack

| Layer         | Tool                               |
| ------------- | ---------------------------------- |
| OCR + Parsing | Google Gemini (Vision + Text)      |
| Backend API   | FastAPI + Python                   |
| Deployment    | Render Web Service                 |
| Data Handling | httpx, pydantic, JSON sanitization |
| Validation    | Deterministic numeric checks       |

---

## 4️⃣ API Usage (for judges)

**Endpoint**

```
POST /extract-bill-data
```

Full URL:

```
https://two2b2244-bajaj-datathon.onrender.com/extract-bill-data
```

### Request Body (JSON)

```json
{
  "document": "RAW_PUBLIC_PDF_URL"
}
```

📌 Must be a **downloadable** file URL
Not HTML, not authentication-restricted

---

## 5️⃣ Response Format (Guaranteed Schema)

```json
{
  "is_success": true,
  "token_usage": {
    "total_tokens": 0,
    "input_tokens": 0,
    "output_tokens": 0
  },
  "data": {
    "pagewise_line_items": [
      {
        "page_no": "1",
        "bill_items": [
          {
            "item_name": "string",
            "item_amount": 0.0,
            "item_rate": 0.0,
            "item_quantity": 0.0
          }
        ]
      }
    ],
    "total_item_count": 0,
    "reconciled_amount": 0.0
  }
}
```

**Field Validations**

* All numeric fields are `float`
* `page_no` is string for consistency
* `is_success` true only if parsing succeeded

---

## 6️⃣ System Workflow

```
PDF URL → Download
        → Gemini Files Upload
        → Gemini OCR (pagewise JSON text)
        → Gemini Parser (compact extraction)
        → Post-processing:
            - Deduplicate per page
            - Remove summary totals
            - Normalize numerics
            - Compute reconciled_amount
        → Strict JSON schema → Response
```

---

## 7️⃣ Error Handling

If anything fails (bad URL, PDF unreadable, AI error):

```json
{
  "is_success": false,
  "reason": "Failed to extract bill data"
}
```

---

## 8️⃣ Compliance with HackRx Requirements

| Requirement                   | Solution                                   |
| ----------------------------- | ------------------------------------------ |
| Extract line items exactly    | ✔ Page-wise structured parsing             |
| Support multiple bill formats | ✔ Rules for Final/Pharmacy/Bill Detail     |
| Do not double count           | ✔ Summary sections removed + dedupe        |
| Compute total correctly       | ✔ `reconciled_amount`                      |
| Return item_count             | ✔ Included                                 |
| Strict JSON schema            | ✔ Validated in formatter                   |
| Minimal hallucination risk    | ✔ Small LLM output + rule-based processing |
| Token reporting               | ✔ Included for every request               |
| API deployed                  | ✔ Public cloud API                         |

---

## 9️⃣ Testing Instructions (Judges)

1️⃣ Open Swagger docs:

```
https://two2b2244-bajaj-datathon.onrender.com/docs
```

2️⃣ Select:

> POST /extract-bill-data → Try it out

3️⃣ Paste:

```json
{
  "document": "https://raw.githubusercontent.com/Shrikant133/public/main/TRAINING_SAMPLES/train_sample_1.pdf"
}
```

4️⃣ Execute → JSON result displays

---

## 🔟 Limitations + Future Enhancements

| Current Limitation                  | Planned Enhancement                       |
| ----------------------------------- | ----------------------------------------- |
| Handwritten text extraction limited | Add handwriting-optimized OCR             |
| Occasional OCR noise                | Apply CV-based cleaning (deskew, denoise) |
| Token usage may vary                | Add cost-predictive handling              |

---

## 1️⃣1️⃣ Local Setup

```bash
git clone <repo_url>
cd Bajaj
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.api.main:app --reload
```

API locally:

```
http://127.0.0.1:8000/extract-bill-data
```

Swagger:

```
http://127.0.0.1:8000/docs
```

---

## 1️⃣2️⃣ Conclusion

✔ Fully working, deployed API
✔ Schema-correct outputs
✔ Reconciled totals
✔ Token tracking
✔ High extraction accuracy
✔ Submission-ready

This solution is ready for automated scoring in the HackRx Datathon.

---

### Contact

> **Shrikant Dighole**
> Email: shrikantdighole2005313@gmail.com

---