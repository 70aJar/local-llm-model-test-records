#!/usr/bin/env python3
"""MiniCPM5 tool-calling checker (XML protocol).

MiniCPM5-1B/2B emit XML-style tool calls, NOT OpenAI JSON tool_calls:
    <function name="add"><param name="a">37</param><param name="b">15</param></function>

The chat template (chat_template.jinja) hardwires this: "When calling a function,
return an XML object within <function ... </function>".  Mainstream OpenAI-compatible
servers (oMLX, LM Studio) have NO `minicpm5` XML->JSON parser (the parser only lands
in SGLang with --tool-call-parser minicpm5), so a generic harness that greps for JSON
`tool_calls` reports "NO TOOL CALL" even though the model answered correctly.

This script tests MiniCPM5 the way it actually works:
  1. sends a standard OpenAI-style `tools:` request,
  2. captures the RAW assistant content,
  3. parses XML <function>/<param> into a canonical call record,
  4. scores whether the emitted call matches the expected one (by name + params).

Usage:
  LM_API=http://127.0.0.1:8002/v1/chat/completions \
  LM_API_KEY=... MODEL=MiniCPM5-2B \
  python3 benchmarks/minicpm5_toolcheck.py "<label>"

Env: LM_API (required), LM_API_KEY (optional), MODEL (default from --model),
     TEMP (default 0.0).
"""
import json
import os
import re
import sys
import time
import urllib.request

API = os.environ.get("LM_API", "http://127.0.0.1:8002/v1/chat/completions")
KEY = os.environ.get("LM_API_KEY", "")
MODEL = os.environ.get("MODEL", "MiniCPM5-2B")
TEMP = float(os.environ.get("TEMP", "0.0"))
LABEL = sys.argv[1] if len(sys.argv) > 1 else "minicpm5-toolcheck"

TOOLS = {
    "add": {
        "name": "add",
        "description": "Add two integers.",
        "parameters": {"type": "object", "properties": {"a": {"type": "integer"}, "b": {"type": "integer"}}, "required": ["a", "b"]},
    },
    "get_weather": {
        "name": "get_weather",
        "description": "Get current weather for a city.",
        "parameters": {"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]},
    },
    "convert_currency": {
        "name": "convert_currency",
        "description": "Convert an amount between currencies.",
        "parameters": {"type": "object", "properties": {"amount": {"type": "number"}, "from": {"type": "string"}, "to": {"type": "string"}}, "required": ["amount", "from", "to"]},
    },
    "book_room": {
        "name": "book_room",
        "description": "Book a meeting room.",
        "parameters": {"type": "object", "properties": {"room": {"type": "string"}, "date": {"type": "string"}}, "required": ["room", "date"]},
    },
    "lookup_employee": {
        "name": "lookup_employee",
        "description": "Look up an employee by name.",
        "parameters": {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]},
    },
}

# (name, prompt, expected-call-check)
SCENARIOS = [
    ("add-37-15",
     "Use the add tool to compute 37 + 15.",
     {"name": "add", "params": {"a": "37", "b": "15"}}),
    ("weather-lahore",
     "What is the weather in Lahore?",
     {"name": "get_weather", "params": {"city": "Lahore"}}),
    ("convert-100-usd-eur",
     "Convert 100 USD to EUR.",
     {"name": "convert_currency", "params": {"amount": "100"}}),
    ("book-room-b-0512",
     "Book Room B for May 12.",
     {"name": "book_room", "params": {"room": "Room B"}}),
    ("lookup-jane",
     "Look up employee Jane Smith.",
     {"name": "lookup_employee", "params": {"name": "Jane Smith"}}),
]


def chat(messages, tools=None, max_tokens=2000):
    payload = {"model": MODEL, "messages": messages, "max_tokens": max_tokens, "temperature": TEMP}
    if tools:
        payload["tools"] = [{"type": "function", "function": t} for t in tools]
    headers = {"Content-Type": "application/json"}
    if KEY:
        headers["Authorization"] = f"Bearer {KEY}"
    req = urllib.request.Request(API, data=json.dumps(payload).encode(), headers=headers)
    t0 = time.time()
    d = json.loads(urllib.request.urlopen(req, timeout=300).read())
    msg = d["choices"][0]["message"]
    return msg, time.time() - t0


XML_RE = re.compile(r'<function name="([^"]+)">(.*?)</function>', re.S)
PARAM_RE = re.compile(r'<param name="([^"]+)">(.*?)</param>', re.S)
CDATA_RE = re.compile(r'<!\[CDATA\[(.*?)\]\]>', re.S)


def parse_xml_calls(content: str):
    """Parse MiniCPM5 XML tool calls into [{name, params:{}}, ...]. Safe/lenient."""
    calls = []
    for m in XML_RE.finditer(content or ""):
        name, body = m.group(1), m.group(2)
        params = {}
        for p in PARAM_RE.finditer(body):
            val = p.group(2).strip()
            cm = CDATA_RE.search(val)
            if cm:
                val = cm.group(1)
            params[p.group(1)] = val
        calls.append({"name": name, "params": params})
    return calls


def check_match(call, expected):
    if call.get("name") != expected["name"]:
        return False, f"name {call.get('name')} != {expected['name']}"
    for k, v in expected["params"].items():
        got = str(call.get("params", {}).get(k, "")).strip()
        # numeric params compare by value, not string form ("100" == "100.0")
        def num(s):
            try:
                return float(s)
            except ValueError:
                return None
        g, e = num(got), num(v)
        if g is not None and e is not None:
            if abs(g - e) > 1e-9:
                return False, f"param {k} = {got!r} != {v!r}"
        elif got != v:
            return False, f"param {k} = {got!r} != {v!r}"
    return True, None


def main():
    print(f"=== MiniCPM5 TOOL CHECK: {LABEL} (model={MODEL}) ===", flush=True)
    print(f"  server: {API}", flush=True)
    results = []
    for sid, prompt, expected in SCENARIOS:
        tools = [TOOLS[expected["name"]]]
        msg, secs = chat([{"role": "user", "content": prompt}], tools=tools)
        content = msg.get("content") or ""
        json_calls = msg.get("tool_calls") or []
        xml_calls = parse_xml_calls(content)
        print(f"\n--- {sid} ({secs:.1f}s) ---", flush=True)
        print(f"  openai tool_calls field: {len(json_calls)}", flush=True)
        print(f"  XML calls parsed: {len(xml_calls)}", flush=True)
        if xml_calls:
            print(f"  RAW  : {content[:300]}", flush=True)
            ok, why = check_match(xml_calls[0], expected)
            print(f"  VERDICT: {'MATCH' if ok else 'MISMATCH'} {why or ''}", flush=True)
        else:
            print(f"  RAW  : {content[:300]}", flush=True)
            print("  VERDICT: NO XML CALL", flush=True)
            ok = False
        results.append({"scenario": sid, "emitted_calls": len(xml_calls), "match": ok,
                        "raw": content[:500], "secs": round(secs, 1)})

    score = sum(1 for r in results if r["match"])
    print(f"\n=== SUMMARY: {score}/{len(results)} tool calls matched ===", flush=True)
    out = {
        "label": LABEL, "model": MODEL, "server": API, "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "scenarios": results, "score": f"{score}/{len(results)}",
        "note": "MiniCPM5 XML tool protocol: <function name=...><param name=...>...</param></function>. "
                "Generic OpenAI-JSON tool_calls parsing will report 0/5 even when the model calls correctly.",
    }
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", f"{LABEL}.json")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write(json.dumps(out, indent=2))
    print(f"Saved -> {p}", flush=True)


if __name__ == "__main__":
    main()