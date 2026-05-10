Name: Uzair Abbas | Roll Number: BSAI23037

# Building Resilient Distributed Systems: StudySync Fault Tolerance

This repository contains the implementation for **Part 3** of the PDC assignment. The project focuses on solving **Problem 3 (Fault Tolerance)** by implementing a **Circuit Breaker Pattern** in a FastAPI application to handle failures in external LLM API dependencies.

##  Project Overview

StudySync encountered severe performance issues when its external LLM API experienced high latency (60s timeouts). In a naive synchronous architecture, this causes server threads to block, leading to a total application hang. 

This implementation introduces a **Circuit Breaker** that:
1.  **Monitors** failures in the LLM service.
2.  **Trips (Opens)** the circuit after a threshold (3 failures) to prevent blocking calls.
3.  **Provides Fallback** responses immediately while the circuit is open.
4.  **Recovers (Half-Open)** after a timeout (10s) to test if the service has recovered.

##  Tech Stack

- **Backend:** FastAPI (Python)
- **Networking:** Requests (with timeout handling)
- **State Management:** Custom Circuit Breaker Implementation
- **Testing:** Automated failure simulation script

##  Project Structure

```text
.
├── app/
│   ├── __init__.py         # Package marker
│   ├── main.py             # Main FastAPI application & Middleware
│   ├── circuit_breaker.py   # Circuit Breaker logic (Closed, Open, Half-Open states)
│   └── fake_llm.py         # Mock LLM API simulating 60s latency
├── tests/
│   └── test_failure.py     # Script to simulate load and verify circuit behavior
├── requirements.txt         # Project dependencies
└── README.md                # Documentation
```

##  Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YourUsername/PDC-Sp24-BSAI23037-Abbas.git
   cd PDC-Sp24-BSAI23037-Abbas
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

##  Running the Application

To demonstrate the system, you need to run two separate servers:

### 1. Start the Fake LLM API (Simulator)
This server simulates a failing external service with a 60-second delay.
```bash
uvicorn app.fake_llm:app --port 9000
```

### 2. Start the StudySync Backend
Run the main FastAPI application in a new terminal:
```bash
uvicorn app.main:app --port 8000
```

##  Testing the Failure Recovery

The provided test script simulates multiple requests to the AI service. Since the LLM API is slow (60s) and the backend has a 3s timeout, the circuit breaker will trip after 3 failed attempts.

Run the test script:
```bash
python tests/test_failure.py
```

### Expected Output
- **Requests 1-3:** Backend tries to reach LLM, times out after 3s, and records a failure.
- **Request 4+:** Circuit trips to `OPEN` state. Backend immediately returns a **Fallback Response** without waiting for the timeout, saving system resources.
- **After 10s:** The circuit enters `HALF_OPEN` to attempt recovery.
 
##  Visual Demonstration
 
### 1. Before: System Hanging (Naive Implementation)
In this scenario, we bypass the circuit breaker. Notice how each request hangs for **3 seconds** before failing. If we had 1,000 users, the entire server would stop responding because all threads would be busy waiting for this slow API.
 
<img width="1366" height="470" alt="image" src="https://github.com/user-attachments/assets/f669ad98-aa7a-4f72-a446-b4638c8c2bd0" />
 
### 2. After: System Resilient (Circuit Breaker Implementation)
Here, the Circuit Breaker is active. After the 3rd failure, it "trips" and opens the circuit. Notice that Requests 4, 5, and 6 return **instantly (0.00s)**. Instead of hanging, the system immediately gives the user a friendly fallback message, keeping the application fast and stable.
 
<img width="1307" height="1021" alt="image" src="https://github.com/user-attachments/assets/651b54c7-9608-4f42-af3d-05c02f7bcd08" />
 
##  Distributed Systems Requirements

### Custom Middleware Header
As per the assignment requirements, a custom FastAPI middleware is implemented to ensure every response contains the student identifier:
- **Header:** `X-Student-ID`
- **Value:** `BSAI23037`

### CAP Theorem Trade-offs
In this implementation, we prioritize **Availability** and **Latency** over **Consistency**. By using a Circuit Breaker and providing a fallback, we ensure the system remains responsive even if the data (AI response) is temporarily unavailable or "stale" (using a cached/fallback message).

---
**Course:** Parallel and Distributed Computing (PDC)  
