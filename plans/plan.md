# Fabric Intelligence Dashboard - Technical Specification

**Version**: 2.0
**Date**: 2025-10-11
**Architecture**: Python + LangChain + Anthropic Claude + Perplexity + Fabric MCP + Next.js + Shadcn

---

## Executive Summary

Build a **beautifully designed**, personalized intelligence dashboard that:
1. Analyzes user's digital behavior from Fabric MCP (Instagram, Google, Pinterest)
2. Detects behavioral patterns and extracts persona themes using Claude
3. Generates a **color scheme** matched to the user's persona
4. Creates **variable number of content cards** (4-8 cards) with AI-written text from Perplexity
5. Displays in a **modular bento grid** using pre-built Shadcn components

**Key Principle**: Design-first approach. Use Shadcn's beautiful components out-of-the-box, customized only with persona-matched colors. **No full-width cards** - maximum col-span-8 for visual variety.

---

## 🎨 Design Philosophy

### Visual Hierarchy
```
Dashboard Grid (Modular Bento Layout - 12 Column System)
│
├─ Large Cards (col-span-8)
│  └─ Deep content, 400-500 words
│
├─ Medium Cards (col-span-6)
│  └─ Balanced content, 250-300 words
│
├─ Small Cards (col-span-4)
│  └─ Focused content, 150-200 words
│
└─ Compact Cards (col-span-3)
   └─ Quick insights, 100-150 words
```

**Card Count**: 4-8 cards depending on detected patterns
**Layout**: Dynamic based on content importance and depth
**Max Width**: col-span-8 (no full-width cards for visual variety)

### Design System

**Layout**: Interactive bento grid (animated, hoverable cards)
**Components**: Shadcn Card, Badge, Separator, Button (no custom generation!)
**Typography**: Inter for UI, Geist for content
**Spacing**: Generous padding, breathing room
**Animation**: Subtle hover effects, smooth transitions
**Color**: Dynamic theme generated from persona

---

## 🎨 Color System

### Persona → Color Mapping

Claude analyzes persona and generates a **cohesive color scheme**:

```python
class ColorScheme(BaseModel):
    # Primary palette
    primary: str       # Main brand color
    secondary: str     # Supporting color
    accent: str        # Highlights, CTAs

    # Backgrounds
    background: str    # Page background
    card: str          # Card backgrounds

    # Text
    foreground: str    # Primary text
    muted: str         # Secondary text

    # Semantic colors
    success: str
    warning: str
    destructive: str

    # Mood
    mood: str          # "energetic", "calm", "professional", "creative"
    rationale: str     # Why these colors for this user
```

### Color Generation Prompt:
```
Analyze this persona: {persona_analysis}

Generate a cohesive color scheme that reflects their:
- Content style (analytical → cool blues, creative → warm purples)
- Activity patterns (high energy → vibrant, contemplative → muted)
- Professional context (corporate → navy/gray, startup → bold colors)

Requirements:
- WCAG AA accessible contrast
- Modern, sophisticated palette
- Works on both light and dark backgrounds
- Harmonious color relationships
```

### Example Palettes:

**Analytical Persona**:
```css
--primary: 219 100% 62%        /* Intelligent blue */
--secondary: 217 91% 35%       /* Deep navy */
--accent: 176 87% 47%          /* Teal accent */
--background: 220 17% 97%      /* Soft gray */
--card: 0 0% 100%              /* Pure white */
```

**Creative Persona**:
```css
--primary: 271 91% 65%         /* Vibrant purple */
--secondary: 335 78% 60%       /* Warm pink */
--accent: 48 96% 53%           /* Gold accent */
--background: 270 20% 98%      /* Lavender tint */
--card: 0 0% 100%              /* White */
```

**Professional Persona**:
```css
--primary: 217 33% 17%         /* Charcoal */
--secondary: 215 28% 47%       /* Professional blue */
--accent: 142 71% 45%          /* Success green */
--background: 220 13% 96%      /* Light gray */
--card: 0 0% 100%              /* White */
```

---

## 🎨 Component Design Specs

### 1. Large Card (Deep Dive)

**Layout**: col-span-8
**Content**: 400-500 words
**Style**: Prominent, editorial, left border accent

