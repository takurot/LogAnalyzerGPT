import os
import re
import subprocess
from openai import OpenAI

client = OpenAI()

# Function to gather logs
def gather_logs():
    logs = []
    log_files = ["/var/log/syslog", "/var/log/messages", "/var/log/dmesg", "/var/log/auth.log"]
    
    for log_file in log_files:
        if os.path.exists(log_file):
            try:
                with open(log_file, "r") as file:
                    logs.append(file.read())
            except PermissionError:
                print(f"Permission denied: {log_file}")
    
    return "\n".join(logs)

# Function to filter for errors and warnings
def filter_logs(log_data):
    filtered_logs = []
    error_keywords = ["error", "failed", "critical", "panic", "warn", "denied", "unauthorized"]
    log_lines = log_data.split("\n")
    
    for line in log_lines:
        if any(keyword in line.lower() for keyword in error_keywords):
            filtered_logs.append(line)
    
    return "\n".join(filtered_logs)

# Function to send logs to OpenAI for summarization
def summarize_logs(log_summary):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a system analyst specializing in Linux system logs."},
            {"role": "user", "content": f"Summarize the following system logs for errors, suspicious activities, and potential future issues, and answer in Japanese:\n\n{log_summary}"}
        ],
    )
    return response.choices[0].message.content.strip()

# Function to save summary to a file
def save_summary_to_file(summary, file_path="log_summary.md"):
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
    print("Filtering logs for errors and warnings...")
    filtered_log_data = filter_logs(log_data)
    
    if filtered_log_data.strip():
        print("Sending logs to OpenAI for summarization...")
        summary = summarize_logs(filtered_log_data)
        print("\nSummary from OpenAI:\n")
        print(summary)
        save_summary_to_file(summary)
    else:
        print("No significant errors or warnings found in logs.")

if __name__ == "__main__":
    main()
