from fetchers.microcenter import fetch_microcenter_html
from parsers.microcenter import parse_microcenter_html
from storage.csv_writer import write_to_csv
from storage.db_store import store_products, get_products

async def process_microcenter(search_param: str) -> str:
    beautiful_soup_object = await fetch_microcenter_html(search_param)
    data = parse_microcenter_html(beautiful_soup_object)
    
    # Store products in database first
    store_products(data, "microcenter")
    
    # Get updated data from database (including price changes)
    db_products = get_products(store="microcenter")
    
    # Write the database data to CSV
    file_name = f"microcenter.csv"
    write_to_csv(db_products, file_name)
    
    return file_name