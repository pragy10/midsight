```markdown
# MIDSight

**A Modern Modular Linux Security CLI powered by AI**  
_by Pragya Sekar_

---

## 🛡️ Overview

MIDSight is a modular command-line security tool for Linux systems. It monitors processes, file integrity, network activity, honeytokens, and more—enriching findings with AI-powered explanations using Google Gemini.

---

## 🚀 Quick Start

### 1. Prerequisites

- **Python 3.9+** installed on your system.
- **Linux OS** (tested on Ubuntu/Debian).
- **Internet connection** (for Gemini LLM analysis and threat intelligence enrichment).
- **Git** (recommended for cloning/updating the repo).

### 2. Clone the Repository

```
git clone https://github.com/yourusername/midsight.git
cd midsight
```

### 3. Install Dependencies

It is recommended to use a virtual environment:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Configure the Gemini API Key

MIDSight uses the Google Gemini LLM for explanations and summaries.  
**You must set up your `.env` file with your Gemini API key before using the AI features.**

#### a. Get Your Gemini API Key

- Go to [Google AI Studio](https://aistudio.google.com).
- Create or copy your Gemini API key.

#### b. Add the Key to `.env`

You can use the built-in configuration menu:

```
python main.py
```
- Select the "Configuration" option from the menu.
- Enter your Gemini API key when prompted.
- The key will be saved in a `.env` file in your project directory.

Or, manually create a `.env` file in the project root:

```
GEMINI_API_KEY=your-gemini-api-key-here
```

> **Never share or commit your `.env` file to a public repository.**

---

## 🏁 How to Run MIDSight

From your project directory:

```
python main.py
```

You will see an interactive menu:

```
  === Midsight Security CLI ===
   Monitor Processes
   File Integrity Checker
   Network Monitor
   GeoIP & Threat Intel Enricher
   Honeytokens / Canary Files
   Generate Security Report
   Configuration
   Exit
```

- **Type the number** for the module you wish to run and follow the prompts.
- For the first run, set up the configuration (Gemini API key) before using AI-powered features.

---

## ⚠️ Before You Use

- **Run as a regular user** (not root) unless you need to monitor protected files or processes.
- **Back up important files** before using file integrity or honeytoken modules.
- **Review monitored file paths** in `file_integrity.py` and honeytoken paths in `honeytoken.py` to ensure they fit your system.
- **Check your `.env`** for the correct Gemini API key.
- **Do not share your `.env` file** or API key with anyone.

---

## 📝 Features

- **Process Monitoring:** Detects suspicious or anomalous processes.
- **File Integrity Checker:** Monitors critical files for unauthorized changes.
- **Network Monitor:** Flags suspicious open ports and outbound connections.
- **GeoIP & Threat Intel:** Enriches network events with location and reputation data.
- **Honeytokens:** Detects access/modification to decoy files.
- **Security Report:** Summarizes all findings with LLM-powered insights.
- **Configuration Menu:** Easily set or update your Gemini API key.

---

## 💡 Troubleshooting

- If you see errors about missing API keys, make sure your `.env` file exists and contains `GEMINI_API_KEY`.
- If a module shows no output, it means no suspicious activity was detected for that check.
- For best results, keep your dependencies up to date:
  ```
  pip install --upgrade -r requirements.txt
  ```

---

## 📂 Project Structure

| File/Folder         | Purpose                                 |
|---------------------|-----------------------------------------|
| `main.py`           | Main CLI entry point                    |
| `db.py`             | Database management                     |
| `process_monitor.py`| Process monitoring module               |
| `file_integrity.py` | File integrity checker                  |
| `network_monitor.py`| Network activity monitor                |
| `geoip_enricher.py` | GeoIP and threat intelligence enrichment|
| `honeytoken.py`     | Honeytoken/canary file monitoring       |
| `report.py`         | Security report generator               |
| `ai_explainer.py`   | LLM integration for explanations        |
| `requirements.txt`  | Python dependencies                     |
| `.env`              | Stores your Gemini API key              |
| `README.md`         | This documentation                      |

---

## 🛡️ Security Note

- MIDSight is for educational and research use.  
- Always review code and configuration before deploying in production environments.

---

## 🙏 Credits

Developed by **Pragya Sekar**  
"Security is not a product, but a process."

---

## 📧 Feedback & Issues

Open an issue or pull request on GitHub to contribute or report bugs.
```