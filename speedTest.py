import subprocess
import re


total_time = 0
ping_count = 0
highping_count = 0
failures = 0

print("\033[0m", "Starting ping test")

try:
    while True:
        result = subprocess.run(['ping', '8.8.8.8', '-n', '1'], capture_output=True, text=True)
        if result.stdout[42] == 'p':
            for line in result.stdout.splitlines():
                match = re.search(r'time[=<]?(\d+\.?\d*)\s*ms', line)
                indent = ""
                visualize = ""
                if match:
                    for i in range(4 - len(match.group(1))):
                        indent += " "
                    for i in range(int(float(match.group(1)))):
                        visualize += " "
                    total_time += float(match.group(1))
                    ping_count += 1
                    if float(match.group(1)) < 100:
                        print("\033[32m", f"{match.group(1)}ms {indent}", "\033[42m", f"{visualize}", "\033[0m")
                    elif float(match.group(1)) < 250:
                        print("\033[33m", f"{match.group(1)}ms {indent}", "\033[43m", f"{visualize}", "\033[0m")
                        highping_count += 1
                    else: 
                        print("\033[31m", f"{match.group(1)}ms {indent}", "\033[41m", f"{visualize}", "\033[0m")
                        highping_count += 1

        else:
            print("\033[41m", "Failure")
            failures += 1
except KeyboardInterrupt:
    print("\033[0m", "")
    print("Ping test stopped.")
    average = total_time / ping_count
    highpingPercent = (highping_count / ping_count * 100)
    failurePercent = (failures / ping_count * 100)
    print(f"Total pings: {ping_count}")
    print(f"Average ping: {average} ms")
    print(f"High pings (>100ms): {highping_count}")
    print(f"High ping percentage: {highpingPercent}%")
    print(f"Failures: {failures}")
    print(f"Failure percentage: {failurePercent}%")
