#!/usr/bin/env python3
"""
Test script for WebSocket pipeline integration.

This script connects to the WebSocket endpoint and prints all progress updates
to verify the real pipeline is working correctly.
"""

import asyncio
import json
import websockets
from datetime import datetime


async def test_pipeline():
    """Test the pipeline WebSocket endpoint."""
    uri = "ws://localhost:8000/ws/generate/fitness-enthusiast"

    print(f"\n{'='*80}")
    print(f"🧪 Testing Fabric Dashboard Pipeline")
    print(f"{'='*80}\n")
    print(f"Connecting to: {uri}")
    print(f"Started at: {datetime.now().strftime('%H:%M:%S')}\n")

    try:
        async with websockets.connect(uri) as websocket:
            print("✓ WebSocket connected\n")
            print(f"{'='*80}")
            print("PROGRESS UPDATES:")
            print(f"{'='*80}\n")

            message_count = 0
            html_received = False

            while True:
                try:
                    # Receive message from server
                    message = await websocket.recv()
                    data = json.loads(message)
                    message_count += 1

                    msg_type = data.get('type')
                    step = data.get('step', '')
                    percent = data.get('percent', 0)
                    msg_text = data.get('message', '')

                    # Print progress update
                    if msg_type == 'progress':
                        print(f"[{percent:3d}%] {step:20s} | {msg_text}")

                        # Print additional data if present
                        if 'data' in data:
                            extra_data = data['data']
                            print(f"       └─ Data: {json.dumps(extra_data, indent=10)[:200]}...")
                            print()

                    elif msg_type == 'complete':
                        html = data.get('html', '')
                        persona = data.get('persona', '')
                        html_received = True

                        print(f"\n{'='*80}")
                        print(f"✅ GENERATION COMPLETE")
                        print(f"{'='*80}")
                        print(f"Persona: {persona}")
                        print(f"HTML Length: {len(html):,} characters")
                        print(f"HTML Preview: {html[:200]}...")
                        break

                    elif msg_type == 'error':
                        error_msg = data.get('message', 'Unknown error')
                        print(f"\n❌ ERROR: {error_msg}")
                        break

                except websockets.exceptions.ConnectionClosed:
                    print("\n🔌 Connection closed by server")
                    break

            # Summary
            print(f"\n{'='*80}")
            print(f"TEST SUMMARY")
            print(f"{'='*80}")
            print(f"Total messages received: {message_count}")
            print(f"HTML received: {'✓ Yes' if html_received else '✗ No'}")
            print(f"Ended at: {datetime.now().strftime('%H:%M:%S')}")

            if html_received:
                print(f"\n✅ Pipeline test PASSED - Real dashboard generated!")
            else:
                print(f"\n❌ Pipeline test FAILED - No HTML received")

            print(f"{'='*80}\n")

    except Exception as e:
        print(f"\n❌ Test failed with error:")
        print(f"   {type(e).__name__}: {e}")
        print(f"\nMake sure the backend is running:")
        print(f"   cd backend && uvicorn app.main:app --reload\n")


if __name__ == "__main__":
    asyncio.run(test_pipeline())