```tsx
<Card className="col-span-8 border-l-4 border-l-primary bg-gradient-to-br from-card to-background/50">
  <CardHeader className="space-y-4">
    <div className="flex items-center justify-between">
      <Badge variant="default" className="gap-1.5">
        <span className="relative flex h-2 w-2">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
          <span className="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
        </span>
        LIVE
      </Badge>
      <span className="text-sm text-muted-foreground">8 min read</span>
    </div>

    <CardTitle className="text-3xl font-bold tracking-tight">
      The Three Schools of AI Safety
    </CardTitle>

    <CardDescription className="text-base">
      Recent developments reveal competing approaches to ensuring AI remains beneficial
    </CardDescription>
  </CardHeader>

  <CardContent className="space-y-6">
    <div className="prose prose-lg prose-neutral max-w-none
                    prose-headings:font-bold prose-headings:tracking-tight
                    prose-h3:text-xl prose-h3:mt-8 prose-h3:mb-4
                    prose-p:text-foreground prose-p:leading-relaxed
                    prose-strong:text-foreground prose-strong:font-semibold
                    prose-ul:my-4 prose-li:my-2">
      {content}
    </div>

    <Separator className="my-6" />

    <div className="flex items-center justify-between">
      <Button variant="ghost" size="sm" className="gap-2">
        <FileText className="h-4 w-4" />
        View 7 Sources
      </Button>
      <Button variant="outline" size="sm" className="gap-2">
        <RefreshCw className="h-4 w-4" />
        Refresh
      </Button>
    </div>
  </CardContent>
</Card>
```

### 2. Medium Card

**Layout**: col-span-6
**Content**: 250-300 words
**Style**: Balanced, informative, hover effects

```tsx
<Card className="col-span-6 group hover:shadow-lg transition-all duration-300">
  <CardHeader>
    <div className="flex items-center gap-2 mb-3">
      <Badge variant="secondary" className="gap-1.5">
        <span className="relative flex h-2 w-2">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
          <span className="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
        </span>
        LIVE
      </Badge>
      <span className="text-xs text-muted-foreground">4 min read</span>
    </div>

    <CardTitle className="text-2xl font-bold tracking-tight group-hover:text-primary transition-colors">
      ESG Investing's Quiet Revolution
    </CardTitle>

    <CardDescription className="mt-2">
      Impact measurement is getting real, and it's changing everything
    </CardDescription>
  </CardHeader>

  <CardContent className="space-y-4">
    <div className="prose prose-neutral max-w-none
                    prose-headings:text-lg prose-headings:font-semibold
                    prose-p:text-sm prose-p:text-muted-foreground
                    prose-ul:text-sm">
      {content}
    </div>

    <div className="flex gap-2 pt-4">
      <Button variant="ghost" size="sm">4 Sources</Button>
      <Button variant="ghost" size="sm">
        <RefreshCw className="h-3 w-3" />
      </Button>
    </div>
  </CardContent>
</Card>
```

### 3. Small Card

**Layout**: col-span-4
**Content**: 150-200 words
**Style**: Focused, clean, border hover

```tsx
<Card className="col-span-4 hover:border-primary transition-colors">
  <CardHeader>
    <Badge variant="outline" className="w-fit gap-1.5 mb-2">
      <span className="relative flex h-1.5 w-1.5">
        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
        <span className="relative inline-flex rounded-full h-1.5 w-1.5 bg-primary"></span>
      </span>
      LIVE
    </Badge>

    <CardTitle className="text-lg font-semibold tracking-tight">
      Quick Space Update
    </CardTitle>
  </CardHeader>

  <CardContent className="space-y-3">
    <p className="text-sm text-muted-foreground leading-relaxed">
      {content}
    </p>

    <div className="flex items-center justify-between pt-2">
      <span className="text-xs text-muted-foreground">2 min read</span>
      <Button variant="ghost" size="sm" className="h-7 w-7 p-0">
        <RefreshCw className="h-3 w-3" />
      </Button>
    </div>
  </CardContent>
</Card>
```

### 4. Compact Card

**Layout**: col-span-3
**Content**: 100-150 words
**Style**: Compact, scannable, quick insights

