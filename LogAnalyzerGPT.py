import os
import re
import subprocess
from openai import OpenAI

client = OpenAI()

# Function to gather logs from specified files
def gather_logs():
    logs = []
    # Target log files
    log_files = [
        "/var/log/syslog",
        "/var/log/messages",
        "/var/log/dmesg",
        "/var/log/auth.log",
        "/var/log/kern.log",
        "/var/log/cron",
        "/var/log/secure"
    ]
    
    for log_file in log_files:
        if os.path.exists(log_file):
            try:
                # Read only the last 500 lines to reduce size
                with open(log_file, "r") as file:
                    logs.append(f"=== {log_file} ===\n" + "".join(file.readlines()[-500:]))
            except PermissionError:
                print(f"Permission denied: {log_file}")
    
    return "\n".join(logs)

# Function to collect dmesg logs
def collect_dmesg_logs():
    try:
        # Collect the last 500 lines of dmesg logs
        dmesg_output = subprocess.check_output(["dmesg", "-T"], text=True)
        dmesg_lines = dmesg_output.split("\n")[-500:]
        return "=== dmesg Logs ===\n" + "\n".join(dmesg_lines)
    except Exception as e:
        print(f"Error collecting dmesg logs: {e}")
        return ""

def collect_boot_logs():
    try:
        boot_logs = subprocess.check_output(["sudo", "journalctl", "-b"], text=True)
        boot_lines = boot_logs.split("\n")[-500:]  # 最後の500行のみ取得
        return "=== Boot Logs ===\n" + "\n".join(boot_lines)
    except Exception as e:
        print(f"Error collecting boot logs: {e}")
        return ""

# Function to filter for errors and warnings
def filter_logs(log_data, context=2):
    """Filter logs containing error keywords and include surrounding context."""

    filtered_blocks = []
    error_keywords = [
        "error",
        "failed",
        "critical",
        "panic",
        "warn",
        "denied",
        "unauthorized",
        "ERROR",
        "Error",
        "CRITICAL",
        "PANIC",
        "WARN",
        "エラー",
    ]

    log_lines = log_data.split("\n")
    total_lines = len(log_lines)

    for idx, line in enumerate(log_lines):
        lowered = line.lower()
        if any(keyword in lowered for keyword in error_keywords):
            start = max(0, idx - context)
            end = min(total_lines, idx + context + 1)
            block = "\n".join(log_lines[start:end])
            filtered_blocks.append(block)

    unique_blocks = []
    seen = set()
    for block in filtered_blocks:
        if block not in seen:
            seen.add(block)
            unique_blocks.append(block)

    return "\n\n".join(unique_blocks)

# Function to send logs to OpenAI for summarization
def summarize_logs(log_summary):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a system analyst specializing in Linux system logs."},
            {"role": "user", "content": f"Summarize the following system logs for errors, suspicious activities, and potential future issues, and answer in Japanese, and mention the log file name to pay attention:\n\n{log_summary}"}
        ],
    )
    return response.choices[0].message.content.strip()

# Function to save summary to a file
def save_summary_to_file(summary, file_path="log_summary.txt"):
    try:
        with open(file_path, "w") as file:
            file.write(summary)
        print(f"Summary saved to {file_path}")
    except IOError as e:
        print(f"Error saving summary to file: {e}")

# Main function
def main():
    print("Gathering logs...")
    log_data = gather_logs()
    
    print("Collecting dmesg logs...")
    dmesg_logs = collect_dmesg_logs()

    print("Collecting boot logs...")
    boot_logs = collect_boot_logs()
    
    combined_logs = log_data + "\n\n" + dmesg_logs + "\n\n" + boot_logs
    print("Filtering logs for errors and warnings...")
    filtered_log_data = filter_logs(combined_logs)
    
    if filtered_log_data.strip():
        print("Sending logs to OpenAI for summarization...")
        summary = summarize_logs(filtered_log_data[:3000])  # Limit to 3000 characters for API
        print("\nSummary from OpenAI:\n")
        print(summary)
        save_summary_to_file(summary)
    else:
        print("No significant errors or warnings found in logs.")

if __name__ == "__main__":
    main()
