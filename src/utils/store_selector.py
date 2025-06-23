from typing import List, Dict
from config import SCRAPE_TARGETS

# User selects stores with numbers -> the (numbers - 1) is the index in "available_stores"
# User can select multiple stores by separating the numbers with a comma
# User can unselect a store by selecting the same number again
# "selected_stores" is a list of store keys

def select_stores() -> List[str]:
    """
    Display a toggle list of available stores and let the user select which ones to use.
    Returns a list of selected store keys.
    """
    available_stores = list(SCRAPE_TARGETS.keys())
    selected_stores = []
    
    print("\nAvailable stores:")
    for i, store in enumerate(available_stores, 1):
        print(f"{i}. {store.title()}")
    
    while True:
        try:
            selection = input("\nEnter store numbers to select or unselect (if already selected) a website to scrape or 'done' to continue: ").strip()
            
            if selection.lower() == 'done':
                if not selected_stores:
                    print("Please select at least one store.")
                    continue
                break
            
            # Parse the input numbers
            store_nums = [int(num.strip()) for num in selection.split(',')]
            
            # Toggle selected stores
            for num in store_nums:
                if 1 <= num <= len(available_stores):
                    store_key = available_stores[num - 1]
                    if store_key in selected_stores:
                        selected_stores.remove(store_key)
                    else:
                        selected_stores.append(store_key)
                else:
                    print(f"Invalid store number: {num}")
            
            # Show current selection
            print("\nCurrently selected stores:")
            for store in available_stores:
                status = "[X]" if store in selected_stores else "[ ]"
                print(f"{status} {store.title()}")
                
        except ValueError:
            print("Please enter valid numbers separated by commas.")
            
    return selected_stores 