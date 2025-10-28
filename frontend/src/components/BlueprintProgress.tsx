/**
 * Blueprint Assembly Loading State - Clean Split Screen Design
 * Three-column layout with zero overlaps
 */

import { useEffect, useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import type { IntelligenceData } from '../types';

interface BlueprintProgressProps {
  progress: number;
  currentStep: string;
  currentMessage: string;
  intelligence: IntelligenceData;
}

interface TerminalMessage {
  text: string;
  completed: boolean;
}

interface DataSource {
  name: string;
  color: string;
  interactions: number;
}

interface DashboardCard {
  label: string;
}

export function BlueprintProgress({ progress, intelligence }: BlueprintProgressProps) {
  const [messages, setMessages] = useState<TerminalMessage[]>([]);

  // Dashboard cards
  const dashboardCards: DashboardCard[] = [
    { label: 'Activity Timeline' },
    { label: 'Pattern Analysis' },
    { label: 'Engagement Metrics' },
    { label: 'Content Insights' },
    { label: 'Peak Hours' },
    { label: 'Recommendations' },
  ];

  // Data sources
  const dataSources: DataSource[] = useMemo(() => [
    {
      name: 'INSTAGRAM',
      color: 'var(--color-crimson)',
      interactions: intelligence.platforms.includes('instagram') ? intelligence.interactions : 847,
    },
    {
      name: 'GOOGLE',
      color: 'var(--color-terminal-green)',
      interactions: intelligence.platforms.includes('google') ? intelligence.interactions : 1203,
    },
    {
      name: 'PINTEREST',
      color: 'var(--color-charcoal)',
      interactions: intelligence.platforms.includes('pinterest') ? intelligence.interactions : 456,
    },
  ], [intelligence]);

  // Progress-based visibility
  const showInstagram = progress >= 15;
  const showGoogle = progress >= 23;
  const showPinterest = progress >= 30;
  const showConstruction = progress >= 40;
  const showPatterns = progress >= 53;
  const showColors = progress >= 60;

  // Terminal messages
  useEffect(() => {
    const newMessages: TerminalMessage[] = [];

    if (progress >= 0) {
      newMessages.push({ text: 'Initializing OnFabric orchestration layer', completed: progress > 8 });
    }
    if (progress >= 5) {
      newMessages.push({ text: 'Establishing secure API connections', completed: progress > 15 });
    }
    if (progress >= 15) {
      newMessages.push({ text: 'Connection established', completed: true });
      newMessages.push({ text: 'Fetching Instagram interactions', completed: progress > 20 });
    }
    if (progress >= 18) {
      newMessages.push({ text: `Retrieved ${dataSources[0].interactions} Instagram interactions`, completed: true });
    }
    if (progress >= 22) {
      newMessages.push({ text: 'Fetching Google activity data', completed: progress > 27 });
    }
    if (progress >= 25) {
      newMessages.push({ text: `Retrieved ${dataSources[1].interactions} Google interactions`, completed: true });
    }
    if (progress >= 28) {
      newMessages.push({ text: 'Fetching Pinterest engagement data', completed: progress > 33 });
    }
    if (progress >= 31) {
      newMessages.push({ text: `Retrieved ${dataSources[2].interactions} Pinterest interactions`, completed: true });
    }
    if (progress >= 35) {
      newMessages.push({ text: 'Calling Weather API for location context', completed: progress > 40 });
    }
    if (progress >= 38) {
      newMessages.push({ text: 'Weather data integrated', completed: true });
    }
    if (progress >= 42) {
      newMessages.push({ text: 'Running pattern detection algorithms', completed: progress > 47 });
    }
    if (progress >= 47 && intelligence.patterns.length > 0) {
      intelligence.patterns.slice(0, 2).forEach((pattern) => {
        newMessages.push({ text: `Detected: ${pattern.title}`, completed: progress > 52 });
      });
    }
    if (progress >= 50) {
      newMessages.push({ text: 'Calling Perplexity API for content insights', completed: progress > 55 });
    }
    if (progress >= 53) {
      newMessages.push({ text: 'Content recommendations generated', completed: true });
    }
    if (progress >= 56) {
      newMessages.push({ text: 'Generating personalized color palette', completed: progress > 61 });
    }
    if (progress >= 59 && intelligence.theme) {
      newMessages.push({ text: `Theme generated: ${intelligence.theme.primary}`, completed: true });
    }
    if (progress >= 62) {
      newMessages.push({ text: 'Calling Google Maps API for location data', completed: progress > 66 });
    }
    if (progress >= 65) {
      newMessages.push({ text: 'Location context integrated', completed: true });
    }
    if (progress >= 68) {
      newMessages.push({ text: 'Generating personalized to-do list', completed: progress > 72 });
    }
    if (progress >= 71) {
      newMessages.push({ text: 'Task priorities calculated', completed: true });
    }
    if (progress >= 74) {
      newMessages.push({ text: 'Orchestrating AI agents for UI assembly', completed: progress > 78 });
    }
    if (progress >= 77) {
      newMessages.push({ text: 'Fabricating dashboard components', completed: progress > 82 });
    }
    if (progress >= 80) {
      newMessages.push({ text: 'Generating personalized widgets', completed: progress > 85 });
    }
    if (progress >= 83) {
      newMessages.push({ text: 'Applying custom styling and layout', completed: progress > 88 });
    }
    if (progress >= 86) {
      newMessages.push({ text: 'Optimizing render performance', completed: progress > 91 });
    }
    if (progress >= 89) {
      newMessages.push({ text: 'Dashboard assembly complete', completed: true });
    }
    if (progress >= 92) {
      newMessages.push({ text: 'Finalizing personalized experience', completed: progress > 96 });
    }
    if (progress >= 95) {
      newMessages.push({ text: 'Your dashboard is ready', completed: true });
    }

    setMessages(newMessages);
  }, [progress, intelligence, dataSources]);

  return (
    <div
      className="min-h-screen flex flex-col"
      style={{ background: 'var(--color-paper)' }}
    >
      {/* Paper texture background */}
      <div
        className="fixed inset-0 pointer-events-none opacity-20"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='100' height='100' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence baseFrequency='0.9' /%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03' /%3E%3C/svg%3E")`,
        }}
      />

      {/* Top Status Bar */}
      <div
        className="border-b flex items-center justify-between relative z-10"
        style={{
          borderColor: 'var(--color-stroke)',
          padding: 'var(--spacing-blueprint-md) var(--spacing-blueprint-lg)',
        }}
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
          <motion.div
            className="w-1.5 h-1.5 rounded-full"
            style={{ background: 'var(--color-terminal-green)' }}
            animate={{ opacity: [1, 0.3, 1] }}
            transition={{ duration: 1.5, repeat: Infinity }}
          />
          <span>{Math.round(progress)}%</span>
        </div>
      </div>

      {/* Three Column Layout */}
      <div className="flex-1 flex relative">
        {/* LEFT COLUMN: Terminal Log */}
        <div
          className="border-r overflow-y-auto"
          style={{
            width: '320px',
            borderColor: 'var(--color-stroke)',
            padding: 'var(--spacing-blueprint-md)',
          }}
        >
          <div className="space-y-1">
            {messages.map((msg, i) => (
              <motion.div
                key={i}
                className="flex items-start gap-2"
                initial={{ opacity: 0, y: -5 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
                style={{
                  fontFamily: 'var(--font-family-mono)',
                  fontSize: '13px',
                  lineHeight: 1.8,
                  color: msg.completed ? 'var(--color-gray)' : 'var(--color-charcoal)',
                }}
              >
                <span
                  style={{
                    color: msg.completed ? 'var(--color-gray)' : 'var(--color-terminal-green)',
                    minWidth: '16px',
                  }}
                >
                  {msg.completed ? '✓' : '▸'}
                </span>
                <span>{msg.text}</span>
              </motion.div>
            ))}
          </div>
        </div>

        {/* CENTER COLUMN: Dashboard Construction */}
        <div className="flex-1 flex items-center justify-center" style={{ padding: 'var(--spacing-blueprint-lg)' }}>
          <AnimatePresence>
            {showConstruction && (
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
                style={{ maxWidth: '700px', width: '100%' }}
              >
                {/* Dashboard Card Grid */}
                <div className="grid grid-cols-2 gap-6">
                  {dashboardCards.map((card, i) => (
                    <motion.div
                      key={i}
                      className="relative border-2 flex items-center justify-center"
                      style={{
                        borderColor: 'var(--color-terminal-green)',
                        background: 'var(--color-white)',
                        minHeight: '120px',
                        padding: 'var(--spacing-blueprint-md)',
                      }}
                      initial={{ opacity: 0, scale: 0.9 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{
                        delay: 0.3 + i * 0.15,
                        duration: 0.6,
                        ease: [0.16, 1, 0.3, 1],
                      }}
                    >
                      {/* Border drawing animation */}
                      <motion.div
                        className="absolute inset-0 border-2 pointer-events-none"
                        style={{ borderColor: 'var(--color-terminal-green)' }}
                        initial={{ clipPath: 'inset(0 100% 100% 0)' }}
                        animate={{ clipPath: 'inset(0 0 0 0)' }}
                        transition={{
                          delay: 0.3 + i * 0.15,
                          duration: 0.8,
                          ease: [0.4, 0.0, 0.2, 1],
                        }}
                      />

                      {/* Card label */}
                      <motion.div
                        style={{
                          fontFamily: 'var(--font-family-mono)',
                          fontSize: '11px',
                          color: 'var(--color-gray)',
                          textAlign: 'center',
                        }}
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 0.6 + i * 0.15, duration: 0.4 }}
                      >
                        {card.label}
                      </motion.div>
                    </motion.div>
                  ))}
                </div>

                {/* Pattern labels below grid */}
                {showPatterns && intelligence.patterns.length > 0 && (
                  <motion.div
                    className="mt-6 space-y-1"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.5, duration: 0.5 }}
                  >
                    {intelligence.patterns.slice(0, 2).map((pattern, i) => (
                      <div
                        key={i}
                        style={{
                          fontFamily: 'var(--font-family-mono)',
                          fontSize: '11px',
                          color: 'var(--color-gray)',
                        }}
                      >
                        ▸ {pattern.title}
                      </div>
                    ))}
                  </motion.div>
                )}

                {/* Color swatches below patterns */}
                {showColors && intelligence.theme && (
                  <motion.div
                    className="mt-4 flex gap-3"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.7, duration: 0.5 }}
                  >
                    {[
                      { color: 'var(--color-crimson)', label: 'crimson' },
                      { color: 'var(--color-terminal-green)', label: 'accent' },
                      { color: 'var(--color-charcoal)', label: 'primary' },
                    ].map((swatch, i) => (
                      <div key={i} className="flex items-center gap-2">
                        <div
                          className="w-5 h-5 border"
                          style={{
                            background: swatch.color,
                            borderColor: 'var(--color-stroke)',
                          }}
                        />
                        <span
                          style={{
                            fontFamily: 'var(--font-family-mono)',
                            fontSize: '10px',
                            color: 'var(--color-gray)',
                          }}
                        >
                          {swatch.label}
                        </span>
                      </div>
                    ))}
                  </motion.div>
                )}
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* RIGHT COLUMN: Data Source Cards */}
        <div
          className="border-l overflow-y-auto"
          style={{
            width: '320px',
            borderColor: 'var(--color-stroke)',
            padding: 'var(--spacing-blueprint-md)',
          }}
        >
          <div className="space-y-6">
            {[
              { show: showInstagram, delay: 0, source: dataSources[0] },
              { show: showGoogle, delay: 0.3, source: dataSources[1] },
              { show: showPinterest, delay: 0.6, source: dataSources[2] },
            ].map(({ show, delay, source }) => (
              <AnimatePresence key={source.name}>
                {show && (
                  <motion.div
                    className="relative border-2 bg-white"
                    style={{
                      borderColor: 'var(--color-stroke)',
                      padding: 'var(--spacing-blueprint-md)',
                    }}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay, duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
                  >
                    {/* Colored border overlay */}
                    <motion.div
                      className="absolute inset-0 border-2 pointer-events-none"
                      style={{ borderColor: source.color }}
                      initial={{ clipPath: 'inset(0 100% 100% 0)' }}
                      animate={{ clipPath: 'inset(0 0 0 0)' }}
                      transition={{ delay: delay + 0.2, duration: 0.8, ease: [0.4, 0.0, 0.2, 1] }}
                    />

                    <div className="space-y-2">
                      <div
                        className="font-medium tracking-wider"
                        style={{
                          fontSize: '12px',
                          letterSpacing: '0.15em',
                          color: 'var(--color-charcoal)',
                          fontFamily: 'var(--font-family-mono)',
                        }}
                      >
                        {source.name}
                      </div>
                      <div
                        style={{
                          fontSize: '13px',
                          color: 'var(--color-gray)',
                          fontFamily: 'var(--font-family-mono)',
                        }}
                      >
                        {source.interactions.toLocaleString()} interactions
                      </div>
                      <div
                        style={{
                          fontSize: '11px',
                          color: 'var(--color-gray)',
                          fontFamily: 'var(--font-family-mono)',
                        }}
                      >
                        2024-10-01 → now
                      </div>
                      <div className="flex items-center gap-2 pt-1">
                        <div
                          className="w-1.5 h-1.5 rounded-full"
                          style={{ background: source.color }}
                        />
                        <span
                          style={{
                            fontSize: '11px',
                            color: 'var(--color-gray)',
                            fontFamily: 'var(--font-family-mono)',
                          }}
                        >
                          fetched
                        </span>
                      </div>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
