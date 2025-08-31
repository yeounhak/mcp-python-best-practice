from fastmcp import Client
import asyncio

async def test_error_type(error_type: str, masked_client: Client, unmasked_client: Client):
    """Test a specific error type on both masked and unmasked servers."""
    
    print(f"\n{'='*60}")
    print(f"🧪 Testing {error_type}")
    print(f"{'='*60}")
    
    # Test on masked server
    print(f"\n🔒 MASKED Server (mask_error_details=True):")
    print("-" * 50)
    try:
        if error_type == "ToolError":
            await masked_client.call_tool("test_toolerror_masked")
        elif error_type == "Standard Exception":
            await masked_client.call_tool("test_standard_exception_masked")
        elif error_type == "Input Validation":
            await masked_client.call_tool("test_input_validation_masked", {"number": "invalid"})
    except Exception as e:
        print(f"❌ MASKED: {e}")
    
    # Test on unmasked server
    print(f"\n🔓 UNMASKED Server (mask_error_details=False):")
    print("-" * 50)
    try:
        if error_type == "ToolError":
            await unmasked_client.call_tool("test_toolerror_unmasked")
        elif error_type == "Standard Exception":
            await unmasked_client.call_tool("test_standard_exception_unmasked")
        elif error_type == "Input Validation":
            await unmasked_client.call_tool("test_input_validation_unmasked", {"number": "invalid"})
    except Exception as e:
        print(f"❌ UNMASKED: {e}")

async def compare_all_error_patterns():
    """Compare all 3 error patterns across masked vs unmasked servers."""
    
    print("🛡️ FastMCP Error Handling: Masked vs Unmasked Comparison")
    print("=" * 60)
    print("Testing 6 scenarios: 3 error types × 2 masking modes")
    
    # Connect to both servers
    try:
        async with Client("http://localhost:8000/mcp") as masked_client:
            try:
                async with Client("http://localhost:8001/mcp") as unmasked_client:
                    
                    # Test 1: ToolError on both servers
                    await test_error_type("ToolError", masked_client, unmasked_client)
                    
                    # Test 2: Standard Exception on both servers  
                    await test_error_type("Standard Exception", masked_client, unmasked_client)
                    
                    # Test 3: Input Validation on both servers
                    await test_error_type("Input Validation", masked_client, unmasked_client)
                    
                    # Summary
                    print(f"\n{'='*60}")
                    print("📊 COMPARISON SUMMARY")
                    print(f"{'='*60}")
                    print("1️⃣ ToolError: Should be IDENTICAL on both servers")
                    print("2️⃣ Standard Exception: Should be DIFFERENT (masked vs detailed)")  
                    print("3️⃣ Input Validation: Should be IDENTICAL on both servers")
                    print(f"{'='*60}")
                    
            except Exception as e:
                print(f"\n❌ Cannot connect to UNMASKED server (port 8001): {e}")
                print("💡 Start unmasked server with: python server.py unmasked")
                
    except Exception as e:
        print(f"\n❌ Cannot connect to MASKED server (port 8000): {e}")
        print("💡 Start masked server with: python server.py")

async def main():
    """Main function for comprehensive error handling comparison."""
    await compare_all_error_patterns()

if __name__ == '__main__':
    asyncio.run(main())