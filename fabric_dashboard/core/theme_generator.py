"""Theme generation module using Claude for persona-matched color schemes."""

from typing import Optional

from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from tenacity import retry, stop_after_attempt, wait_exponential

from fabric_dashboard.models.schemas import (
    AnimationConfig,
    BackgroundTheme,
    ColorScheme,
    FontScheme,
    GradientConfig,
    Pattern,
    PatternConfig,
    PersonaProfile,
)
from fabric_dashboard.utils import logger
from fabric_dashboard.utils.config import get_config


class ThemeGenerator:
    """Generates persona-matched color schemes using Claude."""

    def __init__(self, mock_mode: bool = False):
        """
        Initialize theme generator.

        Args:
            mock_mode: If True, use default theme instead of real LLM calls.
        """
        self.mock_mode = mock_mode
        self.llm: Optional[ChatAnthropic] = None

        if not mock_mode:
            config = get_config()
            if not config:
                raise RuntimeError("Configuration not found. Run 'fabric-dashboard init' first.")

            self.llm = ChatAnthropic(
                model_name="claude-sonnet-4-5",
                temperature=1.0,  # High temperature for funky, creative color schemes
                api_key=config.anthropic_api_key,
                timeout=30,
                max_tokens=2048,
                stop=None,
            )

    def generate_theme(
        self, persona: PersonaProfile, patterns: list[Pattern]
    ) -> ColorScheme:
        """
        Generate a color scheme based on persona and patterns.

        Args:
            persona: User's persona profile.
            patterns: Detected patterns (used for theme inspiration).

        Returns:
            ColorScheme with persona-matched colors.
        """
        if self.mock_mode:
            return self._default_theme()
        else:
            return self._generate_with_claude(persona, patterns)

    def _default_theme(self) -> ColorScheme:
        """
        Return a funky cyberpunk/vaporwave theme for demos.

        Returns:
            ColorScheme with bold, vibrant colors and glass morphism.
        """
        logger.info("Using funky demo theme (Neon Sunset)")

        return ColorScheme(
            # Primary palette - vibrant neons
            primary="#ff6ec7",  # Neon pink
            secondary="#00f5ff",  # Cyan neon
            accent="#b759ff",  # Purple neon
            # Text - light for dark background
            foreground="#f8fafc",  # Almost white
            muted="#cbd5e1",  # Light gray
            # Semantic colors
            success="#00ff9f",  # Neon green
            warning="#ffb800",  # Golden yellow
            destructive="#ff2e63",  # Hot pink red
            # Background theming - dark gradient with glass cards
            background_theme=BackgroundTheme(
                type="gradient",
                gradient=GradientConfig(
                    type="mesh",
                    colors=["#0f0f23", "#1a0b2e", "#2d1b69", "#1e3a8a"],
                    direction="to-br",
                ),
                card_background="rgba(15, 15, 35, 0.7)",  # Dark glass
                card_backdrop_blur=True,
            ),
            # Typography - distinctive cyberpunk fonts
            fonts=FontScheme(
                heading="Orbitron",
                body="Rajdhani",
                mono="JetBrains Mono",
                heading_url="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap",
                body_url="https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600&display=swap",
                mono_url="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap",
            ),
            # Metadata
            mood="Neon Sunset",
            rationale="Vibrant cyberpunk aesthetic with neon colors, dark gradient mesh background, and glass morphism cards for a futuristic, eye-catching demo experience",
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True,
    )
    def _generate_with_claude(
        self, persona: PersonaProfile, patterns: list[Pattern]
    ) -> ColorScheme:
        """
        Generate theme using Claude API with retry logic.

        Args:
            persona: User's persona profile.
            patterns: Detected patterns.

        Returns:
            ColorScheme with generated colors.

        Raises:
            RuntimeError: If generation fails after retries.
        """
        if not self.llm:
            raise RuntimeError("LLM not initialized")

        logger.info("Generating color theme with Claude")

        try:
            # Build prompt template
            prompt = self._build_prompt()

            # Prepare context
            context = self._prepare_context(persona, patterns)

            # Create structured LLM using with_structured_output()
            structured_llm = self.llm.with_structured_output(ColorScheme)

            # Create chain: prompt -> structured LLM
            chain = prompt | structured_llm

            # Execute chain
            result = chain.invoke({
                "context": context,
            })

            # Validate and fix contrast issues
            result = self._ensure_readable_contrast(result)

            logger.success(f"Generated theme with mood: {result.mood}")
            return result

        except Exception as e:
            logger.error(f"Theme generation failed: {e}")
            # Fallback to default theme
            logger.warning("Falling back to default theme")
            return self._default_theme()

    def _build_prompt(self) -> ChatPromptTemplate:
        """
        Build the prompt template for theme generation.

        Returns:
            ChatPromptTemplate for theme generation.
        """
        system_message = """You are an expert UI/UX designer and color theorist specializing in personalized design.

Your task is to create a cohesive, persona-matched color scheme AND typography for a personalized dashboard.

## Guidelines for Color Selection:

**Primary Palette:**
- **Primary**: Main brand/accent color that reflects the persona's vibe
- **Secondary**: Supporting color that complements primary
- **Accent**: Highlight color for CTAs and important elements

**Text (CRITICAL FOR READABILITY):**
- **Foreground**: Primary text color
  - MUST have 4.5:1 contrast ratio minimum with BOTH background AND card_background
  - If background is dark (gradient starting with dark colors, or dark solid), foreground MUST be light (#f8fafc or similar)
  - If background is light, foreground MUST be dark (#0f172a or similar)
  - When card_backdrop_blur is true, assume background color bleeds through cards by ~50%
- **Muted**: Secondary/muted text color (should be readable but less prominent)

**Semantic Colors:**
- **Success**: Green-ish color for success states
- **Warning**: Yellow/orange-ish color for warnings
- **Destructive**: Red-ish color for errors/destructive actions

**Background Theming (background_theme object):**
- **type**: Choose one: "solid", "gradient", "pattern"
- **color**: (if type="solid") Solid background color hex
- **gradient**: (if type="gradient") Object with:
  - type: "linear", "radial", or "mesh"
  - colors: Array of 2-4 hex colors for gradient
  - direction: "to-br", "to-r", "to-t", etc. (optional)
- **pattern**: (if type="pattern") - RARELY use this, only for very creative personas
- **card_background**: Card background color or rgba (e.g., "rgba(255, 255, 255, 0.7)" for glass effect)
- **card_backdrop_blur**: true/false - enable glass morphism effect

**Typography (fonts object):**
- **heading**: Font family for headings (e.g., "EB Garamond", "Playfair Display", "Libre Baskerville")
- **body**: Font family for body text (e.g., "Manrope", "Inter", "Source Sans Pro")
- **mono**: Font family for code (e.g., "IBM Plex Mono", "Fira Code", "JetBrains Mono")
- **heading_url**: Google Fonts URL for heading font
- **body_url**: Google Fonts URL for body font
- **mono_url**: Google Fonts URL for mono font

Example Google Fonts URLs:
- "https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;600;700&display=swap"
- "https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600&display=swap"

**Pattern Overlay (pattern object - OPTIONAL):**
- **type**: Choose one: "dots", "grid", "stripes", "noise", "waves", "hexagon"
- **color**: Pattern color (hex)
- **opacity**: 0.05-0.15 for subtle, 0.2-0.4 for bold (float)
- **scale**: 0.5-2.0 (pattern size multiplier)
- Use patterns for creative/experimental personas, skip for minimal/professional

**Animation (animation object - OPTIONAL):**
- **name**: Choose from: "float", "pulse", "drift", "wave", "rotate-slow", "gradient-shift", "glitch", "breathe", "shimmer", "none"
- **duration**: "15s" to "30s" (slow is better for backgrounds)
- **timing**: "ease-in-out" or "linear"
- Match animation to aesthetic: glitch for cyber, float for organic, pulse for minimal, none for brutalist

**Metadata:**
- **Mood**: Single word or short phrase describing the emotional feel (e.g., "energetic", "calm", "professional", "creative", "bold")
- **Rationale**: 1-2 sentences explaining why these colors AND fonts match the persona

## CRITICAL: ANTI-GENERIC AESTHETIC RULES

You MUST avoid generic AI aesthetics. Every dashboard should look radically different and distinctive.

**BANNED FONTS (DO NOT USE THESE EVER):**
- Inter, Roboto, Arial, Helvetica, system fonts
- Open Sans, Lato, Montserrat, Poppins
- Space Grotesk (overused)

**BANNED COLOR PATTERNS:**
- Generic purple gradients (#7c3aed, #8b5cf6)
- Generic blues (#3b82f6)
- Purple gradient on white background (extremely clichéd)

**REQUIRED APPROACH:**
- Choose fonts that are DISTINCTIVE, UNUSUAL, and MEMORABLE
- Choose colors that are BOLD, UNEXPECTED, and contextual to the persona
- Generate multi-layer backgrounds (gradient + optional pattern + optional animation)
- Vary between aesthetic directions based on persona

**Aesthetic Direction Examples (pick ONE that matches persona):**

**80s/90s Vaporwave:**
- Fonts: Orbitron, Rajdhani, Synth, Audiowide
- Colors: Neon pink (#ff6ec7), cyan (#00f5ff), purple (#b759ff), dark navy base
- Pattern: grid or waves
- Animation: gradient-shift or glitch

**Y2K Cyber Futurism:**
- Fonts: Exo, Audiowide, Electrolize, Orbitron
- Colors: Metallic silver tones, electric blue, holographic gradients
- Pattern: hexagon or geometric
- Animation: shimmer or rotate-slow

**Brutalist Bold:**
- Fonts: Rubik, Bebas Neue, Staatliches, Work Sans
- Colors: Stark contrasts (pure black/white, or bold single color + black)
- Pattern: grid (bold opacity 0.3-0.5)
- Animation: none or pulse

**Organic Psychedelic:**
- Fonts: Righteous, Bungee, Fredoka One, Comfortaa
- Colors: Warped multi-color gradients (4 colors), high saturation
- Pattern: noise or waves
- Animation: wave or drift

**Elegant Serif:**
- Fonts: Cormorant Garamond, Crimson Text, Libre Baskerville, Lora
- Colors: Deep jewel tones, sophisticated muted palette
- Pattern: dots (very subtle, 0.05 opacity)
- Animation: float or breathe

**IMPORTANT: Pick fonts and colors that FIT THE PERSONA. Don't always use the same combinations. Be experimental and creative.**

## Color Selection Strategy:

1. **Analyze the persona's characteristics:**
   - Writing style (analytical vs creative vs provocative)
   - Interests and professional context
   - Activity level and tone preferences

2. **Match colors to personality:**
   - Analytical/professional → Blues, grays, teals
   - Creative/artistic → Purples, oranges, vibrant colors
   - Energetic/social → Warm colors, bright accents
   - Calm/thoughtful → Soft colors, pastels, earth tones
   - Bold/provocative → High contrast, saturated colors

3. **Ensure cohesion:**
   - All colors should work together harmoniously
   - Consider color psychology and emotional impact
   - Balance vibrancy with usability

4. **All colors must be valid 6-digit hex codes** (e.g., #3b82f6, not #3b8 or 3b82f6)

## CRITICAL VALIDATION REQUIREMENTS:

Before finalizing your color choices, verify:

1. **Contrast Ratio Check**:
   - Foreground vs background_theme.color (or first gradient color): MUST be ≥ 4.5:1
   - Foreground vs card_background: MUST be ≥ 4.5:1
   - If card_backdrop_blur is true, test foreground against a blend of background + card_background

2. **Dark Background Rule**:
   - If gradient starts with colors like #1e3a8a, #1e293b, #0f172a (dark blues/grays)
   - OR if solid background is dark (luminance < 0.5)
   - THEN foreground MUST be light: #f8fafc, #e2e8f0, #ffffff, etc.

3. **Light Background Rule**:
   - If gradient starts with colors like #fef3c7, #fce7f3, #ffffff (light yellows/pinks/whites)
   - OR if solid background is light (luminance > 0.5)
   - THEN foreground MUST be dark: #0f172a, #1e293b, #334155, etc.

4. **Backdrop Blur Warning**:
   - When card_backdrop_blur is true, the background gradient will show through the card
   - This darkens light cards and lightens dark cards
   - Adjust card_background accordingly or disable backdrop blur

**These validation requirements are NOT optional. Text readability is the highest priority.**

Your response will be automatically validated against a Pydantic schema, so ensure all required fields are present and all hex codes are valid."""

        human_message = """Create a persona-matched color scheme based on this user profile:

{context}

Generate a cohesive color palette that reflects their personality and interests."""

        return ChatPromptTemplate.from_messages([
            ("system", system_message),
            ("human", human_message),
        ])

    def _prepare_context(
        self, persona: PersonaProfile, patterns: list[Pattern]
    ) -> str:
        """
        Prepare context for the LLM prompt.

        Args:
            persona: User's persona profile.
            patterns: Detected patterns.

        Returns:
            Formatted string with persona and pattern context.
        """
        context_parts = [
            "## Persona Profile",
            f"- Writing Style: {persona.writing_style}",
            f"- Tone Preference: {persona.tone_preference}",
            f"- Activity Level: {persona.activity_level}",
            f"- Interests: {', '.join(persona.interests)}",
        ]

        if persona.professional_context:
            context_parts.append(f"- Professional Context: {persona.professional_context}")

        if persona.age_range:
            context_parts.append(f"- Age Range: {persona.age_range}")

        context_parts.append(f"- Content Depth Preference: {persona.content_depth_preference}")

        # Add top patterns for inspiration
        context_parts.append("\n## Top Patterns (for inspiration)")
        for i, pattern in enumerate(patterns[:3], 1):  # Top 3 patterns
            context_parts.append(f"\n{i}. **{pattern.title}**")
            context_parts.append(f"   Keywords: {', '.join(pattern.keywords[:5])}")

        return "\n".join(context_parts)

    def _ensure_readable_contrast(self, scheme: ColorScheme) -> ColorScheme:
        """
        Validate and fix contrast ratios to ensure readability.

        WCAG AA requires 4.5:1 for normal text, 3:1 for large text.
        We'll use 4.5:1 as the minimum.

        Args:
            scheme: Generated color scheme

        Returns:
            ColorScheme with validated/fixed contrast ratios
        """
        # Get background color for contrast checking
        bg_color = scheme.background_theme.color or "#ffffff"
        if scheme.background_theme.type == "gradient" and scheme.background_theme.gradient:
            # Use first color of gradient for contrast check
            bg_color = scheme.background_theme.gradient.colors[0]

        # Check foreground vs background
        fg_bg_contrast = self._calculate_contrast(scheme.foreground, bg_color)
        if fg_bg_contrast < 4.5:
            logger.warning(f"Low contrast detected: foreground/background = {fg_bg_contrast:.2f}:1")
            # Adjust foreground to be darker if background is light, or lighter if background is dark
            if self._get_luminance(bg_color) > 0.5:
                # Light background - make foreground darker
                scheme.foreground = "#0f172a"  # Dark slate
            else:
                # Dark background - make foreground lighter
                scheme.foreground = "#f8fafc"  # Light gray
            logger.info(f"Fixed foreground color to {scheme.foreground}")

        # Check foreground vs card background
        # Extract hex color from rgba if needed
        card_bg = scheme.background_theme.card_background
        if card_bg.startswith("rgba"):
            # For rgba, assume white or light background for now
            card_bg = "#ffffff"

        fg_card_contrast = self._calculate_contrast(scheme.foreground, card_bg)
        if fg_card_contrast < 4.5:
            logger.warning(f"Low contrast detected: foreground/card = {fg_card_contrast:.2f}:1")
            # Adjust card background to have better contrast with foreground
            if self._get_luminance(scheme.foreground) > 0.5:
                # Light foreground - make card darker
                scheme.background_theme.card_background = "#1e293b"  # Dark slate
            else:
                # Dark foreground - make card lighter
                scheme.background_theme.card_background = "#ffffff"  # White
            logger.info(f"Fixed card background to {scheme.background_theme.card_background}")

        return scheme

    def _get_luminance(self, hex_color: str) -> float:
        """
        Calculate relative luminance of a color.

        Formula from WCAG: https://www.w3.org/TR/WCAG20/#relativeluminancedef

        Args:
            hex_color: Hex color string (e.g., "#3b82f6")

        Returns:
            Relative luminance (0-1)
        """
        # Remove # if present
        hex_color = hex_color.lstrip("#")

        # Convert to RGB
        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0
        b = int(hex_color[4:6], 16) / 255.0

        # Apply gamma correction
        def gamma_correct(c: float) -> float:
            if c <= 0.03928:
                return c / 12.92
            else:
                return ((c + 0.055) / 1.055) ** 2.4

        r = gamma_correct(r)
        g = gamma_correct(g)
        b = gamma_correct(b)

        # Calculate luminance
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    def _calculate_contrast(self, color1: str, color2: str) -> float:
        """
        Calculate contrast ratio between two colors.

        Formula from WCAG: https://www.w3.org/TR/WCAG20/#contrast-ratiodef

        Args:
            color1: First hex color
            color2: Second hex color

        Returns:
            Contrast ratio (1-21)
        """
        lum1 = self._get_luminance(color1)
        lum2 = self._get_luminance(color2)

        # Ensure lum1 is the lighter color
        if lum1 < lum2:
            lum1, lum2 = lum2, lum1

        # Calculate contrast ratio
        return (lum1 + 0.05) / (lum2 + 0.05)
