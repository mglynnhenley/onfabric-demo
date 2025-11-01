# Demo 2: Fashion-Loving Film Producer - Design Document

**Date**: 2025-10-31
**Purpose**: Create second demo persona showcasing dashboard flexibility with contrasting aesthetic and content

## Design Goals

1. **Maximum Contrast with Demo 1**: Show system can handle radically different aesthetics
2. **Rich, Authentic Content**: Real YouTube videos, accurate locations, plausible persona
3. **Life Research Dashboard**: Demonstrate value for major life transitions (relocation)
4. **Creative Professional Profile**: Non-tech persona to broaden appeal

## Persona Profile

**Demographics**:
- Age: 30-35
- Location: Paris (currently) → London (relocating)
- Profession: Film Producer
- Passion: Fashion enthusiast (consumer, not industry)

**Interests & Lifestyle**:
- Primary: Fashion weeks, designer collections, style culture
- Secondary: Art galleries, exhibitions, contemporary art
- Entertainment: Horror films (A24/auteur, not mainstream)
- Culinary: Fine dining, Michelin restaurants, wine culture
- Wellness: Pilates, mindful movement
- Life Stage: Actively house hunting in London neighborhoods

**Contrast with Demo 1**:
| Aspect | Demo 1 (Tech Founder) | Demo 2 (Film Producer) |
|--------|---------------------|----------------------|
| Industry | Tech/AI | Film/Creative |
| Aesthetic | Terminal/Technical | Editorial/Elegant |
| Gender Coding | Male-coded | Female-coded |
| Color Palette | Black/Gold/Green | White/Burgundy/Gold |
| Typography | Monospace only | Serif headlines + Sans body |
| Energy | High-intensity startup | Refined creative |
| Content Density | Dense technical grid | Spacious editorial layout |

## Visual Theme: "Editorial Vogue"

**Mood**: "Editorial elegance meets cinematic sophistication"

**Color Scheme**:
```json
{
  "primary": "#8B2635",        // Deep burgundy (Vogue-esque)
  "secondary": "#2C3E50",      // Charcoal blue (editorial depth)
  "accent": "#C9A961",         // Antique gold (luxury touch)
  "background": "#FEFEFE",     // Pure white (magazine page)
  "foreground": "#1A1A1A",     // Near-black (readable text)
  "muted": "#6B7280",          // Cool gray (metadata)
  "success": "#2D6A4F",        // Forest green
  "warning": "#C9A961",        // Gold (same as accent)
  "destructive": "#B91C1C"     // Deep red
}
```

**Typography**:
- **Heading**: `Playfair Display` - Classic editorial serif
- **Body**: `Inter` - Clean modern sans-serif
- **Mono**: `JetBrains Mono` - Refined monospace for data

**Background Treatment**:
- Type: `gradient`
- Colors: `#FEFEFE` → `#F8F6F4` (subtle warm gradient)
- Direction: `to-br`
- Card background: `rgba(255, 255, 255, 0.95)`
- Card backdrop blur: `true`

**Rationale**: High-fashion magazine aesthetic with dramatic contrast, lots of white space, elegant serif headlines. Think Vogue masthead, gallery walls, editorial sophistication.

## Content Patterns

### Pattern 1: London House Hunter (Confidence: 0.91)
**Description**: Actively researching London neighborhoods for relocation. Comparing areas based on creative industry proximity, cultural amenities, and lifestyle fit.

**Keywords**: London neighborhoods, Notting Hill, Shoreditch, Marylebone, property, relocation, creative hubs

**Interaction Count**: 58

**Time Range**: 2025-09-01 to 2025-10-31

### Pattern 2: Fashion Week Follower (Confidence: 0.88)
**Description**: Tracks global fashion weeks and designer collections. Passionate enthusiast following runway shows, designer profiles, and fashion trends across major fashion capitals.

**Keywords**: fashion week, runway, designers, collections, haute couture, Paris Fashion Week, street style

**Interaction Count**: 47

### Pattern 3: Art & Gallery Circuit (Confidence: 0.85)
**Description**: Regular museum visitor and gallery-goer. Follows contemporary art, exhibitions, and gallery openings in Paris. Cultural event enthusiast.

**Keywords**: exhibitions, contemporary art, galleries, Louvre, Musée d'Orsay, vernissage, art openings

**Interaction Count**: 42

### Pattern 4: Horror Film Devotee (Confidence: 0.82)
**Description**: Dedicated horror genre fan. Watches critically acclaimed horror films, follows horror directors, explores psychological thrillers. More A24/auteur than mainstream.

**Keywords**: horror films, A24, psychological thriller, Ari Aster, Jordan Peele, atmospheric horror

**Interaction Count**: 39

### Pattern 5: Culinary Explorer (Confidence: 0.79)
**Description**: Appreciates fine dining and food culture. Researches Michelin restaurants, wine pairings, and culinary experiences in Paris and London.

**Keywords**: Michelin, restaurants, wine, gastronomy, chef, tasting menu

**Interaction Count**: 34

### Pattern 6: Wellness & Movement (Confidence: 0.76)
**Description**: Maintains wellness routine through Pilates and mindful practices. Balances creative work intensity with movement and self-care.

**Keywords**: Pilates, wellness, movement, studios, mindfulness

**Interaction Count**: 28

## UI Components

### 1. Map Card: London Neighborhoods to Explore
**Pattern**: London House Hunter
**Confidence**: 0.91

**Map Configuration**:
- Center: Shoreditch area (51.5244, -0.0786)
- Zoom: 12

