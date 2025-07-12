# 🛡️ MIDSight

**A Modern, Modular Linux Security CLI Tool Powered by AI**  
_Created by Pragya Sekar_


## 🔍 What is MIDSight?

MIDSight is a command-line tool built for **monitoring Linux systems**. It helps detect suspicious processes, changes to important files, network anomalies, unauthorized access to decoy files (honeytokens), and more — with powerful **AI explanations** using **Google Gemini**.

Whether you're a security enthusiast, sysadmin, or just curious — MIDSight gives you insight with clarity.


## 🚀 Getting Started

### ✅ Requirements

Before installing, make sure you have:

- **Python 3.9 or higher**
- A **Linux system** (tested on Ubuntu/Debian)
- An **Internet connection** (for AI and threat intelligence features)
- **Git** (recommended)


### 🧰 Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/midsight.git
cd midsight
````

#### 2. Set Up Your Environment

We recommend using a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 3. Configure Gemini API

MIDSight uses **Google Gemini** to provide AI-powered summaries and insights.

##### Option 1: Use the Interactive Menu

```bash
python main.py
```

* Select **"Configuration"** from the menu.
* Paste your Gemini API key when prompted.
* A `.env` file will be created for you.

##### Option 2: Add API Key Manually

Create a `.env` file in the root directory:

```
GEMINI_API_KEY=your-gemini-api-key-here
```

> ⚠️ **Do not share or commit your `.env` file**. It contains your private API key.

---

## 🏁 Running MIDSight

Start the tool:

```bash
python main.py
```

You'll see an interactive menu:

```
=== MIDSight Security CLI ===
  1. Monitor Processes
  2. File Integrity Checker
  3. Network Monitor
  4. GeoIP & Threat Intel Enricher
  5. Honeytokens / Canary Files
  6. Generate Security Report
  7. Configuration
  8. Exit
```

* Just choose an option (e.g., 1 for Process Monitoring) and follow the prompts.
* Set up your Gemini API key first to enable AI insights.

---

## ⚠️ Important Notes

* **Run as a regular user** unless you need access to protected files or processes.
* **Back up important files** before using integrity or honeytoken features.
* Review monitored file paths in:

  * `file_integrity.py` → for file checks
  * `honeytoken.py` → for decoy files
* Check `.env` to make sure your Gemini key is valid and present.

---

## 🧠 Features at a Glance

* 🧾 **Process Monitoring** – Spot suspicious or abnormal system activity
* 🗃️ **File Integrity Checker** – Detect unexpected changes to key files
* 🌐 **Network Monitor** – Watch for unusual ports or external connections
* 🌍 **GeoIP & Threat Intelligence** – Add location and reputation to network events
* 🪤 **Honeytokens** – Detect tampering with decoy files
* 📊 **Security Report** – Summarized output with Gemini AI explanations
* ⚙️ **Config Menu** – Easily manage your Gemini API key

---

## 🛠️ Troubleshooting

* **Missing Gemini key?** Make sure your `.env` file exists and is correctly formatted.
* **No suspicious output?** That’s a good thing! The modules report only when something unusual is found.
* **Dependencies outdated?** Keep them fresh with:

  ```bash
  pip install --upgrade -r requirements.txt
  ```

---

## 📁 Project Structure

| File/Folder          | Purpose                           |
| -------------------- | --------------------------------- |
| `main.py`            | Entry point for the CLI           |
| `db.py`              | Handles internal data persistence |
| `process_monitor.py` | Monitors running processes        |
| `file_integrity.py`  | Detects unauthorized file changes |
| `network_monitor.py` | Tracks open ports and traffic     |
| `geoip_enricher.py`  | Adds GeoIP and reputation data    |
| `honeytoken.py`      | Monitors decoy files for access   |
| `report.py`          | Compiles a detailed report        |
| `ai_explainer.py`    | Handles Gemini LLM integration    |
| `requirements.txt`   | Dependency list                   |
| `.env`               | Your private Gemini API key       |
| `README.md`          | This file you're reading :)       |

---

## 🔐 Security & Ethics

* MIDSight is built for **learning, research, and defensive purposes**.
* **Always audit code** and behavior before using it in sensitive or production environments.

---

## 🙌 Acknowledgments

Made with 💻 and ☕ by **Pragya Sekar**


## 📬 Questions or Suggestions?

Open an [issue](https://github.com/yourusername/midsight/issues) or submit a pull request to contribute or report bugs.

```

