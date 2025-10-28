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

interface APICall {
  service: string;
  status: 'calling' | 'complete';
}

export function BlueprintProgress({ progress, intelligence }: BlueprintProgressProps) {
  const [messages, setMessages] = useState<TerminalMessage[]>([]);
  const [apiCalls, setApiCalls] = useState<APICall[]>([]);

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

  // Terminal messages - simplified, no API details
  useEffect(() => {
    const newMessages: TerminalMessage[] = [];

    if (progress >= 0) {
      newMessages.push({ text: 'Initializing OnFabric', completed: progress > 10 });
    }
    if (progress >= 10) {
      newMessages.push({ text: 'Connecting to data sources', completed: progress > 30 });
    }
    if (progress >= 30) {
      newMessages.push({ text: 'Data collection complete', completed: true });
    }
    if (progress >= 35) {
      newMessages.push({ text: 'Analyzing patterns', completed: progress > 55 });
    }
    if (progress >= 55) {
      newMessages.push({ text: 'Pattern analysis complete', completed: true });
    }
    if (progress >= 60) {
      newMessages.push({ text: 'Orchestrating personalization', completed: progress > 80 });
    }
    if (progress >= 80) {
      newMessages.push({ text: 'Building your dashboard', completed: progress > 95 });
    }
    if (progress >= 95) {
      newMessages.push({ text: 'Dashboard ready', completed: true });
    }

    setMessages(newMessages);
  }, [progress, intelligence, dataSources]);

  // API orchestration tracking
  useEffect(() => {
    const calls: APICall[] = [];

    if (progress >= 15) {
      calls.push({ service: 'Instagram Data', status: progress > 20 ? 'complete' : 'calling' });
    }
    if (progress >= 22) {
      calls.push({ service: 'Google Activity', status: progress > 27 ? 'complete' : 'calling' });
    }
    if (progress >= 28) {
      calls.push({ service: 'Pinterest Data', status: progress > 33 ? 'complete' : 'calling' });
    }
    if (progress >= 35) {
      calls.push({ service: 'Weather API', status: progress > 40 ? 'complete' : 'calling' });
    }
    if (progress >= 45) {
      calls.push({ service: 'Perplexity AI', status: progress > 52 ? 'complete' : 'calling' });
    }
    if (progress >= 58) {
      calls.push({ service: 'Google Maps API', status: progress > 64 ? 'complete' : 'calling' });
    }
    if (progress >= 68) {
      calls.push({ service: 'To-Do Generator', status: progress > 74 ? 'complete' : 'calling' });
    }
    if (progress >= 77) {
      calls.push({ service: 'Content Generator', status: progress > 83 ? 'complete' : 'calling' });
    }

    setApiCalls(calls);
  }, [progress]);

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

        {/* CENTER COLUMN: API Orchestration then Dashboard Construction */}
        <div className="flex-1 flex items-center justify-center" style={{ padding: 'var(--spacing-blueprint-lg)' }}>
          {/* API Orchestration View (before dashboard cards) */}
          <AnimatePresence>
            {!showConstruction && apiCalls.length > 0 && (
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
                style={{ maxWidth: '600px', width: '100%' }}
              >
                <div
                  className="mb-6"
                  style={{
                    fontFamily: 'var(--font-family-mono)',
                    fontSize: '14px',
                    color: 'var(--color-charcoal)',
                    letterSpacing: '0.05em',
                  }}
                >
                  Orchestrating Services
                </div>
                <div className="space-y-3">
                  {apiCalls.map((call, i) => (
                    <motion.div
                      key={call.service}
                      className="flex items-center justify-between border-2 bg-white"
                      style={{
                        padding: 'var(--spacing-blueprint-md)',
                        borderColor: call.status === 'complete' ? 'var(--color-terminal-green)' : 'var(--color-stroke)',
                      }}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.1, duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
                    >
                      <span
                        style={{
                          fontFamily: 'var(--font-family-mono)',
                          fontSize: '13px',
                          color: 'var(--color-charcoal)',
                        }}
                      >
                        {call.service}
                      </span>
                      <div className="flex items-center gap-2">
                        {call.status === 'calling' ? (
                          <>
                            <motion.div
                              className="w-1.5 h-1.5 rounded-full"
                              style={{ background: 'var(--color-terminal-green)' }}
                              animate={{ opacity: [1, 0.3, 1] }}
                              transition={{ duration: 1, repeat: Infinity }}
                            />
                            <span
                              style={{
                                fontFamily: 'var(--font-family-mono)',
                                fontSize: '11px',
                                color: 'var(--color-gray)',
                              }}
                            >
                              calling...
                            </span>
                          </>
                        ) : (
                          <>
                            <span style={{ color: 'var(--color-terminal-green)', fontSize: '14px' }}>✓</span>
                            <span
                              style={{
                                fontFamily: 'var(--font-family-mono)',
                                fontSize: '11px',
                                color: 'var(--color-gray)',
                              }}
                            >
                              complete
                            </span>
                          </>
                        )}
                      </div>
                    </motion.div>
                  ))}
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Dashboard Construction View */}
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
