import requests
import time

def run_test():
    print("="*50)
    print("STARTING CIRCUIT BREAKER FAILURE SIMULATION")
    print("="*50)
    
    for i in range(1, 7):
        print(f"\n[Request {i}] Calling /ask-ai...")
        start_time = time.time()
        
        try:
            response = requests.get("http://127.0.0.1:8000/ask-ai")
            duration = time.time() - start_time
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.json()}")
            print(f"Time Taken: {duration:.2f}s")
            
            # Check for header requirement
            if "X-Student-ID" in response.headers:
                print(f"Header Verified: X-Student-ID = {response.headers['X-Student-ID']}")
            else:
                print("WARNING: X-Student-ID header missing!")
                
        except Exception as e:
            print(f"Request failed: {e}")
        
        if i == 3:
            print("\n" + "!"*50)
            print("FAILURE THRESHOLD REACHED (3). CIRCUIT SHOULD NOW BE OPEN.")
            print("!"*50)

    print("\n" + "="*50)
    print("SIMULATION COMPLETE")
    print("="*50)

if __name__ == "__main__":
    run_test()
