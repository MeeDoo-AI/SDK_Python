import os
from meedoo_ai import MeeDooClient

API_KEY = os.environ.get("MEEDEO_API_KEY", "")
BASE_URL = os.environ.get("MEEDEO_BASE_URL", "https://api.meedoo.co/api")

if not API_KEY:
    print("MEEDEO_API_KEY not set")
    exit(1)

client = MeeDooClient(api_key=API_KEY, base_url=BASE_URL)

print("=== Test 1: Basic Chat ===")
resp = client.chat.completions.create(model="meedoo:latest", messages=[{"role":"user","content":"Say hello in one word."}])
print(f'AI says: {resp.content}')
print(f'Tokens: {resp.usage.total_tokens}')

print("\n=== Test 2: Web Search ===")
resp = client.chat.completions.create(model="meedoo:latest", messages=[{"role":"user","content":"What is the Bitcoin price today?"}], features={"web_search": True})
print(f'AI says: {resp.content[:100]}...')

print("\n=== Test 3: Think Mode ===")
resp = client.chat.completions.create(model="meedoo:latest", messages=[{"role":"user","content":"What is 7*8?"}], think=True)
print(f'AI says: {resp.content[:100]}')

print("\n=== Test 4: MeeJudge ===")
status = client.judge.status()
print(f'Judge: enabled={status.enabled}, model={status.model}')

print("\n=== Test 5: Credits ===")
c = client.usage.credits()
print(f'Balance: EUR{c.credit_balance}')

print("\n=== ALL TESTS PASSED ===")
