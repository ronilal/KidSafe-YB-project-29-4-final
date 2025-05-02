import psutil
import os
import time

def close_app(appName):
    # Check for Discord processes
    for process in psutil.process_iter(['pid', 'name']):
        try:
            if appName in process.info['name'] or appName.lower() in process.info['name']:
                print(f"Closing {process.info['name']} (PID: {process.info['pid']})")
                os.kill(process.info['pid'], 9)  # Terminate the process
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

def main():
    print("Monitoring for app...")
    while True:
        close_app('Teams')
        time.sleep(5)  # Check every 5 seconds

if __name__ == "__main__":
    main()
