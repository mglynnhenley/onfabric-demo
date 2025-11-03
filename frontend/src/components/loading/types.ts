import type { Pattern, PersonaProfile } from '../../types';

export type StageStatus = 'pending' | 'active' | 'complete';

export interface StageData {
  data?: {
    interactions: number;
    platforms: string[];
  };
  patterns?: {
    persona: PersonaProfile;
    patterns: Pattern[];
  };
  theme?: {
    mood: string;
    primary: string;
    rationale: string;
  };
  widgets?: {
    widgets: string[];
  };
  enrichment?: {
    apis: string[];
  };
  building?: {
    cardCount: number;
    widgetCount: number;
  };
}

export interface LoadingState {
  currentStep: string;
  percent: number;
  message: string;
  stageStatuses: {
    data: StageStatus;
    patterns: StageStatus;
    theme: StageStatus;
    widgets: StageStatus;
    enrichment: StageStatus;
    building: StageStatus;
  };
  stageData: StageData;
}

export interface PipelineStageConfig {
  id: string;
  title: string;
  icon: string;
  websocketStep: string[];
}
