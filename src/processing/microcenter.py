from fetchers.microcenter import fetch_microcenter_html
from parsers.microcenter import parse_microcenter_html
from storage.csv_writer import write_to_csv
from storage.db_store import store_products, get_products_with_stats

async def process_microcenter(search_param: str) -> str:
    beautiful_soup_object = await fetch_microcenter_html(search_param)
    data = parse_microcenter_html(beautiful_soup_object)
    
    # Store products in database first
    store_products(data, "microcenter")
    
    # Get updated data from database with price statistics
    products_with_stats = get_products_with_stats(store="microcenter")
    
    # Write the database data to CSV
    file_name = f"microcenter.csv"
    write_to_csv(products_with_stats, file_name)
    
    return file_name