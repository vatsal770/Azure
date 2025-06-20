# extract the key-value pairs from the json file under the "fields" key

import json

def extract_fields_invoice(fields: dict) -> dict:
    extracted = {}

    for key, value in fields.items():
        field_type = value.get("type")

        if field_type == "string":
            extracted[key] = value.get("valueString", "").replace("\n", " ").strip()

        elif field_type == "date":
            extracted[key] = value.get("valueDate", "")

        elif field_type == "time":
            extracted[key] = value.get("valueTime", "")

        elif field_type == "number":
            extracted[key] = value.get("valueNumber", "")

        elif field_type == "integer":
            extracted[key] = value.get("valueInteger", "")

        elif field_type == "boolean":
            extracted[key] = value.get("valueBoolean", "")

        elif field_type == "currency":
            currency = value.get("valueCurrency", {})
            extracted[key] = f"{currency.get('symbol', '')}{currency.get('amount', '')}"

        elif field_type == "address":
            # Use the raw content instead of valueAddress
            extracted[key] = value.get("content", "").replace("\n", " ").strip()

        elif field_type == "object":
            nested_fields = value.get("valueObject", {})
            extracted[key] = extract_fields_invoice(nested_fields)

        elif field_type == "array":
            array_items = value.get("valueArray", [])
            extracted_items = []

            for item in array_items:
                item_type = item.get("type")
                if item_type == "object":
                    # Extract nested fields in arrays like Items[], TaxDetails[]
                    extracted_items.append(extract_fields_invoice(item.get("valueObject", {})))
                elif item_type == "currency":
                    currency = item.get("valueCurrency", {})
                    extracted_items.append(f"{currency.get('symbol', '')}{currency.get('amount', '')}")
                else:
                    value_key = f"value{item_type.capitalize()}"
                    extracted_items.append(item.get(value_key))

            extracted[key] = extracted_items

        else:
            # fallback to raw content
            extracted[key] = value.get("content", "").replace("\n", " ").strip()

    return extracted




def extract_fields_idDocument(fields: dict):
    extracted = {}

    for key, value in fields.items():
        field_type = value.get("type")

        if field_type == "string":
            extracted[key] = value.get("valueString", "").replace("\n", " ").strip()

        elif field_type == "date":
            extracted[key] = value.get("valueDate", "")

        elif field_type == "countryRegion":
            extracted[key] = value.get("valueCountryRegion", "")

        elif field_type == "address":
            extracted[key] = value.get("content", "").replace("\n", " ").strip()

        elif field_type == "object":
            nested_fields = value.get("valueObject", {})
            extracted[key] = extract_fields_idDocument(nested_fields)

        else:
            extracted[key] = value.get("content", "").replace("\n", " ").strip()

    return extracted


