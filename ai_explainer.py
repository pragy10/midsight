from dotenv import load_dotenv
import os
from google import genai

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

def explain_process(proc_row):
    prompt = f"""
You are a Linux security assistant. Here is information about a suspicious process:

PID: {proc_row[2]}
Process Name: {proc_row[4]}
User: {proc_row[7]}
Executable: {proc_row[5]}
Cmdline: {proc_row[6]}
Reason flagged: {proc_row[8]}

Please answer IN 5 LINES ONLY:
1. What is this process likely doing?
2. Is it likely to be malicious or suspicious? Why or why not?
3. Give a severity score from 1 (benign) to 10 (critical threat).
4. Explain your reasoning in simple terms for a non-technical user.

IF THE SEVERITY SCORE IS HIGH (>5), SUGGEST SOME SOLUTIONS TOO IN A FEW SENTENCES
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text


def explain_file_change(file_path, change_type, old_hash, new_hash):
    prompt = f"""
You are a Linux security assistant. The following file has changed:

File: {file_path}
Change type: {change_type}
Old hash: {old_hash}
New hash: {new_hash}

Please answer IN 5 LINES ONLY:
1. Why is this file important on a Linux system?
2. What are possible security implications of this change?
3. Give a severity score from 1 (benign) to 10 (critical threat).
4. Explain your reasoning in simple terms for a non-technical user.

IF THE SEVERITY SCORE IS HIGH (>5), SUGGEST SOME SOLUTIONS TOO IN A FEW SENTENCES
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text


def explain_network_event(event_type, details):
    prompt = f"""
You are a Linux security assistant. Here is information about a network event:

Event type: {event_type}
Details: {details}

Please answer IN 5 LINES ONLY:
1. What does this event mean?
2. Is it likely to be malicious or suspicious? Why or why not?
3. Give a severity score from 1 (benign) to 10 (critical threat).
4. Explain your reasoning in simple terms for a non-technical user.

IF THE SEVERITY SCORE IS HIGH (>5), SUGGEST SOME SOLUTIONS TOO IN A FEW SENTENCES
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text


def explain_geoip_event(event_type, ip, location, blacklist_status):
    prompt = f"""
You are a Linux security assistant. Here is information about a network event:

Event type: {event_type}
IP: {ip}
GeoIP location: {location}
Blacklist status: {blacklist_status}

Please answer IN 5 LINES ONLY:
1. Why might this event be interesting or suspicious?
2. What are possible security implications?
3. Give a severity score from 1 (benign) to 10 (critical threat).
4. Explain your reasoning in simple terms for a non-technical user.

IF THE SEVERITY SCORE IS HIGH (>5), SUGGEST SOME SOLUTIONS TOO IN A FEW SENTENCES
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

def explain_honeytoken_event(file_path, event_type):
    prompt = f"""
You are a Linux security assistant. A honeytoken file has triggered an event.

File: {file_path}
Event type: {event_type}

Please answer IN 5 LINES ONLY:
1. Why might this event be interesting or suspicious?
2. What are possible security implications?
3. Give a severity score from 1 (benign) to 10 (critical threat).
4. Explain your reasoning in simple terms for a non-technical user.

IF THE SEVERITY SCORE IS HIGH (>5), SUGGEST SOME SOLUTIONS TOO IN A FEW SENTENCES
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text
