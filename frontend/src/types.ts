/**
 * TypeScript types for the Fabric Dashboard demo app.
 */

export type AppScreen = 'landing' | 'generating' | 'dashboard';

export type PersonaType = 'fitness-enthusiast' | 'creative-professional' | 'tech-learner' | 'remote-worker' | 'demo';

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

export interface CompleteMessage {
  type: 'complete';
  html: string;
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
  dashboardHTML: string | null;
  selectedPersona: PersonaType | null;
  intelligence: IntelligenceData;
  error: string | null;
}
