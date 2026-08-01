# 🔍 FRP - find random ip

**FRP** is a high-performance asynchronous port scanner written in Python. It generates random IP addresses and scans them for open ports.  
Ideal for **network reconnaissance**, **security testing**, and **educational purposes**.

---

## 🚀 Features

- ⚡ **Asynchronous scanning** with `asyncio` and `ThreadPoolExecutor` for blazing-fast performance
- 🌍 **Country filtering** – limit scanning to specific countries (Iran, US, China, and more)
- 🖥️ **OS detection** – identify if the host is running Linux or Windows (via TTL)
- 📁 **Save results** to a file with a clean, formatted output
- 🎨 **Colorful terminal output** – easy to read and visually appealing
- 🛑 **Customizable concurrency** – adjust the number of concurrent connections with `-t`
- 📡 **Random IP generation** – scans real, valid IPv4 addresses

---

## 📦 Installation

### Clone the repository

```bash
git clone https://github.com/pin-toto/frp.git
cd frp
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🖥️ Usage

```bash
python frp.py -g <number_of_ips> -p <ports> [options]
```

### Required arguments

| Argument | Description |
|----------|-------------|
| `-g, --generate` | Number of random IPs to generate and scan |
| `-p, --ports`   | Comma-separated list of ports to check (e.g., `22,80,443`) |

### Optional arguments

| Argument | Description |
|----------|-------------|
| `-f, --filter-country` | Filter IPs by country (`iran`, `us`, `china`) |
| `-fs, --file-save`     | Save results to a file |
| `-o, --os-filter`      | Filter by OS (`win` or `linux`) |
| `-t, --threads`        | Number of concurrent connections (default: `500`) |

---

## 🧪 Examples

### Scan 1000 random IPs for SSH (port 22)

```bash
python frp.py -g 1000 -p 22
```

### Scan 5000 IPs from Iran for ports 22 and 80, and save results

```bash
python frp.py -g 5000 -p 22,80 -f iran -fs results.txt
```

### Scan 2000 IPs, filter by Linux OS, with 700 concurrent threads

```bash
python frp.py -g 2000 -p 22,443 -o linux -t 700
```

---

## 📁 Sample Output

```
==================================================
  FRP - Find Random Port Scanner v1.0
==================================================

Generating 1000 IPs...
Checking ports: 22, 80
Using 500 concurrent connections
Scanning...

Found: 192.168.1.1 - Port: 22 (linux)
Found: 10.0.0.5 - Ports: 22, 80 (linux)

Progress: 100.0% - Found: 2

==================================================
Scan complete! Time: 12.34s
Found 2 open ports.
==================================================
```

---

## ⚠️ Legal Disclaimer

> **This tool is for educational and authorized testing purposes only.**  
> Scanning networks without explicit permission is **illegal** in most jurisdictions.  
> The author assumes no responsibility for any misuse of this tool.

---

## 📜 License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for more details.

---

## 👤 Author

- **pintoto** – [GitHub](https://github.com/pin-toto)

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## ⭐ Support

If you find this tool useful, give it a ⭐ on GitHub and share it with your network!
```
