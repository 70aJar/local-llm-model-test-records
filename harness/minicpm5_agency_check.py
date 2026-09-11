#!/usr/bin/env python3
"""MiniCPM5 agency checker (XML protocol) — reuses the generic harness's 15 scenarios.

The generic harness reads only OpenAI-JSON `tool_calls`. MiniCPM5-1B/2B emit XML
`<function name="..."><param ...>` tool calls (see chat_template.jinja), so the
generic agency section reports ~0/15 even when the model selects the right tool.
This script runs the SAME 15 scenarios but parses XML calls and scores the model
on the tool name actually chosen.

Usage:
  LM_API=... LM_API_KEY=... MODEL=... AGENCY_TEMP=0.5 \
  python3 benchmarks/minicpm5_agency_check.py "<label>"

Env: LM_API (required), LM_API_KEY (optional), MODEL (default MiniCPM5-2B),
     AGENCY_TEMP (default 0.0).
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
TEMP = float(os.environ.get("AGENCY_TEMP", "0.0"))
LABEL = sys.argv[1] if len(sys.argv) > 1 else "minicpm5-agency"

AGENCY_SYSTEM = (
    "You are an assistant with access to tools. Choose the correct tool for the "
    "task and return ONLY the tool call. Never mention tools you are not using."
)

# Same scenarios as full_test_model.py's AGENCY_SCENARIOS (name, prompt, expected-tools, must_empty)
AGENCY_SCENARIOS = [
    ("dept_lookup", "What department does Alice Chen work in?", {"lookup_employee"}, False),
    ("list_active_eng", "List all active employees in Engineering.", {"search_directory"}, False),
    ("count_eng", "How many people are listed in the Engineering department?", {"search_directory"}, False),
    ("list_support_platform", "List everyone who works in Support or Platform.", {"search_directory"}, False),
    ("book_room_b", "Book Conference Room B tomorrow 14:00-15:00 UTC for a standup.", {"book_room"}, False),
    ("book_room_a", "Book Room A this Friday 09:00-10:00 UTC for sprint planning.", {"book_room"}, False),
    ("check_room_b", "Is Conference Room B available tomorrow from 14:00 to 15:00 UTC?", {"check_availability"}, False),
    ("ticket_manager", "Open a medium ticket 'Budget report outdated' in the finance project.", {"open_ticket"}, False),
    ("ticket_support_lead", "Assign Lindsey Tran a support ticket about 'Slow login' in healthcheck project.", {"assign_ticket"}, False),
    ("ticket_platform", "Open a low-severity ticket 'Cron job failing' in the platform project, then tell me the ticket id.", {"open_ticket"}, False),
    ("convert_eur_usd", "Convert 50 EUR to USD.", {"convert_currency"}, False),
    ("convert_usd_jpy", "Convert $75 to JPY.", {"convert_currency"}, False),
    ("restraint_thanks", "Thanks!", set(), True),
    ("restraint_weather", "How are you today?", set(), True),
    ("focus_team", "Get me the ticket status for team X?", {"get_ticket_status"}, False),
]

AGENCY_TOOLS = [
    {"type": "function", "function": {"name": "lookup_employee", "description": "Find an employee by name, email, or ID", "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}},
    {"type": "function", "function": {"name": "search_directory", "description": "List or filter staff (e.g. by department or active status)", "parameters": {"type": "object", "properties": {"department": {"type": "string"}, "active": {"type": "boolean"}}}}},
    {"type": "function", "function": {"name": "book_room", "description": "Reserve a meeting room with ISO-8601 UTC times", "parameters": {"type": "object", "properties": {"room": {"type": "string"}, "start": {"type": "string"}, "end": {"type": "string"}}, "required": ["room", "start", "end"]}}},
    {"type": "function", "function": {"name": "check_availability", "description": "Check whether a meeting room is free", "parameters": {"type": "object", "properties": {"room": {"type": "string"}, "start": {"type": "string"}, "end": {"type": "string"}}, "required": ["room", "start", "end"]}}},
    {"type": "function", "function": {"name": "open_ticket", "description": "Open a support ticket", "parameters": {"type": "object", "properties": {"title": {"type": "string"}, "project": {"type": "string"}, "severity": {"type": "string"}}, "required": ["title", "project", "severity"]}}},
    {"type": "function", "function": {"name": "assign_ticket", "description": "Assign a ticket to an employee", "parameters": {"type": "object", "properties": {"ticket_id": {"type": "string"}, "assignee": {"type": "string"}}, "required": ["ticket_id", "assignee"]}}},
    {"type": "function", "function": {"name": "convert_currency", "description": "Convert an amount between currencies", "parameters": {"type": "object", "properties": {"amount": {"type": "number"}, "from": {"type": "string"}, "to": {"type": "string"}}, "required": ["amount", "from", "to"]}}},
    {"type": "function", "function": {"name": "get_ticket_status", "description": "Get the status of a ticket by ID", "parameters": {"type": "object", "properties": {"ticket_id": {"type": "string"}}, "required": ["ticket_id"]}}},
]


def chat(messages, tools=None, max_tokens=8000):
    payload = {"model": MODEL, "messages": messages, "max_tokens": max_tokens, "temperature": TEMP}
    if tools:
        payload["tools"] = tools
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


def parse_xml_names(content: str):
    return [m.group(1) for m in XML_RE.finditer(content or "")]


def main():
    print(f"=== MiniCPM5 AGENCY CHECK (XML-aware): {LABEL} (model={MODEL}) ===", flush=True)
    total, detail = 0, []
    for name, prompt, expected, must_empty in AGENCY_SCENARIOS:
        msg, dt = chat([{"role": "system", "content": AGENCY_SYSTEM}, {"role": "user", "content": prompt}],
                       tools=AGENCY_TOOLS)
        content = msg.get("content") or ""
        json_names = [tc["function"]["name"] for tc in (msg.get("tool_calls") or [])]
        xml_names = parse_xml_names(content)
        names = json_names or xml_names  # accept either; XML is MiniCPM's native
        if name in ("restraint_thanks", "restraint_weather"):
            passed = len(names) == 0
            effective = names  # show what (if anything) it emitted
        else:
            passed = (expected & set(names)) and ("wiki_search" not in names)
            effective = names
        total += 1 if passed else 0
        detail.append({"scenario": name, "pass": passed, "calls": list(effective), "raw": (content or "")[:200]})
        print(f"  {name:20s} [{'PASS' if passed else 'FAIL'}] {effective}  raw={content[:90]!r}", flush=True)
    print(f"\n=== SUMMARY: {total}/{len(AGENCY_SCENARIOS)} ===", flush=True)
    out = {"label": LABEL, "model": MODEL, "score": f"{total}/{len(AGENCY_SCENARIOS)}",
           "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
           "note": "XML-aware agency (MiniCPM5 protocol). Generic JSON-only agency reports ~2/15 for this family because XML calls are ignored.",
           "scenarios": detail}
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", f"{LABEL}.json")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write(json.dumps(out, indent=2, default=str))
    print(f"Saved -> {p}", flush=True)


if __name__ == "__main__":
    main()