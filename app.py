from flask import Flask
from collections import Counter

app = Flask(__name__)

LOG_FILE = "alerts.log"


@app.route("/")
def home():
    try:
        with open(LOG_FILE, "r") as f:
            logs = f.readlines()
    except:
        logs = ["No alerts yet"]

    # Count alerts per IP
    ip_list = []
    for log in logs:
        parts = log.strip().split()
        if len(parts) > 5:
            ip_list.append(parts[-1])

    ip_count = Counter(ip_list)

    html = """
    <html>
    <head>
        <title>NIDS Dashboard</title>
        <style>
            body {
                font-family: Arial;
                background-color: #0f172a;
                color: white;
                padding: 20px;
            }
            h1 {
                color: #22c55e;
            }
            .alert {
                background-color: #1e293b;
                padding: 10px;
                margin: 10px 0;
                border-left: 5px solid red;
            }
            .card {
                background-color: #1e293b;
                padding: 15px;
                margin: 10px 0;
                border-radius: 8px;
            }
        </style>
    </head>
    <body>
        <h1>🚨 Network Intrusion Detection System</h1>
        <h3>Total Alerts: """ + str(len(logs)) + """</h3>

        <div class="card">
            <h3>📊 Alerts per IP</h3>
    """

    for ip, count in ip_count.items():
        html += f"<p>{ip} : {count} alerts</p>"

    html += "</div><h3>Recent Alerts</h3>"

    for log in reversed(logs):
        html += f"<div class='alert'>{log}</div>"

    html += "</body></html>"

    return html


if __name__ == "__main__":
    app.run(debug=True)