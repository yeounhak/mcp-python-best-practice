from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

# ===============================
# MASKED SERVER (mask_error_details=True)
# ===============================
mcp_masked = FastMCP(name="MaskedServer", mask_error_details=True)

@mcp_masked.tool
def test_toolerror_masked() -> str:
    """Test ToolError with masking enabled."""
    raise ToolError("ToolError message from MASKED server")

@mcp_masked.tool
def test_standard_exception_masked() -> str:
    """Test standard exception with masking enabled."""
    raise ValueError("Standard exception from MASKED server - should be hidden!")

@mcp_masked.tool  
def test_input_validation_masked(number: int) -> str:
    """Test input validation with masking enabled."""
    return f"Valid number received by MASKED server: {number}"

# ===============================
# UNMASKED SERVER (mask_error_details=False)
# ===============================
mcp_unmasked = FastMCP(name="UnmaskedServer", mask_error_details=False)

@mcp_unmasked.tool
def test_toolerror_unmasked() -> str:
    """Test ToolError with masking disabled."""
    raise ToolError("ToolError message from UNMASKED server")

@mcp_unmasked.tool
def test_standard_exception_unmasked() -> str:
    """Test standard exception with masking disabled."""
    raise ValueError("Standard exception from UNMASKED server - should be visible!")

@mcp_unmasked.tool  
def test_input_validation_unmasked(number: int) -> str:
    """Test input validation with masking disabled."""
    return f"Valid number received by UNMASKED server: {number}"

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "unmasked":
        print("🔓 Starting UNMASKED server on port 8001...")
        mcp_unmasked.run(transport='http', port=8001)
    else:
        print("🔒 Starting MASKED server on port 8000...")
        mcp_masked.run(transport='http', port=8000)