#!/usr/bin/env python3
"""
Test script to verify parameter normalization for tool calls.
This tests that common parameter name variations are properly mapped.
"""

import json
from server import normalize_tool_parameters

def test_read_file_normalization():
    """Test that read_file parameter variations are normalized correctly."""
    print("Testing read_file parameter normalization...")
    
    # Test case 1: file_path -> path
    params1 = {
        "file_path": "/test/file.txt",
        "offset": 100,
        "limit": 50
    }
    result1 = normalize_tool_parameters("read_file", params1)
    assert result1 == {"path": "/test/file.txt"}, f"Expected {{'path': '/test/file.txt'}}, got {result1}"
    print("✓ file_path -> path (removed offset, limit)")
    
    # Test case 2: filepath -> path
    params2 = {
        "filepath": "/test/file.txt"
    }
    result2 = normalize_tool_parameters("read_file", params2)
    assert result2 == {"path": "/test/file.txt"}, f"Expected {{'path': '/test/file.txt'}}, got {result2}"
    print("✓ filepath -> path")
    
    # Test case 3: file -> path
    params3 = {
        "file": "/test/file.txt"
    }
    result3 = normalize_tool_parameters("read_file", params3)
    assert result3 == {"path": "/test/file.txt"}, f"Expected {{'path': '/test/file.txt'}}, got {result3}"
    print("✓ file -> path")
    
    # Test case 4: Already correct parameter name
    params4 = {
        "path": "/test/file.txt"
    }
    result4 = normalize_tool_parameters("read_file", params4)
    assert result4 == {"path": "/test/file.txt"}, f"Expected {{'path': '/test/file.txt'}}, got {result4}"
    print("✓ path -> path (no change)")
    
    # Test case 5: Multiple parameters with normalization
    params5 = {
        "file_path": "/test/file.txt",
        "encoding": "utf-8",
        "offset": 0,
        "limit": 100
    }
    result5 = normalize_tool_parameters("read_file", params5)
    assert result5 == {"path": "/test/file.txt", "encoding": "utf-8"}, f"Expected {{'path': '/test/file.txt', 'encoding': 'utf-8'}}, got {result5}"
    print("✓ Multiple parameters normalized correctly")

def test_write_to_file_normalization():
    """Test that write_to_file parameter variations are normalized correctly."""
    print("\nTesting write_to_file parameter normalization...")
    
    params = {
        "file_path": "/test/output.txt",
        "content": "Hello, world!"
    }
    result = normalize_tool_parameters("write_to_file", params)
    assert result == {"path": "/test/output.txt", "content": "Hello, world!"}, f"Expected normalized params, got {result}"
    print("✓ file_path -> path for write_to_file")

def test_apply_diff_normalization():
    """Test that apply_diff parameter variations are normalized correctly."""
    print("\nTesting apply_diff parameter normalization...")
    
    params = {
        "file_path": "/test/file.txt",
        "diff": "some diff content"
    }
    result = normalize_tool_parameters("apply_diff", params)
    assert result == {"path": "/test/file.txt", "diff": "some diff content"}, f"Expected normalized params, got {result}"
    print("✓ file_path -> path for apply_diff")

def test_unknown_tool():
    """Test that unknown tools pass through parameters unchanged."""
    print("\nTesting unknown tool (no normalization)...")
    
    params = {
        "file_path": "/test/file.txt",
        "some_param": "value"
    }
    result = normalize_tool_parameters("unknown_tool", params)
    assert result == params, f"Expected unchanged params, got {result}"
    print("✓ Unknown tool parameters unchanged")

def test_edge_cases():
    """Test edge cases."""
    print("\nTesting edge cases...")
    
    # Empty parameters
    result1 = normalize_tool_parameters("read_file", {})
    assert result1 == {}, "Expected empty dict for empty params"
    print("✓ Empty parameters handled")
    
    # Parameters with None values
    params2 = {
        "file_path": None,
        "offset": 100
    }
    result2 = normalize_tool_parameters("read_file", params2)
    assert result2 == {"path": None}, f"Expected {{'path': None}}, got {result2}"
    print("✓ None values preserved")

if __name__ == "__main__":
    print("=" * 60)
    print("Parameter Normalization Test Suite")
    print("=" * 60)
    
    try:
        test_read_file_normalization()
        test_write_to_file_normalization()
        test_apply_diff_normalization()
        test_unknown_tool()
        test_edge_cases()
        
        print("\n" + "=" * 60)
        print("✅ All tests passed!")
        print("=" * 60)
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)