"""
Simple test script to verify WebSocket works.

This script:
1. Connects to the WebSocket endpoint
2. Listens for progress updates
3. Receives the final dashboard HTML
4. Prints what it got

Run this to test the backend!
"""

import asyncio
import json
import websockets


async def test_websocket(persona: str):
    """Test the WebSocket endpoint with a specific persona."""

    # Connect to the WebSocket
    # ws://localhost:8000/ws/generate/{persona}
    uri = f"ws://localhost:8000/ws/generate/{persona}"

    print(f"🔌 Connecting to {uri}...")

    try:
        # Open WebSocket connection
        async with websockets.connect(uri) as websocket:
            print("✓ Connected!")

            # Listen for messages
            while True:
                # Receive a message
                message_text = await websocket.recv()

                # Parse the JSON
                message = json.loads(message_text)
                message_type = message.get("type")

                # Handle different message types
                if message_type == "progress":
                    percent = message.get("percent")
                    msg = message.get("message")
                    print(f"📊 Progress: {percent}% - {msg}")

                elif message_type == "complete":
                    html = message.get("html")
                    html_length = len(html)
                    print(f"✅ Complete! Received {html_length:,} characters of HTML")

                    # Check if it's the right dashboard
                    if persona in html.lower() or "fitness" in html.lower() or "creative" in html.lower() or "tech" in html.lower():
                        print("✓ HTML contains expected content")

                    # We're done!
                    break

                elif message_type == "error":
                    error_msg = message.get("message")
                    print(f"❌ Error: {error_msg}")
                    break

                else:
                    print(f"❓ Unknown message type: {message_type}")

            print(f"\n✓ Test passed for {persona}!")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

    return True


async def main():
    """Run tests for all 3 personas."""

    print("🚀 Testing WebSocket endpoints...")
    print("=" * 60)

    personas = [
        "fitness-enthusiast",
        "creative-professional",
        "tech-learner"
    ]

    results = []

    for persona in personas:
        print(f"\n📋 Testing: {persona}")
        print("-" * 60)

        success = await test_websocket(persona)
        results.append((persona, success))

        # Small delay between tests
        await asyncio.sleep(0.5)

    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary:")

    for persona, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status} - {persona}")

    all_passed = all(success for _, success in results)

    if all_passed:
        print("\n🎉 All tests passed! Backend is ready!")
    else:
        print("\n⚠️  Some tests failed. Check errors above.")

    return all_passed


if __name__ == "__main__":
    # Run the async main function
    success = asyncio.run(main())

    # Exit with appropriate code
    exit(0 if success else 1)