**Markers**:
1. **Notting Hill** (51.5074, -0.1958) - Classic elegance, creative hub, film production nearby
2. **Shoreditch** (51.5244, -0.0786) - East London creative heart, galleries, young energy
3. **Marylebone** (51.5175, -0.1545) - Refined central village, West End production proximity
4. **Primrose Hill** (51.5418, -0.1631) - Village charm, media professionals, quieter elegance
5. **King's Cross** (51.5301, -0.1232) - Transformed industrial, film studios, transport hub

### 2. Map Card: Paris Fashion & Art District
**Pattern**: Fashion Week Follower + Art Circuit
**Confidence**: 0.85

**Map Configuration**:
- Center: Le Marais (48.8578, 2.3617)
- Zoom: 13

**Markers**:
1. **Le Marais** (48.8578, 2.3617) - Fashion boutiques, vintage treasures
2. **Palais de Tokyo** (48.8639, 2.2975) - Contemporary art, experimental exhibitions
3. **Centre Pompidou** (48.8606, 2.3522) - Modern art, brutalist icon
4. **Saint-Germain Ateliers** (48.8530, 2.3324) - Haute couture workshops
5. **Galeries Lafayette** (48.8738, 2.3320) - Fashion institution, Art Nouveau

### 3. Event Calendar: Fashion & Culture Calendar
**Pattern**: Fashion Week Follower + Art Circuit
**Confidence**: 0.85

**Events** (November-December 2025):
- Fashion Weeks: Paris, Milan, London, Copenhagen, NYC
- Art: Frieze London, Paris Photo, gallery openings
- Film: BFI London Film Festival (horror programming)
- Personal: Pilates studio visits, restaurant reservations

### 4. Video Feed: Horror Cinema Essentials
**Pattern**: Horror Film Devotee
**Confidence**: 0.82

**Content Focus**: A24 horror, psychological thrillers, auteur horror, film criticism

**Video Selection Criteria**:
- Real YouTube videos from film analysis channels
- Focus on elevated/atmospheric horror
- Behind-the-scenes and director interviews
- Production design and visual language analysis

### 5. Video Feed: Fashion Film & Runway
**Pattern**: Fashion Week Follower
**Confidence**: 0.88

**Content Focus**: Runway shows, designer documentaries, fashion film shorts

**Video Selection Criteria**:
- Real YouTube videos from Vogue, Fashion Week channels
- Behind-the-scenes haute couture
- Fashion photography and filmmaking
- Designer profiles and craftsmanship

### 6. Info Card: Paris Weather
**Pattern**: Current location
**Configuration**: `location: "Paris, France"`, `units: "metric"`

### 7. Info Card: London Weather
**Pattern**: Future location (house hunting)
**Configuration**: `location: "London, UK"`, `units: "metric"`

### 8. Task List: London Move Planning
**Pattern**: London House Hunter + Culinary Explorer
**Confidence**: 0.91

**Tasks**:
- House hunting (neighborhood viewings, estate agent meetings)
- Restaurant reservations (trying London dining scene)
- Practical moving tasks
- Cultural exploration (galleries, studios)

### 9. Content Cards (Article Cards)

**Card 1: "Why Notting Hill Still Holds Its Creative Soul"**
- **Pattern**: London House Hunter
- **Size**: Small
- **Topic**: Neighborhood character, creative community, film industry presence

**Card 2: "The New Wave of Elevated Horror"**
- **Pattern**: Horror Film Devotee
- **Size**: Small
- **Topic**: A24's influence, auteur horror trend, production values

**Card 3: "From Paris to London: The Creative Producer's Guide"**
- **Pattern**: London House Hunter
- **Size**: Small
- **Topic**: Relocation insights, industry differences, maintaining creative network

**Card 4: "Fashion Week Through a Film Producer's Lens"**
- **Pattern**: Fashion Week Follower
- **Size**: Compact
- **Topic**: Cinematic elements of fashion, storytelling on runway, visual language

## Layout Philosophy

**Contrast with Demo 1**:
- Demo 1: Dense technical grid with many small widgets
- Demo 2: Generous spacing, larger hero components
- Article cards get prominence (small/medium sizes vs compact/small)
- More breathing room between elements
- Editorial "feature story" feeling

## Implementation Notes

### Real Data Requirements

**✅ Already Real (No Changes Needed)**:
- Map coordinates are accurate
- Weather uses existing API integration
- Locations are correct

**🔍 Needs Real Data (Implementation Phase)**:
- YouTube video URLs, IDs, thumbnails, durations
- Search channels: Vogue, Every Frame a Painting, Lessons from the Screenplay, Now You See It, Fashion Week Online

**📅 Semi-Real (Acceptable for Demo)**:
- Fashion Week dates use real 2025 schedules
- Gallery exhibitions reference real venues but upcoming dates may be fictional

### File Structure
- Location: `fabric_dashboard/tests/fixtures/personas/demo2.json`
- Format: Same JSON schema as demo.json

### Testing
- Verify theme loads correctly with Editorial Vogue aesthetic
- Confirm font loading (Playfair Display, Inter, JetBrains Mono)
- Test map rendering with all markers
- Validate weather API calls for both cities
- Check video embeds work with real YouTube URLs

## Success Criteria

✅ Visual contrast with Demo 1 is immediately apparent
✅ Persona feels authentic and cohesive
✅ Content tells a story (Paris → London transition)
✅ All components use real data where applicable
✅ Typography and color scheme reflect editorial sophistication
✅ Layout demonstrates system flexibility

## Next Steps

1. Create `demo2.json` fixture file
2. Search YouTube for real video content
3. Populate all components with final data
4. Test loading in dashboard
5. Verify theme application
6. Compare side-by-side with Demo 1 for contrast validation
