import re
import json

def parse_receipt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    prices_raw = re.findall(r'\d[\d\s]*,\d{2}', text)
    prices = [p.replace(' ', '').replace(',', '.') for p in prices_raw]
    
    products = re.findall(r'(?m)^\d+\.\n(.*?)\n\d+,\d{3}\s*x', text, flags=re.DOTALL)
    products = [p.replace('\n', ' ').strip() for p in products]

    total_match = re.search(r'ИТОГО:\n([\d\s]+,\d{2})', text)
    if total_match:
        total_str = total_match.group(1).replace(' ', '').replace(',', '.')
        total = float(total_str)
    else:
        total = 0.0

    date_match = re.search(r'Время:\s*(\d{2}\.\d{2}\.\d{4})', text)
    date = date_match.group(1) if date_match else "Not found"
    
    time_match = re.search(r'Время:.*?\s(\d{2}:\d{2}:\d{2})', text)
    time = time_match.group(1) if time_match else "Not found"

    payment_match = re.search(r'(Банковская карта|Наличные)', text)
    payment = payment_match.group(1) if payment_match else "Not found"

    receipt_data = {
        "date": date,
        "time": time,
        "items": products,
        "all_prices_found": prices,
        "total_amount": total,
        "payment_method": payment
    }
    
    return json.dumps(receipt_data, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    result = parse_receipt('raw.txt')
    print(result)
