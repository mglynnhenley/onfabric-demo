/**
 * Main App component - orchestrates all screens with real pipeline data.
 */

import { useState, useCallback, useEffect } from 'react';
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
    dashboardData: null,
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

  // Set data-screen attribute on body for conditional CSS styling
  useEffect(() => {
    document.body.setAttribute('data-screen', state.screen);
    console.log(`📍 Body data-screen attribute set to: ${state.screen}`);
  }, [state.screen]);

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
      // LAYER 4: Verify WebSocket received theme
      console.log('🔍 LAYER 4: WEBSOCKET RECEIVED');
      console.log('  Message:', message);
      console.log('  Has dashboard:', !!message.dashboard);
      console.log('  Has theme:', !!message.dashboard?.theme);
      if (message.dashboard?.theme) {
        console.log('  Theme primary:', message.dashboard.theme.primary);
        console.log('  Theme bg:', message.dashboard.theme.background_theme);
      }

      setState(prev => ({
        ...prev,
        screen: 'dashboard',
        progress: 100,
        dashboardHTML: message.html,  // Deprecated, keeping for backward compatibility
        dashboardData: message.dashboard,  // New JSON format
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
      currentMessage: 'Connecting to AI pipeline...',
      dashboardHTML: null,
      dashboardData: null,
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

    // Connect via WebSocket for real AI pipeline with mock OnFabric data
    connect(persona, handleMessage, handleError);
  };

  const handleGenerateNew = () => {
    setState({
      screen: 'landing',
      progress: 0,
      currentStep: 'initializing',
      currentMessage: 'Initializing...',
      dashboardHTML: null,
      dashboardData: null,
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
      return state.dashboardData ? (
        <Dashboard
          dashboardData={state.dashboardData}
          onGenerateNew={handleGenerateNew}
        />
      ) : (
        <div>Loading dashboard...</div>
      );

    default:
      return <div>Unknown screen</div>;
  }
}

export default App;
