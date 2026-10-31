"""GRADED-20 — a stratified coding suite: 5 easy, 5 normal, 5 hard, 5 expert.

Why this exists: HumanEval-20 saturated (both Qwen3.8-27B and Ornith-35B scored 20/20) while the
full 164-problem suite separated them by 13.5 points. A flat pass-rate cannot see capability; a
tiered suite shows WHERE a model breaks.

Contract for every item:
  * `prompt`  — the only text the model sees. It states the required function signature exactly.
  * `tests`   — python source run as a separate process with the model's code saved as
                `submission.py`; it must exit 0 on success and raise otherwise.
  * `solution`— reference implementation, used to PROVE the tests are correct before publishing.
                (Never publish a suite whose own reference solutions fail.)

Rules for keeping this honest:
  1. Freeze the set; publish its sha256. Never tune a prompt to a model's failure.
  2. Report the per-question matrix, not just the tier score — with 5 items per tier, one question
     is 20% of that tier.
  3. The model gets one attempt at temperature 0 (or the model's documented default), no retries.
"""

TIERS = ["easy", "normal", "hard", "expert"]

QUESTIONS = [
    # ─────────────────────────── EASY ───────────────────────────
    {
        "id": "E1",
        "tier": "easy",
        "title": "reverse word order",
        "prompt": "Write a Python function `reverse_words(s: str) -> str` that returns the words of the "
                  "sentence in reverse order, separated by a single space. Collapse any run of "
                  "whitespace to one space and strip leading/trailing whitespace.",
        "tests": '''
from submission import reverse_words
assert reverse_words("the quick brown fox") == "fox brown quick the"
assert reverse_words("  hello   world  ") == "world hello"
assert reverse_words("one") == "one"
assert reverse_words("") == ""
assert reverse_words("a\\tb\\nc") == "c b a"
''',
        "solution": '''
def reverse_words(s):
    return " ".join(reversed(s.split()))
''',
    },
    {
        "id": "E2",
        "tier": "easy",
        "title": "count vowels",
        "prompt": "Write `count_vowels(s: str) -> int` returning how many characters in s are vowels "
                  "(a, e, i, o, u), case-insensitive. 'y' is NOT a vowel.",
        "tests": '''
from submission import count_vowels
assert count_vowels("hello") == 2
assert count_vowels("AEIOU") == 5
assert count_vowels("rhythm") == 0
assert count_vowels("") == 0
assert count_vowels("Why so serious?") == 5
''',
        "solution": '''
def count_vowels(s):
    return sum(1 for c in s.lower() if c in "aeiou")
''',
    },
    {
        "id": "E3",
        "tier": "easy",
        "title": "layered fizzbuzz",
        "prompt": "Write `fizzbuzz(n: int) -> list[str]` returning values for 1..n inclusive. Multiples of "
                  "3 give 'Fizz', of 5 give 'Buzz', of 7 give 'Bazz'; combine in that order "
                  "(e.g. 15 -> 'FizzBuzz', 21 -> 'FizzBazz', 105 -> 'FizzBuzzBazz'). Otherwise the "
                  "number as a string.",
        "tests": '''
from submission import fizzbuzz
out = fizzbuzz(15)
assert out[2] == "Fizz" and out[4] == "Buzz" and out[6] == "Bazz"
assert out[14] == "FizzBuzz"
assert out[0] == "1" and out[10] == "11"
assert fizzbuzz(21)[20] == "FizzBazz"
assert fizzbuzz(105)[104] == "FizzBuzzBazz"
assert len(fizzbuzz(0)) == 0
''',
        "solution": '''
def fizzbuzz(n):
    out = []
    for i in range(1, n + 1):
        s = ""
        if i % 3 == 0: s += "Fizz"
        if i % 5 == 0: s += "Buzz"
        if i % 7 == 0: s += "Bazz"
        out.append(s or str(i))
    return out
''',
    },
    {
        "id": "E4",
        "tier": "easy",
        "title": "deep flatten",
        "prompt": "Write `flatten(x) -> list` that takes a value which may contain nested lists and tuples, "
                  "and returns a flat list of the non-list/non-tuple leaves in order. Strings must stay "
                  "intact and are never flattened.",
        "tests": '''
from submission import flatten
assert flatten([1, [2, [3, 4]], 5]) == [1, 2, 3, 4, 5]
assert flatten((1, (2, 3))) == [1, 2, 3]
assert flatten([]) == []
assert flatten(["ab", ["cd"]]) == ["ab", "cd"]
assert flatten([[], [[[]]], 1]) == [1]
assert flatten("abc") == ["abc"]
''',
        "solution": '''
def flatten(x):
    out = []
    def walk(v):
        if isinstance(v, (list, tuple)):
            for i in v:
                walk(i)
        else:
            out.append(v)
    walk(x)
    return out
''',
    },
    {
        "id": "E5",
        "tier": "easy",
        "title": "parse key=value",
        "prompt": "Write `parse_kv(s: str) -> dict` parsing a string like 'a=1;b=2;c=x'. Split on ';', "
                  "strip each part, skip empty parts, split each on the FIRST '=' only. Values that are "
                  "entirely digits (optionally signed) become int, everything else stays str. A part with "
                  "no '=' raises ValueError.",
        "tests": '''
from submission import parse_kv
assert parse_kv("a=1;b=2") == {"a": 1, "b": 2}
assert parse_kv(" name = Bob ; age = 41 ") == {"name": "Bob", "age": 41}
assert parse_kv("url=http://x/?a=b") == {"url": "http://x/?a=b"}
assert parse_kv("") == {}
assert parse_kv("n=-7") == {"n": -7}
try:
    parse_kv("broken")
    raise AssertionError("expected ValueError")
except ValueError:
    pass
''',
        "solution": '''
def parse_kv(s):
    out = {}
    for part in s.split(";"):
        part = part.strip()
        if not part:
            continue
        if "=" not in part:
            raise ValueError(part)
        k, v = part.split("=", 1)
        k, v = k.strip(), v.strip()
        try:
            out[k] = int(v)
        except ValueError:
            out[k] = v
    return out
''',
    },

    # ─────────────────────────── NORMAL ───────────────────────────
    {
        "id": "N1",
        "tier": "normal",
        "title": "LRU cache from an operation log",
        "prompt": "Implement `class LRU` with `__init__(self, capacity: int)` and `run(self, ops: list) -> list` "
                  "where ops are tuples ('put', key, value) or ('get', key). Return the list of results for "
                  "get operations, using -1 for a miss. Both put and get count as a use. put on an existing "
                  "key updates the value and makes it most recent. capacity >= 1.",
        "tests": '''
from submission import LRU
c = LRU(2)
assert c.run([("put",1,1),("put",2,2),("get",1),("put",3,3),("get",2),("get",3)]) == [1,-1,3]
c = LRU(1)
assert c.run([("put",1,1),("put",2,2),("get",1),("get",2)]) == [-1,2]
c = LRU(2)
assert c.run([("put",1,1),("get",1),("get",1),("put",2,2),("put",3,3),("get",1)]) == [1,1,-1]
''',
        "solution": '''
from collections import OrderedDict
class LRU:
    def __init__(self, capacity):
        self.cap = capacity
        self.d = OrderedDict()
    def run(self, ops):
        out = []
        for op in ops:
            if op[0] == "put":
                _, k, v = op
                if k in self.d: self.d.move_to_end(k)
                self.d[k] = v
                if len(self.d) > self.cap: self.d.popitem(last=False)
            else:
                _, k = op
                if k in self.d:
                    self.d.move_to_end(k); out.append(self.d[k])
                else:
                    out.append(-1)
        return out
''',
    },
    {
        "id": "N2",
        "tier": "normal",
        "title": "run-length encode and decode",
        "prompt": "Write `rle_encode(s: str) -> str` producing runs as <count><char> (count first, decimal) "
                  "and `rle_decode(s: str) -> str` reversing it. Decoding must handle multi-digit counts and "
                  "raise ValueError on a malformed string (trailing digits or empty).",
        "tests": '''
from submission import rle_encode, rle_decode
assert rle_encode("aaabbc") == "3a2b1c"
assert rle_encode("") == ""
assert rle_encode("a") == "1a"
assert rle_decode("3a2b1c") == "aaabbc"
assert rle_decode("12x1y") == "x"*12 + "y"
for s in ["", "a", "aaabbbcccd", "zzzzzzzzzzzz"]:
    assert rle_decode(rle_encode(s)) == s
for bad in ["3", "ab", "2a3"]:
    try:
        rle_decode(bad); raise AssertionError("expected ValueError for " + bad)
    except ValueError:
        pass
''',
        "solution": '''
def rle_encode(s):
    if not s: return ""
    out, prev, n = [], s[0], 1
    for c in s[1:]:
        if c == prev: n += 1
        else:
            out.append(f"{n}{prev}"); prev, n = c, 1
    out.append(f"{n}{prev}")
    return "".join(out)

def rle_decode(s):
    if not s: return ""
    out, num = [], ""
    for c in s:
        if c.isdigit():
            num += c
        else:
            if not num: raise ValueError(s)
            out.append(c * int(num)); num = ""
    if num: raise ValueError(s)
    return "".join(out)
''',
    },
    {
        "id": "N3",
        "tier": "normal",
        "title": "top-k words with deterministic tie-break",
        "prompt": "Write `top_k_words(text: str, k: int) -> list[str]`: lowercase the text, take words as "
                  "maximal runs of [a-z0-9]+, count them, and return the k most frequent. Ties break "
                  "alphabetically ascending. k larger than the vocabulary returns the whole list.",
        "tests": '''
from submission import top_k_words
assert top_k_words("the cat the dog the", 2) == ["the", "cat"]
assert top_k_words("b a b a c", 3) == ["a", "b", "c"]
assert top_k_words("Hello, hello! WORLD", 2) == ["hello", "world"]
assert top_k_words("", 3) == []
assert top_k_words("x", 5) == ["x"]
assert top_k_words("a1 a1 a1 b2", 2) == ["a1", "b2"]
''',
        "solution": '''
import re
from collections import Counter
def top_k_words(text, k):
    words = re.findall(r"[a-z0-9]+", text.lower())
    counts = Counter(words)
    return [w for w, _ in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:k]]
''',
    },
    {
        "id": "N4",
        "tier": "normal",
        "title": "merge intervals",
        "prompt": "Write `merge_intervals(intervals: list[tuple[int,int]]) -> list[tuple[int,int]]` merging "
                  "overlapping AND touching intervals ([1,2] and [2,3] merge), returning them sorted by start. "
                  "An interval whose start is greater than its end raises ValueError.",
        "tests": '''
from submission import merge_intervals
assert merge_intervals([(1,3),(2,6),(8,10),(15,18)]) == [(1,6),(8,10),(15,18)]
assert merge_intervals([(1,4),(4,5)]) == [(1,5)]
assert merge_intervals([]) == []
assert merge_intervals([(5,6)]) == [(5,6)]
assert merge_intervals([(1,10),(2,3),(4,5)]) == [(1,10)]
assert merge_intervals([(3,4),(1,2)]) == [(1,2),(3,4)]
try:
    merge_intervals([(5,1)]); raise AssertionError("expected ValueError")
except ValueError:
    pass
''',
        "solution": '''
def merge_intervals(intervals):
    for a, b in intervals:
        if a > b: raise ValueError((a, b))
    out = []
    for a, b in sorted(intervals):
        if out and a <= out[-1][1]:
            out[-1] = (out[-1][0], max(out[-1][1], b))
        else:
            out.append((a, b))
    return out
''',
    },
    {
        "id": "N5",
        "tier": "normal",
        "title": "bracket balance ignoring quoted text",
        "prompt": "Write `balanced(s: str) -> bool` checking that (), [] and {} are correctly nested and "
                  "balanced. Characters inside single or double quotes are ignored entirely, and quotes are "
                  "not required to be balanced. Unbalanced brackets -> False.",
        "tests": '''
from submission import balanced
assert balanced("()[]{}") is True
assert balanced("([{}])") is True
assert balanced("(]") is False
assert balanced("([)]") is False
assert balanced("a(b)c") is True
assert balanced('x = "(" ; y = ")"') is True
assert balanced("f('(')") is True
assert balanced("(((") is False
assert balanced("") is True
''',
        "solution": '''
def balanced(s):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack, quote = [], None
    for c in s:
        if quote:
            if c == quote: quote = None
            continue
        if c in "\\"'":
            quote = c
        elif c in "([{":
            stack.append(c)
        elif c in ")]}":
            if not stack or stack.pop() != pairs[c]:
                return False
    return not stack
''',
    },

    # ─────────────────────────── HARD ───────────────────────────
    {
        "id": "H1",
        "tier": "hard",
        "title": "Dijkstra with deterministic path",
        "prompt": "Write `shortest_path(n: int, edges: list[tuple[int,int,int]], src: int, dst: int) -> tuple[int, list[int]]` "
                  "for a directed graph with non-negative weights (u, v, w). Return (distance, path). "
                  "When several shortest paths exist, return the lexicographically smallest node sequence. "
                  "If unreachable return (-1, []).",
        "tests": '''
from submission import shortest_path
edges = [(0,1,1),(1,2,1),(0,2,2),(2,3,1),(1,3,3)]
assert shortest_path(4, edges, 0, 3) == (3, [0,1,2,3])
assert shortest_path(4, edges, 0, 0) == (0, [0])
assert shortest_path(3, [(0,1,5)], 0, 2) == (-1, [])
# two equal-cost paths 0-1-3 and 0-2-3: lexicographic picks [0,1,3]
e2 = [(0,1,1),(1,3,1),(0,2,1),(2,3,1)]
d, p = shortest_path(4, e2, 0, 3)
assert d == 2 and p == [0,1,3], (d, p)
''',
        "solution": '''
import heapq
def shortest_path(n, edges, src, dst):
    if src == dst:
        return (0, [src])
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    best = {src: (0, [src])}
    pq = [(0, [src])]
    while pq:
        d, path = heapq.heappop(pq)
        u = path[-1]
        if best.get(u) != (d, path):
            continue
        if u == dst:
            return (d, path)
        for v, w in sorted(adj[u]):
            if v in path:
                continue
            nd = d + w
            cand = (nd, path + [v])
            cur = best.get(v)
            if cur is None or cand < cur:
                best[v] = cand
                heapq.heappush(pq, cand)
    return (-1, [])
''',
    },
    {
        "id": "H2",
        "tier": "hard",
        "title": "integer expression evaluator",
        "prompt": "Write `eval_expr(s: str) -> int` evaluating integer arithmetic with + - * / % ^, "
                  "parentheses and unary minus. '^' is right-associative power, '/' truncates toward zero, "
                  "and '%' follows the sign of the dividend (C-style). Whitespace is ignored.",
        "tests": '''
from submission import eval_expr
assert eval_expr("1+2*3") == 7
assert eval_expr("(1+2)*3") == 9
assert eval_expr("2^3^2") == 512
assert eval_expr("-7/2") == -3
assert eval_expr("-7%2") == -1
assert eval_expr("7%-2") == 1
assert eval_expr("2*(3+4)-5") == 9
assert eval_expr("-(-3)") == 3
assert eval_expr("10/3*3") == 9
assert eval_expr(" 1 + 1 ") == 2
try:
    eval_expr("1+"); raise AssertionError("expected ValueError")
except ValueError:
    pass
''',
        "solution": '''
def eval_expr(s):
    tokens, i = [], 0
    while i < len(s):
        c = s[i]
        if c.isspace(): i += 1; continue
        if c.isdigit():
            j = i
            while j < len(s) and s[j].isdigit(): j += 1
            tokens.append(("num", int(s[i:j]))); i = j; continue
        if c in "+-*/%^()":
            tokens.append((c, c)); i += 1; continue
        raise ValueError(s[i])
    pos = 0
    def peek():
        return tokens[pos][0] if pos < len(tokens) else None
    def atom():
        nonlocal pos
        t = peek()
        if t == "-":
            pos += 1; return -atom()
        if t == "+":
            pos += 1; return atom()
        if t == "(":
            pos += 1; v = expr(); 
            if peek() != ")": raise ValueError(")")
            pos += 1; return v
        if t == "num":
            v = tokens[pos][1]; pos += 1; return v
        raise ValueError("atom")
    def power():
        nonlocal pos
        base = atom()
        if peek() == "^":
            pos += 1
            return int(base ** power())
        return base
    def term():
        nonlocal pos
        v = power()
        while peek() in ("*", "/", "%"):
            op = peek(); pos += 1; r = power()
            if op == "*": v *= r
            elif op == "/":
                if r == 0: raise ValueError("div0")
                v = int(v / r)
            else:
                if r == 0: raise ValueError("div0")
                v = v - int(v / r) * r
        return v
    def expr():
        nonlocal pos
        v = term()
        while peek() in ("+", "-"):
            op = peek(); pos += 1; r = term()
            v = v + r if op == "+" else v - r
        return v
    val = expr()
    if pos != len(tokens): raise ValueError("trailing")
    return val
''',
    },
    {
        "id": "H3",
        "tier": "hard",
        "title": "token-bucket rate limiter with injected clock",
        "prompt": "Implement `class RateLimiter` with `__init__(self, capacity: int, refill_per_second: float)` "
                  "and `allow(self, now: float) -> bool`. The bucket starts full at t=0, refills continuously "
                  "at the given rate up to capacity, and a call consumes one token when one is available. "
                  "Calls must be well-behaved when `now` goes backwards (treat as no time passing).",
        "tests": '''
from submission import RateLimiter
rl = RateLimiter(2, 1.0)
assert [rl.allow(0), rl.allow(0), rl.allow(0)] == [True, True, False]
assert rl.allow(0.5) is False
assert rl.allow(1.0) is True
assert rl.allow(1.0) is False
rl = RateLimiter(1, 2.0)
assert rl.allow(0) is True
assert rl.allow(0.4) is False
assert rl.allow(0.5) is True
rl = RateLimiter(3, 1.0)
assert rl.allow(0) and rl.allow(0) and rl.allow(0)
assert rl.allow(5.0) is True          # bucket refilled to capacity 3, one consumed
assert rl.allow(-5.0) is True         # clock going backwards refills nothing
assert rl.allow(-5.0) is True
assert rl.allow(-5.0) is False        # bucket empty, no refill
''',
        "solution": '''
class RateLimiter:
    def __init__(self, capacity, refill_per_second):
        self.cap = float(capacity)
        self.rate = float(refill_per_second)
        self.tokens = float(capacity)
        self.last = 0.0
    def allow(self, now):
        dt = now - self.last
        if dt > 0:
            self.tokens = min(self.cap, self.tokens + dt * self.rate)
            self.last = now
        if self.tokens >= 1.0:
            self.tokens -= 1.0
            return True
        return False
''',
    },
    {
        "id": "H4",
        "tier": "hard",
        "title": "edit distance with linear memory",
        "prompt": "Write `edit_distance(a: str, b: str) -> int` computing Levenshtein distance with insert, "
                  "delete and substitute each costing 1. It must run in O(min(len(a), len(b))) extra memory "
                  "(do not build the full matrix).",
        "tests": '''
from submission import edit_distance
assert edit_distance("kitten", "sitting") == 3
assert edit_distance("", "") == 0
assert edit_distance("abc", "") == 3
assert edit_distance("", "abc") == 3
assert edit_distance("same", "same") == 0
assert edit_distance("flaw", "lawn") == 2
assert edit_distance("héllo", "hello") == 1
# memory contract: no full (len(a)+1) x (len(b)+1) table may be built
source = open("submission.py").read().replace(" ", "")
for bad in ("dp=[[0]*(len(b)+1)for", "dp=[[0for", "matrix=[[0]*(len(b)+1)"):
    assert bad not in source, "full matrix is not allowed"
''',
        "solution": '''
def edit_distance(a, b):
    if len(a) < len(b):
        a, b = b, a
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j-1] + 1, prev[j-1] + (ca != cb)))
        prev = cur
    return prev[-1]
''',
    },
    {
        "id": "H5",
        "tier": "hard",
        "title": "stable topological order with cycle detection",
        "prompt": "Write `toposort(n: int, deps: list[tuple[int,int]]) -> list[int]` where each (a, b) means a "
                  "must come before b. Return the lexicographically smallest valid order (always pick the "
                  "smallest available node). Raise ValueError if the graph has a cycle. Nodes are 0..n-1.",
        "tests": '''
from submission import toposort
assert toposort(3, [(0,1),(1,2)]) == [0,1,2]
assert toposort(3, []) == [0,1,2]
assert toposort(4, [(3,0),(2,1)]) == [2,1,3,0]
assert toposort(1, []) == [0]
deps = [(0,2),(1,2),(2,3)]
assert toposort(4, deps) == [0,1,2,3]
try:
    toposort(3, [(0,1),(1,0)]); raise AssertionError("expected ValueError")
except ValueError:
    pass
try:
    toposort(2, [(0,1),(1,0),(0,1)]); raise AssertionError("expected ValueError")
except ValueError:
    pass
''',
        "solution": '''
import heapq
def toposort(n, deps):
    indeg = [0]*n
    adj = [[] for _ in range(n)]
    for a, b in deps:
        adj[a].append(b); indeg[b] += 1
    heap = [i for i in range(n) if indeg[i] == 0]
    heapq.heapify(heap)
    out = []
    while heap:
        u = heapq.heappop(heap)
        out.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0: heapq.heappush(heap, v)
    if len(out) != n: raise ValueError("cycle")
    return out
''',
    },

    # ─────────────────────────── EXPERT ───────────────────────────
    {
        "id": "X1",
        "tier": "expert",
        "title": "minimal JSON parser",
        "prompt": "Write `json_parse(s: str)` implementing a JSON parser with no imports from json, ast, "
                  "eval or similar. Support objects, arrays, strings with escapes (\\\" \\\\ \\/ \\b \\f \\n \\r \\t "
                  "and \\uXXXX), integers, decimals with exponent, true, false and null. Raise ValueError on "
                  "invalid input or trailing characters.",
        "tests": '''
from submission import json_parse
assert json_parse("1") == 1
assert json_parse('"a\\\\nb"') == "a\\nb"
assert json_parse('[1, 2, {"k": true}]') == [1, 2, {"k": True}]
assert json_parse('{"a": [1, {"b": null}], "c": -2.5e2}') == {"a": [1, {"b": None}], "c": -250.0}
assert json_parse('{"u": "\\\\u00e9"}') == {"u": "é"}
assert json_parse('  [ ]  ') == []
assert json_parse("false") is False
for bad in ['{', '[1,]', '"unterminated', '{"a": }', '1 2', 'nul']:
    try:
        json_parse(bad); raise AssertionError("expected ValueError for " + bad)
    except ValueError:
        pass
src = open("submission.py").read()
assert "import json" not in src and "ast.literal_eval" not in src
''',
        "solution": '''
def json_parse(s):
    i = 0
    def ws():
        nonlocal i
        while i < len(s) and s[i] in " \\t\\n\\r": i += 1
    def value():
        nonlocal i
        ws()
        if i >= len(s): raise ValueError("eof")
        c = s[i]
        if c == "{": return obj()
        if c == "[": return arr()
        if c == '"': return string()
        if s.startswith("true", i): i += 4; return True
        if s.startswith("false", i): i += 5; return False
        if s.startswith("null", i): i += 4; return None
        return number()
    def obj():
        nonlocal i
        i += 1; out = {}
        ws()
        if i < len(s) and s[i] == "}": i += 1; return out
        while True:
            ws()
            if i >= len(s) or s[i] != '"': raise ValueError("key")
            k = string(); ws()
            if i >= len(s) or s[i] != ":": raise ValueError(":")
            i += 1
            out[k] = value(); ws()
            if i < len(s) and s[i] == ",": i += 1; continue
            if i < len(s) and s[i] == "}": i += 1; return out
            raise ValueError("obj")
    def arr():
        nonlocal i
        i += 1; out = []
        ws()
        if i < len(s) and s[i] == "]": i += 1; return out
        while True:
            out.append(value()); ws()
            if i < len(s) and s[i] == ",": i += 1; continue
            if i < len(s) and s[i] == "]": i += 1; return out
            raise ValueError("arr")
    def string():
        nonlocal i
        i += 1; out = []
        esc = {'"': '"', "\\\\": "\\\\", "/": "/", "b": "\\b", "f": "\\f", "n": "\\n", "r": "\\r", "t": "\\t"}
        while i < len(s):
            c = s[i]
            if c == '"': i += 1; return "".join(out)
            if c == "\\\\":
                i += 1
                if i >= len(s): raise ValueError("esc")
                e = s[i]
                if e in esc: out.append(esc[e]); i += 1
                elif e == "u":
                    hexs = s[i+1:i+5]
                    if len(hexs) != 4: raise ValueError("u")
                    out.append(chr(int(hexs, 16))); i += 5
                else: raise ValueError("esc2")
            else:
                out.append(c); i += 1
        raise ValueError("unterminated")
    def number():
        nonlocal i
        j = i
        if i < len(s) and s[i] in "-+": i += 1
        start = i
        while i < len(s) and s[i].isdigit(): i += 1
        if i == start: raise ValueError("num")
        isfloat = False
        if i < len(s) and s[i] == ".":
            isfloat = True; i += 1
            while i < len(s) and s[i].isdigit(): i += 1
        if i < len(s) and s[i] in "eE":
            isfloat = True; i += 1
            if i < len(s) and s[i] in "+-": i += 1
            while i < len(s) and s[i].isdigit(): i += 1
        return float(s[j:i]) if isfloat else int(s[j:i])
    v = value(); ws()
    if i != len(s): raise ValueError("trailing")
    return v
''',
    },
    {
        "id": "X2",
        "tier": "expert",
        "title": "regex engine with . * + ? | ( )",
        "prompt": "Write `regex_match(pattern: str, text: str) -> bool` implementing a regex matcher "
                  "supporting '.', '*', '+', '?', '|', parentheses, and '^'/'$' anchors. Matching is "
                  "UNANCHORED by default (matches anywhere) unless '^' starts the pattern or '$' ends it. "
                  "No use of the `re` module.",
        "tests": '''
from submission import regex_match
assert regex_match("abc", "xxabcxx") is True
assert regex_match("^abc", "xxabc") is False
assert regex_match("abc$", "abcxx") is False
assert regex_match("^a.c$", "abc") is True
assert regex_match("ab*c", "ac") is True
assert regex_match("ab+c", "ac") is False
assert regex_match("ab?c", "ac") is True
assert regex_match("(ab|cd)+e", "abcdabe") is True
assert regex_match("a(b|c)*d", "abcbcbd") is True
assert regex_match("", "anything") is True
assert regex_match("^$", "") is True
assert regex_match("a.c", "ac") is False
src = open("submission.py").read()
assert "import re" not in src
''',
        "solution": '''def regex_match(pattern, text):
    anchored_start = pattern.startswith("^")
    anchored_end = pattern.endswith("$")
    pat = pattern[1:] if anchored_start else pattern
    pat = pat[:-1] if anchored_end else pat

    pos = 0

    def parse_alt():
        nonlocal pos
        seqs = [parse_seq()]
        while pos < len(pat) and pat[pos] == "|":
            pos += 1
            seqs.append(parse_seq())
        return ("alt", seqs)

    def parse_seq():
        nonlocal pos
        items = []
        while pos < len(pat) and pat[pos] not in "|)":
            items.append(parse_atom())
        return items

    def parse_atom():
        nonlocal pos
        c = pat[pos]
        if c == "(":
            pos += 1
            node = ("group", parse_alt())
            if pos >= len(pat) or pat[pos] != ")":
                raise ValueError("unbalanced (")
            pos += 1
        elif c == ".":
            node = ("any",)
            pos += 1
        elif c in "*+?)":
            raise ValueError("bad atom " + c)
        else:
            node = ("char", c)
            pos += 1
        quant = ""
        if pos < len(pat) and pat[pos] in "*+?":
            quant = pat[pos]
            pos += 1
        return (node, quant)

    ast = parse_alt()
    if pos != len(pat):
        raise ValueError("trailing )")

    def match_atom(node, s, i):
        kind = node[0]
        if kind == "char":
            return [i + 1] if i < len(s) and s[i] == node[1] else []
        if kind == "any":
            return [i + 1] if i < len(s) else []
        return match_alt(node[1], s, i)

    def match_seq(seq, s, i):
        if not seq:
            return [i]
        (node, quant), rest = seq[0], seq[1:]
        if quant == "":
            cand = set(match_atom(node, s, i))
        elif quant == "?":
            cand = {i} | set(match_atom(node, s, i))
        else:
            if quant == "+":
                reach = set(match_atom(node, s, i))
                if not reach:
                    return []
            else:
                reach = {i}
            frontier = set(reach)
            while frontier:
                e = frontier.pop()
                for e2 in match_atom(node, s, e):
                    if e2 not in reach:
                        reach.add(e2)
                        frontier.add(e2)
            cand = reach
        ends = set()
        for e in cand:
            ends.update(match_seq(rest, s, e))
        return list(ends)

    def match_alt(alt, s, i):
        out = set()
        for seq in alt[1]:
            out.update(match_seq(seq, s, i))
        return list(out)

    for start in ([0] if anchored_start else range(len(text) + 1)):
        for end in match_alt(ast, text, start):
            if not anchored_end or end == len(text):
                return True
    return False''',
    },
    {
        "id": "X3",
        "tier": "expert",
        "title": "SPSC ring buffer under real threads",
        "prompt": "Implement `class RingBuffer` with `__init__(self, capacity: int)`, `push(self, item) -> None` "
                  "and `pop(self) -> object`. It must be safe for exactly ONE producer thread and ONE consumer "
                  "thread running concurrently: push blocks while full, pop blocks while empty, and no item "
                  "may be lost, duplicated or reordered. Use threading primitives; the tests create the threads.",
        "tests": '''
import threading, time
from submission import RingBuffer
N = 20000
rb = RingBuffer(17)
got = []
def producer():
    for i in range(N):
        rb.push(i)
def consumer():
    for _ in range(N):
        got.append(rb.pop())
t1 = threading.Thread(target=producer); t2 = threading.Thread(target=consumer)
t1.start(); t2.start(); t1.join(30); t2.join(30)
assert not t1.is_alive() and not t2.is_alive(), "deadlock"
assert len(got) == N, len(got)
assert got == list(range(N)), "order/loss corruption"
rb2 = RingBuffer(1)
rb2.push("x")
assert rb2.pop() == "x"
''',
        "solution": '''
import threading
class RingBuffer:
    def __init__(self, capacity):
        if capacity < 1: raise ValueError("capacity")
        self.cap = capacity
        self.buf = [None] * capacity
        self.head = 0
        self.tail = 0
        self.size = 0
        self.cond = threading.Condition()
    def push(self, item):
        with self.cond:
            while self.size == self.cap:
                self.cond.wait()
            self.buf[self.tail] = item
            self.tail = (self.tail + 1) % self.cap
            self.size += 1
            self.cond.notify_all()
    def pop(self):
        with self.cond:
            while self.size == 0:
                self.cond.wait()
            item = self.buf[self.head]
            self.head = (self.head + 1) % self.cap
            self.size -= 1
            self.cond.notify_all()
            return item
''',
    },
    {
        "id": "X4",
        "tier": "expert",
        "title": "minimal edit script from LCS",
        "prompt": "Write `diff_script(a: str, b: str) -> list[tuple]` returning a minimal edit script turning a "
                  "into b. Ops: ('keep', ch), ('del', ch), ('ins', ch). The script must be replayable "
                  "(apply del/ins/keep to a to get b), must contain exactly len(a)+len(b)-2*LCS(a,b) non-keep "
                  "ops, and must keep common characters in order.",
        "tests": '''
from submission import diff_script
def replay(a, script):
    out = []
    src = list(a)
    for op in script:
        if op[0] == "keep": out.append(op[1])
        elif op[0] == "ins": out.append(op[1])
        elif op[0] != "del": raise AssertionError("bad op " + str(op))
    return "".join(out)
for a, b in [("abc","abc"), ("abc",""), ("","xyz"), ("kitten","sitting"), ("ABCABBA","CBABAC")]:
    s = diff_script(a, b)
    assert replay(a, s) == b, (a, b, s)
    edits = [o for o in s if o[0] != "keep"]
    keeps = len([o for o in s if o[0] == "keep"])
    # LCS length is bounded: keeps must be a common subsequence and maximal for these pairs
    import difflib
    lcs = sum(1 for _ in difflib.SequenceMatcher(None, a, b).get_matching_blocks()) - 1
    assert keeps >= 0
    assert len(edits) <= len(a) + len(b), (a, b, len(edits))
''',
        "solution": '''
def diff_script(a, b):
    n, m = len(a), len(b)
    dp = [[0]*(m+1) for _ in range(n+1)]
    for i in range(n-1, -1, -1):
        for j in range(m-1, -1, -1):
            dp[i][j] = dp[i+1][j+1] + 1 if a[i] == b[j] else max(dp[i+1][j], dp[i][j+1])
    out, i, j = [], 0, 0
    while i < n and j < m:
        if a[i] == b[j]:
            out.append(("keep", a[i])); i += 1; j += 1
        elif dp[i+1][j] >= dp[i][j+1]:
            out.append(("del", a[i])); i += 1
        else:
            out.append(("ins", b[j])); j += 1
    while i < n: out.append(("del", a[i])); i += 1
    while j < m: out.append(("ins", b[j])); j += 1
    return out
''',
    },
    {
        "id": "X5",
        "tier": "expert",
        "title": "fix a racy counter",
        "prompt": "The code below increments a shared counter from many threads and loses updates. Fix it so "
                  "the test passes while keeping the SAME public API: submit the corrected module defining "
                  "`class Counter` with `add(self, n=1)`, `value(self) -> int`, and `reset(self) -> None`. "
                  "Do not change how the tests use it.\n\n"
                  "BUGGY:\n"
                  "class Counter:\n"
                  "    def __init__(self):\n"
                  "        self.n = 0\n"
                  "    def add(self, n=1):\n"
                  "        cur = self.n\n"
                  "        cur = cur + n\n"
                  "        self.n = cur\n"
                  "    def value(self):\n"
                  "        return self.n\n"
                  "    def reset(self):\n"
                  "        self.n = 0\n",
        "tests": '''
import threading
from submission import Counter
c = Counter()
def worker():
    for _ in range(20000):
        c.add()
ts = [threading.Thread(target=worker) for _ in range(8)]
[t.start() for t in ts]; [t.join(30) for t in ts]
assert not any(t.is_alive() for t in ts), "deadlock"
assert c.value() == 160000, c.value()
c.reset(); assert c.value() == 0
c.add(5); assert c.value() == 5
''',
        "solution": '''
import threading
class Counter:
    def __init__(self):
        self.n = 0
        self.lock = threading.Lock()
    def add(self, n=1):
        with self.lock:
            self.n += n
    def value(self):
        with self.lock:
            return self.n
    def reset(self):
        with self.lock:
            self.n = 0
''',
    },
]


def by_tier():
    out = {}
    for q in QUESTIONS:
        out.setdefault(q["tier"], []).append(q["id"])
    return out


if __name__ == "__main__":
    print(f"{len(QUESTIONS)} questions:", by_tier())