```tsx
<Card className="col-span-3 relative overflow-hidden
                 before:absolute before:inset-0 before:bg-gradient-to-br
                 before:from-primary/10 before:to-accent/10 before:z-0">
  <div className="relative z-10">
    <CardHeader>
      <Badge variant="secondary" className="w-fit gap-1.5 mb-2 bg-accent/20 text-accent-foreground border-accent/40">
        <Sparkles className="h-3 w-3" />
        WILDCARD
      </Badge>

      <CardTitle className="text-lg font-semibold tracking-tight">
        What AI & Fashion Have in Common
      </CardTitle>
    </CardHeader>

    <CardContent className="space-y-3">
      <p className="text-sm text-muted-foreground leading-relaxed">
        {content}
      </p>

      <Button variant="outline" size="sm" className="w-full mt-4">
        Learn More
      </Button>
    </CardContent>
  </div>
</Card>
```

---

## 🎨 Interactive Grid Layout

### Bento Grid Implementation

```tsx
<div className="container mx-auto p-6 lg:p-12">
  {/* Header */}
  <header className="mb-12 space-y-4">
    <div className="flex items-center justify-between">
      <div>
        <h1 className="text-4xl font-bold tracking-tight">
          Good {timeOfDay}, {userName}
        </h1>
        <p className="text-muted-foreground mt-2">
          Your personalized intelligence dashboard
        </p>
      </div>

      <div className="flex gap-3">
        <Button variant="outline" size="sm">
          <RefreshCw className="h-4 w-4 mr-2" />
          Refresh All
        </Button>
        <Button variant="ghost" size="sm">
          <Settings className="h-4 w-4" />
        </Button>
      </div>
    </div>

    <div className="flex items-center gap-2 text-sm text-muted-foreground">
      <Clock className="h-4 w-4" />
      <span>Last updated {lastUpdated}</span>
      <span className="mx-2">•</span>
      <span>{totalInteractions} interactions analyzed</span>
    </div>
  </header>

  {/* Interactive Bento Grid */}
  <div className="grid grid-cols-12 gap-6 auto-rows-fr">
    {/* Dynamic cards based on detected patterns (4-8 cards) */}
    {/* Example layouts: */}
    {/* Large + Medium: col-span-8 + col-span-4 */}
    {/* Medium + Medium: col-span-6 + col-span-6 */}
    {/* Small + Compact: col-span-4 + col-span-4 + col-span-4 */}
    {cards.map((card, index) => (
      <DynamicCard key={index} card={card} />
    ))}
  </div>

  {/* Footer */}
  <footer className="mt-12 pt-8 border-t border-border">
    <div className="flex items-center justify-between text-sm text-muted-foreground">
      <div className="flex items-center gap-2">
        <span>Powered by</span>
        <Badge variant="outline">Claude</Badge>
        <Badge variant="outline">Perplexity</Badge>
        <Badge variant="outline">Fabric</Badge>
      </div>
      <div>
        Generated in {generationTime}s
      </div>
    </div>
  </footer>
</div>
```

### Responsive Behavior

```css
/* Desktop (default) */
.grid { grid-cols: 12 }

/* Tablet */
@media (max-width: 1024px) {
  .col-span-8 { grid-column: span 12 }   /* Large goes full */
  .col-span-6 { grid-column: span 12 }   /* Medium goes full */
  .col-span-4 { grid-column: span 6 }    /* Small half */
  .col-span-3 { grid-column: span 6 }    /* Compact half */
}

/* Mobile */
@media (max-width: 640px) {
  .col-span-8,
  .col-span-6,
  .col-span-4,
  .col-span-3 { grid-column: span 12 }   /* All full width */
}
```

---

## 🎨 Typography System

### Font Pairing

**UI Elements**: Inter (clean, readable)
**Content**: Geist (modern, editorial)

