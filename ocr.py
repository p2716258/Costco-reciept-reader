import re
import pytesseract
from PIL import Image
import pandas as pd
import argparse

# Define a function to parse the receipt
'''
def parse_receipt(image_path):
    try:
        # Open and read the image with OCR
        image = Image.open(image_path)
    except FileNotFoundError:
        print(f"Error: The file at {image_path} was not found.")
        return None
    except Exception as e:
        print(f"Error opening image: {e}")
        return None

    try:
        receipt_text = pytesseract.image_to_string(image, config="--psm 6")
    except Exception as e:
        print(f"Error during OCR: {e}")
        return None

    # Initialize a list to store parsed data
    parsed_items = []

    # Split text into lines
    lines = receipt_text.strip().split("\n")
    i = 0

    while i < len(lines):
        line = lines[i].strip()
        match = re.match(r"(.+?)\s1x\s([\d.]+)\s([A-Z])$", line)
        
        if match:
            item_name = match.group(1)
            price = float(match.group(2))
            vat_suffix = match.group(3)
            vat_applicable = "Yes" if vat_suffix == "A" else "No"
            
            # Check if the next line is a discount (same item with negative price)
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                discount_match = re.match(rf"{re.escape(item_name)}\s-\s?([\d.]+)\s{vat_suffix}$", next_line)
                
                if discount_match:
                    discount = float(discount_match.group(1))
                    price -= discount  # Apply discount to the price
                    i += 1  # Skip the discount line
            
            # Append parsed item to the list
            parsed_items.append({"Item": item_name, "Price (Pre-VAT)": price, "VAT Applicable": vat_applicable})
        
        i += 1

    # Convert parsed items to a DataFrame
    df_parsed_items = pd.DataFrame(parsed_items)
    return df_parsed_items

    
'''
def parse_receipt(image_path):
    try:
        # Open and read the image with OCR
        image = Image.open(image_path)
    except FileNotFoundError:
        print(f"Error: The file at {image_path} was not found.")
        return None
    except Exception as e:
        print(f"Error opening image: {e}")
        return None

    try:
        receipt_text = pytesseract.image_to_string(image, config="--psm 6")
        print("OCR Output:\n", receipt_text)  # Print the OCR output
    except Exception as e:
        print(f"Error during OCR: {e}")
        return None

    # Initialize a list to store parsed data
    parsed_items = []
    # (Rest of the parsing logic remains unchanged)
# Main function to handle command-line arguments
def main():
    parser = argparse.ArgumentParser(description="Parse a receipt image.")
    parser.add_argument("image_path", help="Path to the receipt image")
    args = parser.parse_args()
    
    # Run the function and save to CSV
    df = parse_receipt(args.image_path)
    if df is not None:
        df.to_csv("parsed_receipt.csv", index=False)  # Save to CSV instead of Excel
        print("Data saved to parsed_receipt.csv")
    else:
        print("Failed to parse receipt. No data to save.")

if __name__ == "__main__":
    main()