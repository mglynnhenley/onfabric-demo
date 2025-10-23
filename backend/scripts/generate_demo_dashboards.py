"""
Generate demo dashboards for the interactive demo.

SIMPLIFIED VERSION FOR DEMO:
Instead of using the complex pipeline, we create simple but beautiful HTML
directly. This is easier to understand and maintain for the demo.

Why simplified?
- No Claude API calls needed (saves $)
- No complex pipeline debugging
- Instant generation
- Still looks great!
"""

from pathlib import Path


# Our 3 demo personas with their colors and content
DEMO_DASHBOARDS = {
    "fitness-enthusiast": {
        "title": "Your Fitness Journey",
        "subtitle": "Personal Trainer & Wellness Coach",
        "color": "#10b981",  # Green
        "gradient_from": "#10b981",
        "gradient_to": "#059669",
        "cards": [
            {
                "title": "Morning Workout Routine",
                "content": "You're crushing it with consistent 6 AM gym sessions! Your dedication to strength training and cardio is paying off - keep that energy up!",
                "icon": "💪"
            },
            {
                "title": "Nutrition Tracking",
                "content": "Your meal planning game is strong. High protein focus and macro tracking shows you're serious about fueling your body right.",
                "icon": "🥗"
            },
            {
                "title": "Marathon Training",
                "content": "30 miles per week - you're absolutely ready for that marathon! Your consistency is what separates dreamers from achievers.",
                "icon": "🏃"
            }
        ]
    },

    "creative-professional": {
        "title": "Your Creative Journey",
        "subtitle": "Designer & Content Creator",
        "color": "#8b5cf6",  # Purple
        "gradient_from": "#8b5cf6",
        "gradient_to": "#7c3aed",
        "cards": [
            {
                "title": "Design Mastery",
                "content": "Your daily Figma and Adobe Creative Suite work shows true dedication to craft. Those client projects are looking 🔥",
                "icon": "🎨"
            },
            {
                "title": "Visual Inspiration",
                "content": "Love how you curate inspiration from Dribbble, Behance, and Pinterest. Your aesthetic sense is evolving beautifully!",
                "icon": "✨"
            },
            {
                "title": "Photography Portfolio",
                "content": "Those weekend photography sessions are building something special. Your portfolio diversity is impressive!",
                "icon": "📸"
            }
        ]
    },

    "tech-learner": {
        "title": "Your Learning Journey",
        "subtitle": "Software Engineer & Lifelong Learner",
        "color": "#3b82f6",  # Blue
        "gradient_from": "#3b82f6",
        "gradient_to": "#2563eb",
        "cards": [
            {
                "title": "Daily Coding Practice",
                "content": "Those daily GitHub commits don't lie - you're building real skills. Side projects are where the magic happens!",
                "icon": "💻"
            },
            {
                "title": "Tech Community",
                "content": "Active on HackerNews and dev communities - you're staying on the cutting edge. Keep learning, keep shipping!",
                "icon": "🚀"
            },
            {
                "title": "AI Experiments",
                "content": "Building with Claude and GPT-4? You're riding the AI wave. These experiments today become products tomorrow.",
                "icon": "🤖"
            }
        ]
    }
}


def generate_html(persona_key: str, data: dict) -> str:
    """
    Generate a beautiful HTML dashboard.

    This is a simplified version that doesn't need the full pipeline.
    Perfect for the demo!
    """

    # Build the cards HTML
    cards_html = ""
    for card in data["cards"]:
        cards_html += f"""
        <div class="card">
            <div class="card-icon">{card['icon']}</div>
            <h3>{card['title']}</h3>
            <p>{card['content']}</p>
        </div>
        """

    # Complete HTML template
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{data['title']} - Fabric Dashboard</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}

            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                background: linear-gradient(135deg, {data['gradient_from']} 0%, {data['gradient_to']} 100%);
                min-height: 100vh;
                padding: 40px 20px;
                color: #333;
            }}

            .container {{
                max-width: 1200px;
                margin: 0 auto;
            }}

            .header {{
                text-align: center;
                color: white;
                margin-bottom: 50px;
            }}

            .header h1 {{
                font-size: 48px;
                font-weight: 700;
                margin-bottom: 10px;
                text-shadow: 0 2px 10px rgba(0,0,0,0.2);
            }}

            .header p {{
                font-size: 20px;
                opacity: 0.95;
                font-weight: 500;
            }}

            .cards-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 30px;
                margin-top: 40px;
            }}

            .card {{
                background: white;
                border-radius: 20px;
                padding: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.15);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }}

            .card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 15px 40px rgba(0,0,0,0.2);
            }}

            .card-icon {{
                font-size: 48px;
                margin-bottom: 15px;
            }}

            .card h3 {{
                font-size: 24px;
                margin-bottom: 15px;
                color: {data['color']};
            }}

            .card p {{
                font-size: 16px;
                line-height: 1.6;
                color: #666;
            }}

            .footer {{
                text-align: center;
                margin-top: 60px;
                padding: 30px;
                background: rgba(255,255,255,0.1);
                border-radius: 20px;
                color: white;
            }}

            .footer p {{
                margin: 5px 0;
                opacity: 0.9;
            }}

            @media (max-width: 768px) {{
                .header h1 {{
                    font-size: 32px;
                }}

                .cards-grid {{
                    grid-template-columns: 1fr;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>{data['title']}</h1>
                <p>{data['subtitle']}</p>
            </div>

            <div class="cards-grid">
                {cards_html}
            </div>

            <div class="footer">
                <p><strong>Generated with Fabric Intelligence Dashboard</strong></p>
                <p>Powered by AI • Personalized for You</p>
            </div>
        </div>
    </body>
    </html>
    """

    return html


def main():
    """
    Generate all 3 demo dashboards.

    This is super simple:
    1. Loop through our 3 personas
    2. Generate HTML for each
    3. Save to files

    That's it! No complex pipeline needed for the demo.
    """
    print("🚀 Starting demo dashboard generation...")
    print("=" * 60)

    # Create output directory
    output_dir = Path(__file__).parent.parent / "dashboards"
    output_dir.mkdir(exist_ok=True)
    print(f"📁 Output directory: {output_dir}")

    # Generate each dashboard
    for persona_key, data in DEMO_DASHBOARDS.items():
        print(f"\n🎨 Generating {data['title']}...")

        try:
            # Generate HTML
            html = generate_html(persona_key, data)

            # Save to file
            output_file = output_dir / f"{persona_key}.html"
            output_file.write_text(html)

            print(f"  ✓ Saved to {output_file.name} ({len(html):,} characters)")

        except Exception as e:
            print(f"  ❌ Error: {e}")
            continue

    print("\n" + "=" * 60)
    print("✅ Demo dashboard generation complete!")
    print(f"📊 Generated {len(DEMO_DASHBOARDS)} dashboards")
    print(f"📂 Location: {output_dir}")
    print("\nYou can now open these HTML files in a browser to see them!")


if __name__ == "__main__":
    main()
