/**
 * TypeScript types for the Fabric Dashboard demo app.
 */

export type AppScreen = 'landing' | 'generating' | 'dashboard';

export type PersonaType = 'fitness-enthusiast' | 'creative-professional' | 'tech-learner' | 'remote-worker';

// Pattern data from AI analysis
export interface Pattern {
  title: string;
  confidence: number;
  description: string;
}

// Theme data from AI generation
export interface ThemeData {
  mood: string;
  primary: string;
  rationale: string;
}

// Card title preview
export interface CardPreview {
  title: string;
}

// Progress message types
export interface ProgressMessage {
  type: 'progress';
  step: string;
  percent: number;
  message: string;
  data?: {
    interactions?: number;
    platforms?: string[];
    patterns?: Pattern[];
    mood?: string;
    primary?: string;
    rationale?: string;
    cards?: CardPreview[];
    widgets?: string[];
  };
}

// Dashboard JSON types (from backend)
export interface Widget {
  id: string;
  type: string;
  size: 'small' | 'medium' | 'large';
  priority: number;
  data: Record<string, any>;
}

export interface PersonaProfile {
  writing_style: string;
  interests: string[];
  activity_level: string;
  professional_context?: string;
  tone_preference: string;
  age_range?: string;
  content_depth_preference: string;
}

export interface FontScheme {
  heading: string;
  body: string;
  mono: string;
  heading_url: string;
  body_url: string;
  mono_url: string;
}

export interface BackgroundTheme {
  type: string;
  color?: string;
  gradient?: {
    type: string;
    colors: string[];
    direction?: string;
  };
  pattern?: {
    type: string;
    color: string;
    opacity: number;
    scale: number;
  };
  card_background: string;
  card_backdrop_blur: boolean;
}

export interface ColorScheme {
  primary: string;
  secondary: string;
  accent: string;
  foreground: string;
  muted: string;
  success: string;
  warning: string;
  destructive: string;
  background_theme: BackgroundTheme;
  fonts: FontScheme;
  mood: string;
  rationale: string;
}

export interface DashboardJSON {
  id: string;
  generated_at: string;
  widgets: Widget[];
  theme: ColorScheme;
  persona: PersonaProfile;
}

export interface CompleteMessage {
  type: 'complete';
  html: string;
  dashboard: DashboardJSON;  // New JSON format
  persona: string;
}

export interface ErrorMessage {
  type: 'error';
  message: string;
}

export type WebSocketMessage = ProgressMessage | CompleteMessage | ErrorMessage;

// Intelligence data collected during generation
export interface IntelligenceData {
  patterns: Pattern[];
  theme: ThemeData | null;
  cards: CardPreview[];
  widgets: string[];
  interactions: number;
  platforms: string[];
}

export interface AppState {
  screen: AppScreen;
  progress: number;
  currentStep: string;
  currentMessage: string;
  dashboardHTML: string | null;  // Deprecated, keeping for backward compatibility
  dashboardData: DashboardJSON | null;  // New JSON format
  selectedPersona: PersonaType | null;
  intelligence: IntelligenceData;
  error: string | null;
}
