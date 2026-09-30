import asyncio
import json
import aiohttp

async def get_cookies():
    ws_url = "ws://localhost:9222/devtools/page/5C2675DDB990D6E63D41BFBA18D5CD5D"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(ws_url) as ws:
                # Get cookies
                await ws.send_str(json.dumps({"id": 1, "method": "Network.getCookies", "params": {"urls": ["https://leetcode.com", "https://leetcode.com/"]}}))
                
                cookies = []
                for _ in range(10):
                    msg = await ws.receive()
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        data = json.loads(msg.data)
                        if data.get("id") == 1 and "result" in data:
                            cookies = data["result"]["cookies"]
                            break
                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        break
                
                return cookies
    except Exception as e:
        print(f"WebSocket error: {e}")
        return []

cookies = asyncio.run(get_cookies())
print("=== Cookies found ===")
for c in cookies:
    print(f"{c['name']}: {c['value'][:50]}..." if len(c['value']) > 50 else f"{c['name']}: {c['value']}")

# Write to lc_cookies.txt in Netscape format
if cookies:
    lines = ["# Netscape HTTP Cookie File"]
    for c in cookies:
        domain_flag = "TRUE" if c.get("domain", "").startswith(".") else "FALSE"
        secure_flag = "TRUE" if c.get("secure", False) else "FALSE"
        expires = int(c.get("expires", 0)) if c.get("expires") else 0
        lines.append(f"{c['domain']}\t{domain_flag}\t{c['path']}\t{secure_flag}\t{expires}\t{c['name']}\t{c['value']}")
    
    with open("lc_cookies.txt", "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"\nSaved {len(cookies)} cookies to lc_cookies.txt")
else:
    print("No cookies found!")