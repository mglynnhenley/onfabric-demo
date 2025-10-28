/**
 * Progress screen - Blueprint construction with technical process log.
 */

import { useEffect, useState, useRef } from 'react';
import { motion } from 'framer-motion';
import type { IntelligenceData } from '../types';

interface ProgressProps {
  progress: number;
  currentStep: string;
  currentMessage: string;
  intelligence: IntelligenceData;
}

// Developer-focused technical process steps
const BASE_MESSAGES = [
  '▸ Initializing WebSocket connection to OnFabric API',
  '▸ Authenticating with device code flow...',
  '▸ Fetching interaction graph from /api/threads',
  '▸ Running NLP preprocessing on message bodies',
  '▸ Extracting temporal features (timestamps, duration, frequency)',
  '▸ Computing embedding vectors for semantic analysis',
  '▸ Applying clustering algorithm to identify patterns',
  '▸ Generating color palette based on interaction entropy',
  '▸ Selecting UI components from pattern library',
  '▸ Rendering personalized interface...',
];

export function Progress({ progress, currentMessage, intelligence }: ProgressProps) {
  const [messages, setMessages] = useState<string[]>([]);
  const prevMessageRef = useRef('');

  // Build full message list from actual data
  useEffect(() => {
    const newMessages = [...BASE_MESSAGES];

    // Add actual intelligence data when available
    if (intelligence.interactions > 0) {
      const idx = newMessages.findIndex(m => m.includes('Fetching'));
      if (idx >= 0) {
        newMessages.splice(idx + 1, 0, `▸ Retrieved ${intelligence.interactions} interactions`);
      }
    }

    intelligence.patterns.forEach(pattern => {
      if (pattern.name && pattern.name !== 'undefined') {
        newMessages.push(`▸ Pattern detected: ${pattern.name}`);
      }
    });

    if (intelligence.theme && intelligence.theme.mood) {
      newMessages.push(`▸ Theme computed: ${intelligence.theme.mood}`);
    }

    setMessages(newMessages);
  }, [intelligence]);

  // Add current message if it's new
  useEffect(() => {
    if (currentMessage && currentMessage !== prevMessageRef.current) {
      prevMessageRef.current = currentMessage;
      if (!messages.includes(currentMessage)) {
        setMessages(prev => [...prev, currentMessage]);
      }
    }
  }, [currentMessage, messages]);

  // Calculate visible items based on progress
  const visibleMessageCount = Math.max(1, Math.ceil((progress / 100) * messages.length));

  return (
    <div
      className="min-h-screen flex flex-col"
      style={{ background: 'var(--color-paper)' }}
    >
      {/* Subtle paper texture */}
      <div
        className="fixed inset-0 pointer-events-none opacity-20"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='100' height='100' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence baseFrequency='0.9' /%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03' /%3E%3C/svg%3E")`,
        }}
      />

      {/* Subtle grid */}
      <div
        className="fixed inset-0 pointer-events-none opacity-5"
        style={{
          backgroundImage: `
            linear-gradient(to right, var(--color-stroke) 1px, transparent 1px),
            linear-gradient(to bottom, var(--color-stroke) 1px, transparent 1px)
          `,
          backgroundSize: '60px 60px',
        }}
      />

      {/* Top Status Bar - Zen Terminal */}
      <div
        className="relative z-10 border-b px-8 py-6 flex items-center justify-between"
        style={{ borderColor: 'var(--color-stroke)' }}
      >
        <div
          className="flex items-center gap-3"
          style={{
            fontFamily: 'var(--font-family-mono)',
            fontSize: '12px',
            color: 'var(--color-gray)',
            fontWeight: 300,
          }}
        >
          <span style={{ color: 'var(--color-terminal-green)' }}>▸</span>
          <span>generating.interface()</span>
        </div>
        <div
          className="flex items-center gap-4"
          style={{
            fontFamily: 'var(--font-family-mono)',
            fontSize: '12px',
            color: 'var(--color-charcoal)',
            fontWeight: 500,
          }}
        >
          <div
            className="w-1.5 h-1.5 rounded-full animate-blink"
            style={{ background: 'var(--color-terminal-green)' }}
          />
          <span>{progress}%</span>
        </div>
      </div>

      {/* Main Content - Centered Terminal Output */}
      <div className="relative z-10 flex-1 flex items-center justify-center px-8 py-16">
        <div className="w-full max-w-[800px]">
          {/* Progress bar */}
          <div className="mb-12">
            <div
              className="h-0.5 w-full"
              style={{ background: 'var(--color-stroke)' }}
            >
              <motion.div
                className="h-full"
                style={{ background: 'var(--color-terminal-green)' }}
                initial={{ width: '0%' }}
                animate={{ width: `${progress}%` }}
                transition={{ duration: 0.3, ease: 'easeOut' }}
              />
            </div>
          </div>

          {/* Technical Message Stream */}
          <div className="space-y-1">
            {/* Only show messages up to current progress */}
            {messages.slice(0, visibleMessageCount).map((message, index) => {
              const isLatest = index === visibleMessageCount - 1;

              return (
                <motion.div
                  key={index}
                  className="flex items-start gap-4 py-3"
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{
                    duration: 0.2,
                    ease: 'easeOut',
                  }}
                >
                  <span
                    className={isLatest ? 'animate-blink' : ''}
                    style={{
                      color: isLatest ? 'var(--color-terminal-green)' : 'var(--color-gray)',
                      fontSize: '14px',
                      marginTop: '3px',
                      minWidth: '16px',
                    }}
                  >
                    {isLatest ? '▸' : '✓'}
                  </span>
                  <span
                    style={{
                      fontFamily: 'var(--font-family-mono)',
                      fontSize: '15px',
                      lineHeight: 1.6,
                      color: isLatest ? 'var(--color-charcoal)' : 'var(--color-gray)',
                      fontWeight: isLatest ? 500 : 400,
                    }}
                  >
                    {message}
                  </span>
                </motion.div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