```css
/* Headings */
.heading-1 {
  font-size: 2.25rem;    /* 36px */
  font-weight: 700;
  line-height: 1.2;
  letter-spacing: -0.02em;
}

.heading-2 {
  font-size: 1.875rem;   /* 30px */
  font-weight: 700;
  line-height: 1.3;
  letter-spacing: -0.01em;
}

.heading-3 {
  font-size: 1.5rem;     /* 24px */
  font-weight: 600;
  line-height: 1.4;
}

/* Body */
.body-large {
  font-size: 1.125rem;   /* 18px */
  line-height: 1.7;
}

.body {
  font-size: 1rem;       /* 16px */
  line-height: 1.6;
}

.body-small {
  font-size: 0.875rem;   /* 14px */
  line-height: 1.5;
}

/* Captions */
.caption {
  font-size: 0.75rem;    /* 12px */
  line-height: 1.4;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
```

---

## 🎨 Animation & Interaction

### Hover Effects

```css
/* Card hover */
.card {
  transition: all 300ms cubic-bezier(0.4, 0, 0.2, 1);
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1);
}

/* Button hover */
.button {
  transition: all 150ms cubic-bezier(0.4, 0, 0.2, 1);
}

.button:hover {
  transform: translateY(-1px);
}

/* Live badge pulse */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.live-badge {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
```

### Loading States

```tsx
{/* Skeleton for loading cards */}
<Card className="col-span-6">
  <CardHeader>
    <Skeleton className="h-4 w-16 mb-3" />
    <Skeleton className="h-8 w-3/4" />
    <Skeleton className="h-4 w-full mt-2" />
  </CardHeader>
  <CardContent>
    <div className="space-y-2">
      <Skeleton className="h-4 w-full" />
      <Skeleton className="h-4 w-full" />
      <Skeleton className="h-4 w-3/4" />
    </div>
  </CardContent>
</Card>
```

---

## 🏗️ Technical Architecture

### Simplified Flow (Design-Focused)

```
User → Generate Dashboard
    ↓
[1] Fabric MCP: Fetch user data
    ↓
[2] Claude: Pattern detection + Persona analysis
    ↓
[3] Claude: Color scheme generation (based on persona)
    ↓
[4] Logic: Widget assignment (4-8 cards, variable layout)
    ↓
[5] Claude: Generate Perplexity queries (per widget)
    ↓
[6] Perplexity: Execute queries (parallel)
    ↓
[7] Claude: Write content (per widget, parallel)
    ↓
[8] Template Engine: Inject content into Shadcn components
    ↓
[9] Build: Generate static HTML with Next.js
    ↓
Output: Beautiful, interactive dashboard
```

### No Component Generation!

Instead of generating components with Claude:

1. **Pre-built Templates**: 4 card size templates (large, medium, small, compact)
2. **Content Injection**: Claude writes the text, we inject into templates
3. **Color Theming**: Apply persona colors via CSS variables
4. **Static Export**: Next.js builds to static HTML

### Implementation Approach

```python
# templates/cards.tsx (static templates)
HERO_CARD_TEMPLATE = """
<Card className="col-span-12 border-l-4 border-l-primary">
  <CardHeader>...</CardHeader>
  <CardContent>
    <div className="prose prose-lg">
      {CONTENT_PLACEHOLDER}
    </div>
  </CardContent>
</Card>
"""

# In generation pipeline:
def generate_dashboard(patterns, persona, content):
    # 1. Generate color scheme from persona
    colors = generate_color_scheme(persona)

    # 2. Inject content into templates
    hero_html = HERO_CARD_TEMPLATE.replace("{CONTENT_PLACEHOLDER}", content[0])
    secondary_html = SECONDARY_CARD_TEMPLATE.replace("{CONTENT_PLACEHOLDER}", content[1])
    # ... etc

    # 3. Build dashboard with colors
    dashboard = build_dashboard(
        cards=[hero_html, secondary_html, tertiary_html, wildcard_html],
        colors=colors,
        metadata={"name": user_name, "timestamp": now()}
    )

    return dashboard
```

---

## 📦 Data Models (Updated)

