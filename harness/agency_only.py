#!/usr/bin/env python3
"""Agency-15 only, against any OpenAI-compatible endpoint.
Usage: LM_API=... MODEL=... [AGENCY_TEMP=0.5] [THINKING_ENABLED=0] python3 agency_only.py <label>
"""
import json, time, sys, os
sys.path.insert(0, "/Users/pasc/Projects/AlitaAICore/benchmarks")
import full_test_model as ft

MODEL = os.environ.get("MODEL", "gemma-4-31b-jang_4m-crack@q4_k_m")
LABEL = sys.argv[1] if len(sys.argv) > 1 else "agency"
ft.MODEL = MODEL
ft.OUT_DIR = "/Users/pasc/Projects/AlitaAICore/benchmarks/results"

print(f"=== AGENCY-15: {LABEL} (model={MODEL}) ===", flush=True)
print(f"API: {ft.API}", flush=True)
score, detail = ft.run_agency()
print(f"\nAgency: {score}/15", flush=True)

result = {"label": LABEL, "model": MODEL, "agency": score,
          "agency_detail": detail,
          "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}
path = os.path.join(ft.OUT_DIR, LABEL + ".json")
with open(path, "w") as f:
    json.dump(result, f, indent=2, default=list)
print(f"Saved -> {path}", flush=True)
print(f"=== {LABEL} Agency: {score}/15 ===", flush=True)