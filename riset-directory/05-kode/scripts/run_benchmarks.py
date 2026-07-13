import os
import sys
import time
import subprocess
import urllib.request
import re
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE_DIR / "results"
SCRIPTS_DIR = BASE_DIR / "scripts"

# Define the exact interleave sequence of 10 runs
RUNS = [
    {"run": 1, "framework": "springboot", "service": "springboot-api", "target": "http://springboot-api:8080", "filename": "sb-run-001.csv", "health_url": "http://localhost:8080/actuator/health"},
    {"run": 2, "framework": "dotnet", "service": "dotnet-api", "target": "http://dotnet-api:5000", "filename": "dn-run-001.csv", "health_url": "http://localhost:5000/health"},
    {"run": 3, "framework": "dotnet", "service": "dotnet-api", "target": "http://dotnet-api:5000", "filename": "dn-run-002.csv", "health_url": "http://localhost:5000/health"},
    {"run": 4, "framework": "springboot", "service": "springboot-api", "target": "http://springboot-api:8080", "filename": "sb-run-002.csv", "health_url": "http://localhost:8080/actuator/health"},
    {"run": 5, "framework": "springboot", "service": "springboot-api", "target": "http://springboot-api:8080", "filename": "sb-run-003.csv", "health_url": "http://localhost:8080/actuator/health"},
    {"run": 6, "framework": "dotnet", "service": "dotnet-api", "target": "http://dotnet-api:5000", "filename": "dn-run-003.csv", "health_url": "http://localhost:5000/health"},
    {"run": 7, "framework": "dotnet", "service": "dotnet-api", "target": "http://dotnet-api:5000", "filename": "dn-run-004.csv", "health_url": "http://localhost:5000/health"},
    {"run": 8, "framework": "springboot", "service": "springboot-api", "target": "http://springboot-api:8080", "filename": "sb-run-004.csv", "health_url": "http://localhost:8080/actuator/health"},
    {"run": 9, "framework": "springboot", "service": "springboot-api", "target": "http://springboot-api:8080", "filename": "sb-run-005.csv", "health_url": "http://localhost:8080/actuator/health"},
    {"run": 10, "framework": "dotnet", "service": "dotnet-api", "target": "http://dotnet-api:5000", "filename": "dn-run-005.csv", "health_url": "http://localhost:5000/health"},
]

def run_cmd(cmd, **kwargs):
    """Wrapper to run subprocess commands ensuring they run in the BASE_DIR."""
    if 'cwd' not in kwargs:
        kwargs['cwd'] = str(BASE_DIR)
    return subprocess.run(cmd, **kwargs)

def check_mongodb_count():
    try:
        # Check running MongoDB
        res = run_cmd([
            "docker", "compose", "exec", "mongodb", "mongosh", "benchmark_db", 
            "--eval", "db.ikea_products.countDocuments()"
        ], capture_output=True, text=True, check=False)
        output = res.stdout.strip()
        digits = "".join(re.findall(r'\d+', output))
        if digits:
            return int(digits)
    except Exception as e:
        print(f"Error checking MongoDB document count: {e}")
    return 0

def stop_all_apis():
    print("Stopping any running API containers...")
    run_cmd(["docker", "compose", "--profile", "springboot", "down"], check=False)
    run_cmd(["docker", "compose", "--profile", "dotnet", "down"], check=False)

