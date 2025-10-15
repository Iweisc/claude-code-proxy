# Parameter Normalization

## Overview

The proxy server includes automatic parameter normalization for tool calls to handle common parameter name variations. This ensures compatibility with different clients that may use slightly different parameter naming conventions.

## Supported Tools

The following tools have parameter normalization enabled:

### read_file
- `file_path` → `path`
- `filepath` → `path`
- `file` → `path`
- Removes unsupported parameters: `offset`, `limit`

### write_to_file
- `file_path` → `path`
- `filepath` → `path`
- `file` → `path`

### apply_diff
- `file_path` → `path`
- `filepath` → `path`
- `file` → `path`

## How It Works

When the proxy receives a tool call from the LLM, it automatically normalizes the parameters before sending them back to the client. This happens in two places:

1. **In `convert_anthropic_to_litellm()`**: When processing tool_use blocks in messages
2. **In `convert_litellm_to_anthropic()`**: When converting LLM responses back to Anthropic format

## Example

If a client sends a tool call like this:

```json
{
  "type": "tool_use",
  "id": "toolu_123",
  "name": "read_file",
  "input": {
    "file_path": "/test/file.txt",
    "offset": 100,
    "limit": 50
  }
}
```

The proxy will automatically normalize it to:

```json
{
  "type": "tool_use",
  "id": "toolu_123",
  "name": "read_file",
  "input": {
    "path": "/test/file.txt"
  }
}
```

## Adding New Mappings

To add parameter normalization for a new tool, edit the `PARAMETER_MAPPINGS` dictionary in [`server.py`](server.py:130):

```python
PARAMETER_MAPPINGS = {
    "your_tool_name": {
        "old_param_name": "new_param_name",
        "another_old_name": "correct_name"
    }
}
```

## Testing

Run the parameter normalization tests:

```bash
python3 test_parameter_normalization.py
```

## Why This Is Needed

Different AI coding assistants and clients may use different parameter naming conventions. For example:
- Some use `file_path` while others use `path`
- Some include pagination parameters like `offset` and `limit` that aren't supported by all tools

This normalization layer ensures compatibility across different clients without requiring changes to the underlying tools.