```python
# models/schemas.py

# Color Scheme Model
class ColorScheme(BaseModel):
    # Primary palette
    primary: str = Field(pattern=r"^#[0-9a-fA-F]{6}$")
    secondary: str = Field(pattern=r"^#[0-9a-fA-F]{6}$")
    accent: str = Field(pattern=r"^#[0-9a-fA-F]{6}$")

    # Backgrounds
    background: str = Field(pattern=r"^#[0-9a-fA-F]{6}$")
    card: str = Field(pattern=r"^#[0-9a-fA-F]{6}$")

    # Text
    foreground: str = Field(pattern=r"^#[0-9a-fA-F]{6}$")
    muted: str = Field(pattern=r"^#[0-9a-fA-F]{6}$")

    # Semantic
    success: str = Field(pattern=r"^#[0-9a-fA-F]{6}$")
    warning: str = Field(pattern=r"^#[0-9a-fA-F]{6}$")
    destructive: str = Field(pattern=r"^#[0-9a-fA-F]{6}$")

    # Metadata
    mood: str  # "energetic", "calm", "professional", "creative"
    rationale: str  # Why these colors

# Card Content Model
class CardContent(BaseModel):
    title: str
    description: str  # Subtitle/tagline
    body: str  # Markdown content
    reading_time_minutes: int
    sources: list[str]
    size: Literal["large", "medium", "small", "compact"]  # col-span-8, 6, 4, 3
    confidence: float  # Pattern confidence (affects positioning)

# Dashboard Model
class Dashboard(BaseModel):
    user_name: str
    generated_at: datetime
    color_scheme: ColorScheme
    cards: list[CardContent]  # 4-8 cards (variable)
    metadata: dict[str, Any]
```

---

## 🚀 Updated Implementation Plan

### Phase 1: Setup Frontend Templates (2 hours)

**Tasks**:
1. Set up Next.js project with Shadcn
2. Create 4 card component templates (hero, secondary, tertiary, wildcard)
3. Set up color theming system (CSS variables)
4. Create dashboard layout with bento grid
5. Test responsive behavior

**Deliverables**:
- ✅ Beautiful, responsive templates
- ✅ Dynamic color theming works
- ✅ All Shadcn components styled

---

### Phase 2: Pattern Detection & Color Generation (2-3 hours)

**Tasks**:
1. ✅ Fabric MCP integration (already set up)
2. Implement pattern detector
3. Implement color scheme generator (Claude)
4. Test color generation with different personas

**Deliverables**:
- ✅ Patterns detected from Fabric data
- ✅ Color schemes generated per persona
- ✅ Colors are accessible and beautiful

---

### Phase 3: Content Generation (2-3 hours)

**Tasks**:
1. Implement query generator (Claude)
2. Implement content fetcher (Perplexity)
3. Implement content writer (Claude)
4. Write in persona-matched styles

**Deliverables**:
- ✅ Smart queries generated
- ✅ Perplexity content fetched
- ✅ Content written in appropriate styles

---

### Phase 4: Template Injection & Build (2 hours)

**Tasks**:
1. Content injection into card templates
2. Color application to CSS variables
3. Next.js static build
4. Test full pipeline

**Deliverables**:
- ✅ Content injected correctly
- ✅ Colors applied throughout
- ✅ Beautiful HTML output

---

### Phase 5: Polish & Animation (1-2 hours)

**Tasks**:
1. Refine animations and transitions
2. Perfect responsive behavior
3. Add loading states
4. Final design polish

**Deliverables**:
- ✅ Smooth, delightful interactions
- ✅ Perfect on all screen sizes
- ✅ Production-ready design

---

## 🎯 Success Metrics

**Design Quality**:
- ✅ Visually stunning on first impression
- ✅ Cohesive color scheme matches persona
- ✅ Typography is readable and elegant
- ✅ Spacing feels generous and intentional
- ✅ Animations are smooth and purposeful

**Technical**:
- ✅ Uses Shadcn components unmodified
- ✅ Responsive on all devices
- ✅ Fast load times (static HTML)
- ✅ Accessible (WCAG AA)

**User Experience**:
- ✅ Content feels personally relevant
- ✅ Colors feel "right" for the user
- ✅ Easy to scan and read
- ✅ Delightful to interact with

---

## Summary

**Key Simplifications**:
- ❌ No AI-generated components
- ✅ Pre-built Shadcn templates
- ✅ Dynamic color theming only
- ✅ Content injection via templates
- ✅ Design-first approach

**Result**: A **beautifully designed** dashboard that's fast to build, reliable to generate, and stunning to look at.
