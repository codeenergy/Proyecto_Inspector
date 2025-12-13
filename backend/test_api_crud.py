import requests
import json

BASE_URL = "http://localhost:8001"

def test_crud():
    print(f"Testing API at {BASE_URL}")
    
    # 1. Create Target
    print("\n1. Creating Target...")
    new_target = {
        "url": "https://test-crud.com",
        "target_pageviews": 5,
        "ad_click_probability": 0.5,
        "viewport": {"width": 1024, "height": 768},
        "enabled": True
    }
    try:
        res = requests.post(f"{BASE_URL}/targets", json=new_target)
        print(f"POST Status: {res.status_code}")
        print(f"POST Response: {res.text}")
        if res.status_code != 200:
            return
    except Exception as e:
        print(f"POST Failed: {e}")
        return

    # 2. List Targets to find ID
    print("\n2. Listing Targets...")
    try:
        res = requests.get(f"{BASE_URL}/targets")
        targets = res.json().get("data", [])
        target_id = None
        for t in targets:
            if t["url"] == "https://test-crud.com":
                target_id = t["id"]
                break
        print(f"Found Target ID: {target_id}")
    except Exception as e:
        print(f"GET Failed: {e}")
        return

    if not target_id:
        print("Could not find created target ID")
        return

    # 3. Update Target
    print(f"\n3. Updating Target {target_id}...")
    update_data = {
        "url": "https://test-crud-updated.com",
        "target_pageviews": 10,
        "ad_click_probability": 0.1,
        "viewport": {"width": 1024, "height": 768},
        "enabled": False
    }
    try:
        res = requests.put(f"{BASE_URL}/targets/{target_id}", json=update_data)
        print(f"PUT Status: {res.status_code}")
        print(f"PUT Response: {res.text}")
    except Exception as e:
        print(f"PUT Failed: {e}")

    # 4. Delete Target
    print(f"\n4. Deleting Target {target_id}...")
    try:
        res = requests.delete(f"{BASE_URL}/targets/{target_id}")
        print(f"DELETE Status: {res.status_code}")
        print(f"DELETE Response: {res.text}")
    except Exception as e:
        print(f"DELETE Failed: {e}")

if __name__ == "__main__":
    test_crud()
