/**
 * Custom hook for WebSocket connection to backend.
 */

import { useRef, useCallback } from 'react';
import type { WebSocketMessage, PersonaType } from '../types';

const WS_URL = import.meta.env.PROD
  ? 'wss://your-app.up.railway.app/ws/generate'  // TODO: Update with actual Railway URL
  : 'ws://localhost:8001/ws/generate';

export function useWebSocket() {
  const wsRef = useRef<WebSocket | null>(null);

  const connect = useCallback((
    persona: PersonaType,
    onMessage: (message: WebSocketMessage) => void,
    onError: (error: string) => void
  ) => {
    try {
      const ws = new WebSocket(`${WS_URL}/${persona}`);
      wsRef.current = ws;

      ws.onopen = () => {
        console.log(`✓ WebSocket connected for ${persona}`);
      };

      ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data) as WebSocketMessage;
          onMessage(message);
        } catch (err) {
          console.error('Failed to parse WebSocket message:', err);
          onError('Failed to parse server message');
        }
      };

      ws.onerror = () => {
        onError('Connection error. Make sure the backend is running on port 8001.');
      };

      ws.onclose = () => {
        console.log('WebSocket disconnected');
      };

    } catch (err) {
      console.error('Failed to create WebSocket:', err);
      onError('Failed to connect to server');
    }
  }, []);

  const disconnect = useCallback(() => {
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
  }, []);

  return { connect, disconnect };
}
