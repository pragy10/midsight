from dotenv import load_dotenv
import os
from google import genai

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

question = """Please answer IN 5 LINES ONLY:
1. What is this process likely doing?
2. Is it likely to be malicious or suspicious? Why or why not?
3. Explain your reasoning in simple terms for a non-technical user.
4. Give a severity score from 1 (benign) to 10 (critical threat). format is like -> Severity: fraction/10 


IF THE SEVERITY SCORE IS HIGH (>5), SUGGEST SOME SOLUTIONS TOO IN A FEW SENTENCES
USE EMOJIS AS GIVEN BELOW(like infront of each point you make), AND DONT USE BIGGER TEXT OR BOLD BECAUSE THIS IS ON A COMMANDLINE.

SO DONT USE ASTERISKS TO MAKE THE TEXT BIGGER. JUST NORMAL TEXT OK??

so the format of explaining those four questions be like
🔹 {explanation}
🔹 {explanation}
🔹 {explanation}
🔹 {explanation} 

DONT INCLUDE ANY NUMBERINGS!!!!

/use the below only if the risk is high, ie, >5/
🛡️ SOLUTION:
{describe solution here in next line}
 """

def explain_process(proc_row):
    prompt = f"""
You are a Linux security assistant. Here is information about a suspicious process:

PID: {proc_row[2]}
Process Name: {proc_row[4]}
User: {proc_row[7]}
Executable: {proc_row[5]}
Cmdline: {proc_row[6]}
Reason flagged: {proc_row[8]}

{question}
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

{question}
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

{question}
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

{question}
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

{question}
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text


def explain_overall_report(process_count, file_count, network_count, honeytoken_count):
    prompt = f"""
You are a Linux SOC assistant. Here is a summary of recent security findings:

- Suspicious processes: {process_count}
- File integrity alerts: {file_count}
- Network events: {network_count}
- Honeytoken triggers: {honeytoken_count}

Please provide:
1. A brief summary of the overall security situation.
2. Which areas are most concerning and why?
3. Suggestions for the user to improve their security posture.
4. Use simple, non-technical language.

USE EMOJIS, AND DONT USE BIGGER TEXT OR BOLD BECAUSE THIS IS ON A COMMANDLINE.
SO DONT USE ASTERISKS TO MAKE THE TEXT BIGGER. JUST NORMAL TEXT OK??
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text
