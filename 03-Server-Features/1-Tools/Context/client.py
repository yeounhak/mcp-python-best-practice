from fastmcp import Client
import asyncio

async def test_context_features():
    """Test all Context features provided by the server."""
    
    async with Client("http://localhost:8000/mcp") as client:
        print("🧪 FastMCP Context Features Demo")
        print("=" * 60)
        
        # Test 1: Logging demonstration
        print("\n1️⃣ Testing Logging Features")
        print("-" * 40)
        try:
            result = await client.call_tool("demonstrate_logging", {
                "message": "Hello from client!"
            })
            print(f"✅ Result: {result.get('message')}")
            print(f"📝 Request Info: {result.get('request_info')}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test 2: Progress reporting
        print("\n2️⃣ Testing Progress Reporting")
        print("-" * 40)
        try:
            result = await client.call_tool("process_with_progress", {
                "task_name": "Data Processing Demo",
                "steps": 5
            })
            print(f"✅ Task: {result.get('task_name')}")
            print(f"📊 Status: {result.get('status')}")
            print(f"📈 Steps completed: {result.get('total_steps')}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test 3: LLM Sampling
        print("\n3️⃣ Testing LLM Sampling")
        print("-" * 40)
        test_data = """
        FastMCP is a powerful Python framework for building Model Control Protocol (MCP) servers.
        It provides easy-to-use decorators for creating tools, resources, and prompts.
        The Context object enables servers to access logging, progress reporting, and LLM sampling capabilities.
        This makes it ideal for building intelligent automation tools and AI-powered applications.
        """
        
        # Test different analysis types
        analysis_types = ["summary", "sentiment", "keywords"]
        
        for analysis_type in analysis_types:
            try:
                result = await client.call_tool("analyze_data_with_llm", {
                    "data": test_data,
                    "analysis_type": analysis_type
                })
                print(f"📊 {analysis_type.upper()} Analysis:")
                print(f"   Status: {result.get('status')}")
                if result.get('status') == 'success':
                    print(f"   Result: {result.get('analysis_result')}")
                else:
                    print(f"   Error: {result.get('error')}")
                print()
            except Exception as e:
                print(f"❌ {analysis_type} analysis failed: {e}")
        
        # Test 4: Resource reading (will likely fail as demo)
        print("\n4️⃣ Testing Resource Reading")
        print("-" * 40)
        try:
            result = await client.call_tool("read_and_process_resource", {
                "resource_uri": "file:///tmp/demo.txt"
            })
            print(f"📁 Resource URI: {result.get('resource_uri')}")
            print(f"📊 Status: {result.get('status')}")
            if result.get('status') == 'success':
                print(f"📝 Content preview: {result.get('content_preview')}")
                print(f"📊 Word count: {result.get('word_count')}")
            else:
                print(f"⚠️  Expected result: {result.get('status')} - {result.get('error', 'Resource not found')}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test 5: Comprehensive demo
        print("\n5️⃣ Testing Comprehensive Context Demo")
        print("-" * 40)
        try:
            demo_text = """
            Context objects in FastMCP provide servers with powerful capabilities including
            structured logging, progress reporting, resource access, and LLM sampling.
            This enables building sophisticated AI-powered tools that can interact with
            clients, process data, and provide intelligent insights.
            """
            
            result = await client.call_tool("comprehensive_demo", {
                "input_text": demo_text
            })
            
            print(f"✅ Demo Status: {result.get('demo_status')}")
            print(f"⏱️  Processing Time: {result.get('processed_data', {}).get('processing_time', 'N/A'):.2f}s")
            print(f"📝 Summary: {result.get('processed_data', {}).get('summary', 'N/A')}")
            print(f"🔧 Features Used: {', '.join(result.get('context_features_used', []))}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print(f"\n{'='*60}")
        print("📊 Context Features Test Summary:")
        print("✅ Logging: Debug, Info, Warning, Error levels")
        print("✅ Progress: Real-time progress reporting")
        print("✅ LLM Sampling: Text analysis and processing")
        print("✅ Resource Access: File and URI reading")
        print("✅ Request Info: Client and request identification")
        print(f"{'='*60}")

async def interactive_demo():
    """Interactive demonstration allowing user input."""
    
    print("\n🎮 Interactive Context Demo")
    print("Enter text to analyze, or 'quit' to exit:")
    
    async with Client("http://localhost:8000/mcp") as client:
        while True:
            user_input = input("\n📝 Enter text: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                print("⚠️  Please enter some text to analyze.")
                continue
            
            try:
                print("\n🔄 Processing...")
                result = await client.call_tool("comprehensive_demo", {
                    "input_text": user_input
                })
                
                print(f"\n✅ Analysis Complete!")
                print(f"📝 Summary: {result.get('processed_data', {}).get('summary', 'N/A')}")
                print(f"📊 Word Count: {result.get('processed_data', {}).get('word_count', 'N/A')}")
                print(f"⏱️  Processing Time: {result.get('processed_data', {}).get('processing_time', 'N/A'):.2f}s")
                
            except Exception as e:
                print(f"❌ Error: {e}")

async def main():
    """Main function to run Context feature tests."""
    try:
        # Run automated tests
        await test_context_features()
        
        # Ask if user wants interactive demo
        response = input("\n🎮 Would you like to try the interactive demo? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            await interactive_demo()
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        print("💡 Make sure the server is running: python server.py")

if __name__ == '__main__':
    asyncio.run(main())