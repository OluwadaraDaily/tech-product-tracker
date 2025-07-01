from typing import List, Tuple
from processing.microcenter import process_microcenter

# Default configurations
DEFAULT_STORES = ["microcenter"]
DOES_STORE_HAVE_SEARCH_PARAMS = {
    "microcenter": True
}
DEFAULT_SEARCH_PARAMS = {
    "microcenter": [
        "gpu",
        "cpu",
        # "ram",
        # "ssd",
        # "macbook",
        # "monitor"
    ]
}

async def process_store(store: str, search_param: str | None) -> str:
    """Process a single store and return the CSV filename."""
    if store == "microcenter":
        return await process_microcenter(search_param)
    else:
        print(f"Handler for {store} not implemented yet")
        return None

async def run() -> List[Tuple[str, str]]:
    """Run the script in automated mode with default parameters."""
    processed_files = []
    
    # Process each store with each search parameter
    for store in DEFAULT_STORES:
        if DOES_STORE_HAVE_SEARCH_PARAMS[store]:
            for search_param in DEFAULT_SEARCH_PARAMS[store]:
                print(f"\nProcessing {store.title()} for {search_param}...")
                file_name = await process_store(store, search_param)
                if file_name:
                    processed_files.append((file_name, search_param))
                    print(f"Data written to src/data/{file_name}")
        else:
            print(f"\nProcessing {store.title()}...")
            file_name = await process_store(store, None)
            if file_name:
                processed_files.append((file_name, None))

    return processed_files 