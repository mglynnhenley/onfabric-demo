/**
 * Main App component - orchestrates all screens with real pipeline data.
 */

import { useState, useCallback } from 'react';
import { Landing } from './components/Landing';
import { Progress } from './components/Progress';
import { Dashboard } from './components/Dashboard';
import { useWebSocket } from './hooks/useWebSocket';
import type { AppState, PersonaType, WebSocketMessage, Pattern, ThemeData, CardPreview } from './types';

function App() {
  const { connect, disconnect } = useWebSocket();

  const [state, setState] = useState<AppState>({
    screen: 'landing',
    progress: 0,
    currentStep: 'initializing',
    currentMessage: 'Initializing...',
    dashboardHTML: null,
    selectedPersona: null,
    intelligence: {
      patterns: [],
      theme: null,
      cards: [],
      widgets: [],
      interactions: 0,
      platforms: [],
    },
    error: null,
  });

  const handleMessage = useCallback((message: WebSocketMessage) => {
    if (message.type === 'error') {
      alert(`Error: ${message.message}`);
      setState(prev => ({
        ...prev,
        screen: 'landing',
        error: message.message,
      }));
      return;
    }

    if (message.type === 'complete') {
      setState(prev => ({
        ...prev,
        screen: 'dashboard',
        progress: 100,
        dashboardHTML: message.html,
      }));
      disconnect();
      return;
    }

    if (message.type === 'progress') {
      setState(prev => {
        const newState = {
          ...prev,
          progress: message.percent,
          currentStep: message.step,
          currentMessage: message.message,
        };

        // Update intelligence data based on step
        if (message.data) {
          const intelligence = { ...prev.intelligence };

          // Data loaded
          if (message.data.interactions !== undefined) {
            intelligence.interactions = message.data.interactions;
          }
          if (message.data.platforms) {
            intelligence.platforms = message.data.platforms;
          }

          // Patterns discovered
          if (message.data.patterns) {
            intelligence.patterns = message.data.patterns as Pattern[];
          }

          // Theme generated
          if (message.data.mood && message.data.primary) {
            intelligence.theme = {
              mood: message.data.mood,
              primary: message.data.primary,
              rationale: message.data.rationale || '',
            } as ThemeData;
          }

          // Cards generated
          if (message.data.cards) {
            intelligence.cards = message.data.cards as CardPreview[];
          }

          // Widgets selected
          if (message.data.widgets) {
            intelligence.widgets = message.data.widgets;
          }

          newState.intelligence = intelligence;
        }

        return newState;
      });
    }
  }, [disconnect]);

  const handleError = useCallback((error: string) => {
    alert(`Connection Error: ${error}\n\nMake sure the backend is running:\ncd backend && uvicorn app.main:app --reload`);
    setState(prev => ({
      ...prev,
      screen: 'landing',
      error,
    }));
  }, []);

  const handleGenerate = (persona: PersonaType) => {
    setState({
      screen: 'generating',
      progress: 0,
      currentStep: 'initializing',
      currentMessage: 'Connecting to server...',
      dashboardHTML: null,
      selectedPersona: persona,
      intelligence: {
        patterns: [],
        theme: null,
        cards: [],
        widgets: [],
        interactions: 0,
        platforms: [],
      },
      error: null,
    });

    connect(persona, handleMessage, handleError);
  };

  const handleGenerateNew = () => {
    setState({
      screen: 'landing',
      progress: 0,
      currentStep: 'initializing',
      currentMessage: 'Initializing...',
      dashboardHTML: null,
      selectedPersona: null,
      intelligence: {
        patterns: [],
        theme: null,
        cards: [],
        widgets: [],
        interactions: 0,
        platforms: [],
      },
      error: null,
    });
  };

  // Render current screen
  switch (state.screen) {
    case 'landing':
      return <Landing onGenerate={handleGenerate} />;

    case 'generating':
      return (
        <Progress
          progress={state.progress}
          currentStep={state.currentStep}
          currentMessage={state.currentMessage}
          intelligence={state.intelligence}
        />
      );

    case 'dashboard':
      return (
        <Dashboard
          html={state.dashboardHTML!}
          persona={state.selectedPersona || 'demo'}
          onGenerateNew={handleGenerateNew}
        />
      );

    default:
      return <div>Unknown screen</div>;
  }
}

export default App;
