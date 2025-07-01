from typing import List, Tuple
from processing.microcenter import process_microcenter
from utils import select_stores

async def process_store(store: str, search_param: str | None) -> str:
    """Process a single store and return the CSV filename."""
    if store == "microcenter":
        return await process_microcenter(search_param)
    else:
        print(f"Handler for {store} not implemented yet")
        return None

async def run() -> List[Tuple[str, str]]:
    """Run the script in interactive mode with user input."""
    processed_files = []
    
    # First, let user select stores
    selected_stores = select_stores()
    print(f"\nSelected stores: {', '.join(store.title() for store in selected_stores)}")
    
    # Get search parameter
    search_param = input("\nEnter the search parameter: ")
    
    # Process each selected store
    for store in selected_stores:
        print(f"\nProcessing {store.title()}...")
        file_name = await process_store(store, search_param)
        if file_name:
            processed_files.append((file_name, search_param))
            print(f"Data written to src/data/{file_name}")

    return processed_files 