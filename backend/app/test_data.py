"""
Mock data for testing all widget types.

This module provides complete mock data for all 7 widget types
to verify frontend rendering without running the full AI pipeline.
"""

from datetime import datetime
from fabric_dashboard.models.ui_components import (
    InfoCard,
    MapCard,
    MapMarker,
    VideoFeed,
    EventCalendar,
    TaskList,
    TaskItem,
    ContentCard,
)


def get_mock_ui_components() -> list:
    """
    Return a list of mock UI components covering all 7 widget types.

    Returns:
        List of UIComponent instances ready for dashboard_builder conversion
    """
    return [
        # 1. InfoCard - Weather widget
        InfoCard(
            title="San Francisco Weather",
            pattern_title="Local Explorer",
            confidence=0.85,
            location="San Francisco, CA",
            info_type="weather",
            units="imperial",
            show_forecast=True,
            enriched_data={
                "temperature": 72,
                "condition": "Sunny",
                "humidity": 65,
                "wind_speed": 8,
            }
        ),

        # 2. MapCard - Location markers
        MapCard(
            title="Favorite Coffee Shops",
            pattern_title="Urban Coffee Culture",
            confidence=0.90,
            center_lat=37.7749,
            center_lng=-122.4194,
            zoom=12,
            style="streets",
            markers=[
                MapMarker(
                    lat=37.7849,
                    lng=-122.4094,
                    title="Blue Bottle Coffee",
                    description="Artisanal coffee in Hayes Valley"
                ),
                MapMarker(
                    lat=37.7649,
                    lng=-122.4294,
                    title="Sightglass Coffee",
                    description="Specialty roaster in SoMa"
                ),
                MapMarker(
                    lat=37.7949,
                    lng=-122.4394,
                    title="Ritual Coffee",
                    description="Mission District favorite"
                ),
            ]
        ),

        # 3. VideoFeed - YouTube recommendations
        VideoFeed(
            title="Tech Talks You'll Love",
            pattern_title="Tech Learner",
            confidence=0.88,
            search_query="machine learning tutorials",
            max_results=3,
            video_duration="medium",
            order_by="relevance",
            enriched_videos=[
                {
                    "title": "Introduction to Neural Networks - Deep Learning Course",
                    "thumbnail": "https://i.ytimg.com/vi/aircaruvnKU/hqdefault.jpg",
                    "url": "https://youtube.com/watch?v=aircaruvnKU",
                    "duration": "15:24",
                },
                {
                    "title": "Building Your First Machine Learning Model with Python",
                    "thumbnail": "https://i.ytimg.com/vi/7eh4d6sabA0/hqdefault.jpg",
                    "url": "https://youtube.com/watch?v=7eh4d6sabA0",
                    "duration": "22:10",
                },
                {
                    "title": "Understanding Transformers - The Architecture Behind GPT",
                    "thumbnail": "https://i.ytimg.com/vi/SZorAJ4I-sA/hqdefault.jpg",
                    "url": "https://youtube.com/watch?v=SZorAJ4I-sA",
                    "duration": "18:45",
                },
            ]
        ),

        # 4. EventCalendar - Upcoming events
        EventCalendar(
            title="Events Near You",
            pattern_title="Community Networker",
            confidence=0.82,
            search_query="tech conferences san francisco",
            location="San Francisco, CA",
            max_results=4,
            date_range="30",
            enriched_events=[
                {
                    "name": "AI & Machine Learning Summit 2025",
                    "date": "2025-11-15T09:00:00Z",
                    "venue": {
                        "name": "Moscone Center",
                        "city": "San Francisco"
                    },
                    "url": "https://ticketmaster.com/event/1234",
                },
                {
                    "name": "React Developer Conference",
                    "date": "2025-11-20T10:30:00Z",
                    "venue": {
                        "name": "Palace of Fine Arts",
                        "city": "San Francisco"
                    },
                    "url": "https://ticketmaster.com/event/5678",
                },
                {
                    "name": "Startup Founder Networking Night",
                    "date": "2025-11-22T18:00:00Z",
                    "venue": {
                        "name": "WeWork SoMa",
                        "city": "San Francisco"
                    },
                    "url": "https://ticketmaster.com/event/9012",
                },
            ]
        ),

        # 5. TaskList - To-do items
        TaskList(
            title="Today's Focus",
            pattern_title="Organized Achiever",
            confidence=0.87,
            tasks=[
                TaskItem(text="Review pull requests for dashboard redesign", priority="high"),
                TaskItem(text="Schedule 1:1 with design team", priority="medium"),
                TaskItem(text="Finish quarterly planning document", priority="high"),
                TaskItem(text="Test new widget components", priority="medium"),
                TaskItem(text="Update project roadmap", priority="low"),
            ]
        ),

        # 6. ContentCard - Article recommendation
        ContentCard(
            title="Deep Dive Resource",
            pattern_title="Tech Innovator",
            confidence=0.92,
            article_title="The Future of Human-AI Collaboration in Software Development",
            overview="An in-depth exploration of how AI coding assistants are transforming software development workflows, featuring interviews with leading engineers and analysis of productivity metrics across major tech companies.",
            url="https://perplexity.ai/article/ai-development-future",
            source_name="Tech Review Quarterly",
            published_date="2025-10-15",
            search_query="future of AI in software development",
        ),

        # 7. Another ContentCard for variety (different topic)
        ContentCard(
            title="Design Insights",
            pattern_title="Creative Professional",
            confidence=0.88,
            article_title="Principles of Generative UI Design: Creating Dynamic Interfaces",
            overview="Exploring the intersection of AI and interface design, this article examines how generative systems can create personalized user experiences while maintaining usability and accessibility standards.",
            url="https://perplexity.ai/article/generative-ui-design",
            source_name="Design Systems Journal",
            published_date="2025-10-20",
            search_query="generative UI design principles",
        ),
    ]


def get_mock_persona():
    """Return a mock persona profile for testing."""
    return {
        "writing_style": "analytical and data-driven with clear structure",
        "interests": ["technology", "artificial intelligence", "design"],
        "activity_level": "high",
        "professional_context": "tech startup founder",
        "tone_preference": "balanced and professional",
        "age_range": "30-40",
        "content_depth_preference": "deep_dives",
    }


def get_mock_color_scheme():
    """Return a mock color scheme for testing."""
    return {
        "primary": "#3B82F6",
        "secondary": "#8B5CF6",
        "accent": "#F59E0B",
        "foreground": "#1F2937",
        "muted": "#6B7280",
        "success": "#10B981",
        "warning": "#F59E0B",
        "destructive": "#EF4444",
        "background_theme": {
            "type": "gradient",
            "gradient": {
                "type": "linear",
                "colors": ["#1e3a8a", "#7c3aed", "#db2777"],
                "direction": "135deg"
            },
            "card_background": "#FFFFFF",
            "card_backdrop_blur": True,
        },
        "fonts": {
            "heading": "Inter",
            "body": "Inter",
            "mono": "Fira Code",
            "heading_url": "https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap",
            "body_url": "https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap",
            "mono_url": "https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&display=swap",
        },
        "mood": "professional",
        "rationale": "Tech-inspired blue with creative purple accent for an innovative feel",
    }