def wait_for_healthy(service, health_url, timeout=90):
    print(f"Waiting for {service} to become healthy at {health_url}...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        # 1. Check HTTP healthcheck endpoint
        try:
            req = urllib.request.Request(health_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=2) as resp:
                if resp.getcode() == 200:
                    body = resp.read().decode('utf-8')
                    if "UP" in body or "healthy" in body or '"status"' in body or "status" in body:
                        print(f"-> {service} is healthy! (via HTTP check)")
                        return True
        except Exception:
            pass
        
        # 2. Check docker compose ps for healthy status (fallback)
        try:
            res = run_cmd([
                "docker", "compose", "ps", service
            ], capture_output=True, text=True, check=False)
            if "healthy" in res.stdout.lower():
                print(f"-> {service} is healthy! (via docker compose check)")
                return True
        except Exception:
            pass
        
        time.sleep(3)
    return False

def main():
    print("==================================================")
    print("      AUTOMATED BENCHMARK RUNNER SCRIPT          ")
    print("==================================================")

    # 1. Ensure results folder exists
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # 2. Start MongoDB
    print("\n[Step 1] Ensuring MongoDB is running and healthy...")
    run_cmd(["docker", "compose", "up", "-d", "mongodb"], check=True)
    
    # Wait for MongoDB to be healthy
    mongo_healthy = False
    start_time = time.time()
    while time.time() - start_time < 60:
        res = run_cmd(["docker", "compose", "ps", "mongodb"], capture_output=True, text=True, check=False)
        if "healthy" in res.stdout.lower():
            mongo_healthy = True
            break
        time.sleep(2)
    
    if not mongo_healthy:
        print("[ERROR] MongoDB is not healthy. Exiting.")
        sys.exit(1)
    print("MongoDB is healthy.")

    # Check and import document if needed
    count = check_mongodb_count()
    print(f"MongoDB documents count: {count}")
    if count != 401046:
        print("Dataset is incomplete or not imported. Running data importer...")
        run_cmd(["docker", "compose", "--profile", "import", "up", "data-importer"], check=True)
        # Verify again
        count = check_mongodb_count()
        print(f"Verified MongoDB documents count after import: {count}")
        if count != 401046:
            print("[WARNING] Document count is still not 401046. Proceeding anyway...")

    # 3. Clean up before starting
    stop_all_apis()

    # 4. Run benchmarks
    total_runs = len(RUNS)
    print(f"\n[Step 2] Starting {total_runs} benchmark runs sequentially...")
    
    for idx, run in enumerate(RUNS):
        run_num = run["run"]
        framework = run["framework"]
        service = run["service"]
        target = run["target"]
        filename = run["filename"]
        health_url = run["health_url"]
        
        print("\n--------------------------------------------------")
        print(f"Run {run_num}/{total_runs}: Starting {framework.upper()} API...")
        print("--------------------------------------------------")
        
        # Start API
        run_cmd(["docker", "compose", "--profile", framework, "up", "-d", service], check=True)
        
        # Wait for API to become healthy
        if not wait_for_healthy(service, health_url):
            print(f"[ERROR] API {service} failed to become healthy. Stopping execution.")
            sys.exit(1)
            
        # Extra sleep for stabilization
        time.sleep(2)
        
        # Run k6
        print(f"Running k6 load test. Saving output to results/{filename}...")
        k6_cmd = [
            "docker", "compose", "--profile", "k6", "run", "--rm", "k6", "run",
            "/scripts/load-test.js", "-e", f"TARGET={target}", f"--out=csv=/results/{filename}"
        ]
        k6_res = run_cmd(k6_cmd, check=False)
        if k6_res.returncode != 0:
            print(f"[WARNING] k6 run exited with code {k6_res.returncode}")
            
        # Down the API
        print(f"Stopping {framework.upper()} API...")
        run_cmd(["docker", "compose", "--profile", framework, "down"], check=True)
        
        # Cooldown period (5 seconds) to release resources
        print("Cooldown period of 5 seconds...")
        time.sleep(5)

    print("\n--------------------------------------------------")
    print("[Step 3] All benchmark runs completed successfully!")
    print("--------------------------------------------------")

    # 5. Extract metrics using extract_metrics.py
    print("\n[Step 4] Extracting metrics to results/all_runs.csv...")
    try:
        import numpy
        print("numpy is installed on host. Running metrics extraction locally...")
        extract_cmd = [sys.executable, str(SCRIPTS_DIR / "extract_metrics.py"), "--input", str(RESULTS_DIR), "--output", str(RESULTS_DIR / "all_runs.csv")]
        run_cmd(extract_cmd, check=True)
    except ImportError:
        print("numpy not found on host. Running metrics extraction via Docker...")
        results_host = str(RESULTS_DIR.resolve())
        scripts_host = str(SCRIPTS_DIR.resolve())
        
        docker_cmd = [
            "docker", "run", "--rm",
            "-v", f"{results_host}:/results",
            "-v", f"{scripts_host}:/scripts",
            "python:3.12-alpine",
            "sh", "-c", "pip install numpy --quiet && python /scripts/extract_metrics.py --input /results --output /results/all_runs.csv"
        ]
        run_cmd(docker_cmd, check=True)

    # 6. Run Statistical Analysis
    print("\n[Step 5] Performing statistical analysis...")
    try:
        import pandas
        import scipy
        print("pandas and scipy are installed on host. Running analysis locally...")
        analyze_cmd = [sys.executable, str(SCRIPTS_DIR / "analyze_results.py")]
        # Needs to be run from the repository root to find results/all_runs.csv
        run_cmd(analyze_cmd, cwd=str(BASE_DIR), check=True)
    except ImportError:
        print("pandas/scipy not found on host. Running analysis via Docker...")
        
        # Map base directory to /workspace and set it as working directory.
        base_host = str(BASE_DIR.resolve())
        docker_cmd = [
            "docker", "run", "--rm",
            "-v", f"{base_host}:/workspace",
            "-w", "/workspace",
            "python:3.12-slim",
            "sh", "-c", "pip install pandas scipy --quiet && python scripts/analyze_results.py"
        ]
        run_cmd(docker_cmd, check=True)

    print("\n==================================================")
    print("      BENCHMARKS COMPLETE & ANALYSIS DONE         ")
    print("==================================================")

if __name__ == "__main__":
    main()
