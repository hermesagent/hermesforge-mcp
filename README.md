# Hermesforge MCP Server

<!-- mcp-name: io.github.hermesagent/hermesforge-mcp -->

Give your AI agent (Claude, Cursor, Windsurf, Cline) the ability to **screenshot any URL** and **render charts** — directly from the model context.

## Tools

| Tool | Description |
|------|-------------|
| `screenshot_url` | Capture a screenshot of any public web page |
| `render_chart` | Render a Chart.js config as a chart image |
| `get_api_usage` | Check your current usage and rate limits |

## Installation

### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "hermesforge": {
      "command": "uvx",
      "args": ["hermesforge-mcp"],
      "env": {
        "HERMESFORGE_API_KEY": "your-key-here"
      }
    }
  }
}
```

### Cursor / Windsurf / Cline

```json
{
  "mcpServers": {
    "hermesforge": {
      "command": "python",
      "args": ["-m", "hermesforge_mcp.server"],
      "env": {
        "HERMESFORGE_API_KEY": "your-key-here"
      }
    }
  }
}
```

## API Keys

- **Free tier**: 10 screenshots/day, no key required
- **Free API key**: 100/day — get one at [hermesforge.dev/api/keys](https://hermesforge.dev/api/keys)
- **Paid plans**: higher volume at [hermesforge.dev/pricing](https://hermesforge.dev/pricing)

## Usage Examples

Once connected, your AI agent can:

```
Take a screenshot of https://example.com
```

```
Render this chart:
{"type": "bar", "data": {"labels": ["Q1","Q2","Q3"], "datasets": [{"label": "Revenue", "data": [12000, 15000, 18000]}]}}
```

## Rate Limits

Rate limits are per API key (or per IP for anonymous use). When you hit a limit, the tool returns a helpful message with upgrade options.

## License

MIT
