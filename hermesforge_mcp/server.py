"""
Hermesforge MCP Server

Gives AI agents (Claude, Cursor, Windsurf, etc.) direct access to:
- Screenshot API: capture any URL as an image
- Chart Rendering API: render Chart.js configs as images

Install:
  pip install hermesforge-mcp
  # or: uvx hermesforge-mcp

Configure in Claude Desktop / Cursor / Windsurf:
  {
    "mcpServers": {
      "hermesforge": {
        "command": "hermesforge-mcp",
        "env": {"HERMESFORGE_API_KEY": "your-key-here"}
      }
    }
  }

Free tier: 10 screenshots/day without API key.
API keys at: https://hermesforge.dev/api/keys
"""

import os
import sys
import base64
import requests
from mcp.server.fastmcp import FastMCP

API_BASE = "https://hermesforge.dev"
API_KEY = os.environ.get("HERMESFORGE_API_KEY", "")

mcp = FastMCP("Hermesforge")


def _auth_headers() -> dict:
    if API_KEY:
        return {"X-API-Key": API_KEY}
    return {}


@mcp.tool()
def screenshot_url(
    url: str,
    width: int = 1280,
    height: int = 800,
    format: str = "png",
    full_page: bool = False,
) -> str:
    """
    Capture a screenshot of any web page and return it as a base64-encoded image.

    Use this when you need to:
    - See what a website looks like visually
    - Verify a page rendered correctly
    - Capture UI state for debugging or documentation
    - Extract visual information from a web page

    Args:
        url: The URL to screenshot (must be publicly accessible)
        width: Viewport width in pixels (default: 1280)
        height: Viewport height in pixels (default: 800)
        format: Image format - 'png' or 'jpeg' (default: 'png')
        full_page: Capture the full page height, not just the viewport (default: False)

    Returns:
        Base64-encoded image data with data URI prefix, ready to display.
        Example: "data:image/png;base64,iVBORw0KGgo..."

    Rate limits: 10/day free tier. Get a free API key at https://hermesforge.dev/api/keys
    for 100/day. Paid plans available for higher volume.
    """
    params = {
        "url": url,
        "width": width,
        "height": height,
        "format": format,
        "full_page": str(full_page).lower(),
    }

    try:
        resp = requests.get(
            f"{API_BASE}/api/screenshot",
            params=params,
            headers=_auth_headers(),
            timeout=30,
        )
    except requests.RequestException as e:
        return f"Error: Could not reach Hermesforge API: {e}"

    if resp.status_code == 200:
        img_bytes = resp.content
        b64 = base64.b64encode(img_bytes).decode()
        mime = "image/jpeg" if format == "jpeg" else "image/png"
        return f"data:{mime};base64,{b64}"
    elif resp.status_code == 429:
        try:
            msg = resp.json().get("message", "")
        except Exception:
            msg = ""
        return (
            f"Rate limit reached. {msg} "
            f"Get a free API key at https://hermesforge.dev/api/keys "
            f"or see plans at https://hermesforge.dev/pricing"
        )
    elif resp.status_code == 402:
        return (
            f"Payment required. This endpoint uses x402 micropayments. "
            f"See https://hermesforge.dev/pricing for API key options."
        )
    else:
        return f"Error: API returned {resp.status_code}: {resp.text[:200]}"


@mcp.tool()
def render_chart(
    chart_config: str,
    width: int = 800,
    height: int = 600,
    format: str = "png",
) -> str:
    """
    Render a Chart.js configuration as a chart image.

    Use this when you need to:
    - Visualize data as bar, line, pie, scatter, or other Chart.js chart types
    - Generate charts programmatically from data
    - Create charts for reports or documentation

    Args:
        chart_config: A JSON string containing a valid Chart.js configuration object.
            Example: '{"type":"bar","data":{"labels":["A","B","C"],"datasets":[{"label":"Values","data":[1,2,3]}]}}'
        width: Chart width in pixels (default: 800)
        height: Chart height in pixels (default: 600)
        format: Image format - 'png' or 'jpeg' (default: 'png')

    Returns:
        Base64-encoded chart image with data URI prefix.

    Rate limits: Shared with screenshot API. Get a free API key at https://hermesforge.dev/api/keys
    """
    import json

    # Validate JSON
    try:
        config = json.loads(chart_config)
    except json.JSONDecodeError as e:
        return f"Error: chart_config is not valid JSON: {e}"

    payload = {
        "config": config,
        "width": width,
        "height": height,
        "format": format,
    }

    try:
        resp = requests.post(
            f"{API_BASE}/api/charts/render",
            json=payload,
            headers={**_auth_headers(), "Content-Type": "application/json"},
            timeout=30,
        )
    except requests.RequestException as e:
        return f"Error: Could not reach Hermesforge API: {e}"

    if resp.status_code == 200:
        img_bytes = resp.content
        b64 = base64.b64encode(img_bytes).decode()
        mime = "image/jpeg" if format == "jpeg" else "image/png"
        return f"data:{mime};base64,{b64}"
    elif resp.status_code == 429:
        try:
            msg = resp.json().get("message", "")
        except Exception:
            msg = ""
        return (
            f"Rate limit reached. {msg} "
            f"Get a free API key at https://hermesforge.dev/api/keys"
        )
    else:
        return f"Error: API returned {resp.status_code}: {resp.text[:200]}"


@mcp.tool()
def get_api_usage() -> str:
    """
    Check your current API usage and rate limit status.

    Returns your current usage counts and remaining quota for:
    - Screenshot API
    - Chart Rendering API

    Requires HERMESFORGE_API_KEY environment variable to be set.
    Without an API key, shows anonymous tier limits.
    """
    try:
        resp = requests.get(
            f"{API_BASE}/api/usage",
            headers=_auth_headers(),
            timeout=10,
        )
    except requests.RequestException as e:
        return f"Error: Could not reach Hermesforge API: {e}"

    if resp.status_code == 200:
        return resp.text
    else:
        return f"Error: {resp.status_code}: {resp.text[:200]}"


def main():
    import os
    transport = os.environ.get("MCP_TRANSPORT", "stdio")
    if transport in ("sse", "streamable-http"):
        mcp.run(transport=transport)
    else:
        mcp.run()


if __name__ == "__main__":
    main()
