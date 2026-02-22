from http.server import BaseHTTPRequestHandler
import json
import numpy as np

DATA = [
  {"region":"apac","service":"analytics","latency_ms":201.8,"uptime_pct":98.502,"timestamp":20250301},
  {"region":"apac","service":"checkout","latency_ms":227.09,"uptime_pct":98.356,"timestamp":20250302},
  {"region":"apac","service":"recommendations","latency_ms":190.27,"uptime_pct":99.18,"timestamp":20250303},
  {"region":"apac","service":"analytics","latency_ms":155.61,"uptime_pct":98.72,"timestamp":20250304},
  {"region":"apac","service":"checkout","latency_ms":160.6,"uptime_pct":97.848,"timestamp":20250305},
  {"region":"apac","service":"analytics","latency_ms":156.53,"uptime_pct":99.104,"timestamp":20250306},
  {"region":"apac","service":"catalog","latency_ms":115.45,"uptime_pct":98.248,"timestamp":20250307},
  {"region":"apac","service":"recommendations","latency_ms":163.48,"uptime_pct":97.458,"timestamp":20250308},
  {"region":"apac","service":"analytics","latency_ms":146.67,"uptime_pct":98.051,"timestamp":20250309},
  {"region":"apac","service":"checkout","latency_ms":176.94,"uptime_pct":99.278,"timestamp":20250310},
  {"region":"apac","service":"recommendations","latency_ms":125.18,"uptime_pct":98.541,"timestamp":20250311},
  {"region":"apac","service":"payments","latency_ms":173.95,"uptime_pct":99.065,"timestamp":20250312},
  {"region":"emea","service":"support","latency_ms":204.35,"uptime_pct":97.98,"timestamp":20250301},
  {"region":"emea","service":"analytics","latency_ms":210.95,"uptime_pct":98.114,"timestamp":20250302},
  {"region":"emea","service":"support","latency_ms":203,"uptime_pct":97.817,"timestamp":20250303},
  {"region":"emea","service":"payments","latency_ms":139.94,"uptime_pct":98.304,"timestamp":20250304},
  {"region":"emea","service":"recommendations","latency_ms":198.05,"uptime_pct":98.221,"timestamp":20250305},
  {"region":"emea","service":"recommendations","latency_ms":168.47,"uptime_pct":98.922,"timestamp":20250306},
  {"region":"emea","service":"checkout","latency_ms":175.54,"uptime_pct":99.007,"timestamp":20250307},
  {"region":"emea","service":"catalog","latency_ms":230.19,"uptime_pct":98.476,"timestamp":20250308},
  {"region":"emea","service":"support","latency_ms":138.84,"uptime_pct":98.008,"timestamp":20250309},
  {"region":"emea","service":"analytics","latency_ms":115.82,"uptime_pct":99.179,"timestamp":20250310},
  {"region":"emea","service":"payments","latency_ms":152.42,"uptime_pct":97.711,"timestamp":20250311},
  {"region":"emea","service":"catalog","latency_ms":181.53,"uptime_pct":97.583,"timestamp":20250312},
  {"region":"amer","service":"recommendations","latency_ms":157.16,"uptime_pct":99.245,"timestamp":20250301},
  {"region":"amer","service":"recommendations","latency_ms":187.47,"uptime_pct":98.968,"timestamp":20250302},
  {"region":"amer","service":"catalog","latency_ms":207.96,"uptime_pct":99.304,"timestamp":20250303},
  {"region":"amer","service":"analytics","latency_ms":102.59,"uptime_pct":97.381,"timestamp":20250304},
  {"region":"amer","service":"support","latency_ms":127.83,"uptime_pct":98.23,"timestamp":20250305},
  {"region":"amer","service":"recommendations","latency_ms":188.84,"uptime_pct":98.149,"timestamp":20250306},
  {"region":"amer","service":"analytics","latency_ms":215.61,"uptime_pct":97.27,"timestamp":20250307},
  {"region":"amer","service":"support","latency_ms":117.33,"uptime_pct":98.814,"timestamp":20250308},
  {"region":"amer","service":"recommendations","latency_ms":192.27,"uptime_pct":97.196,"timestamp":20250309},
  {"region":"amer","service":"analytics","latency_ms":205.81,"uptime_pct":99.237,"timestamp":20250310},
  {"region":"amer","service":"catalog","latency_ms":138.96,"uptime_pct":97.758,"timestamp":20250311},
  {"region":"amer","service":"catalog","latency_ms":150.95,"uptime_pct":97.433,"timestamp":20250312},
]

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(length))
        regions = body.get("regions", [])
        threshold = body.get("threshold_ms", 180)

        result = {}
        for region in regions:
            records = [d for d in DATA if d["region"] == region]
            if not records:
                result[region] = None
                continue
            latencies = [r["latency_ms"] for r in records]
            uptimes = [r["uptime_pct"] for r in records]
            result[region] = {
                "avg_latency": round(float(np.mean(latencies)), 4),
                "p95_latency": round(float(np.percentile(latencies, 95)), 4),
                "avg_uptime": round(float(np.mean(uptimes)), 4),
                "breaches": int(sum(1 for l in latencies if l > threshold))
            }

        self.send_response(200)
        self._send_cors_headers()
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())

    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
