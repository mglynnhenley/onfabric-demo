/**
 * Blueprint Assembly Loading State
 * A technical blueprint construction metaphor showing OnFabric's orchestration
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
  position: { x: number; y: number };
  color: string;
  interactions: number;
}

export function BlueprintProgress({ progress, intelligence }: BlueprintProgressProps) {
  const [messages, setMessages] = useState<TerminalMessage[]>([]);

  // Data sources configuration
  const dataSources: DataSource[] = useMemo(() => [
    {
      name: 'INSTAGRAM',
      position: { x: 20, y: 15 },
      color: 'var(--color-crimson)',
      interactions: intelligence.platforms.includes('instagram') ? intelligence.interactions : 847,
    },
    {
      name: 'GOOGLE',
      position: { x: 80, y: 20 },
      color: 'var(--color-terminal-green)',
      interactions: intelligence.platforms.includes('google') ? intelligence.interactions : 1203,
    },
    {
      name: 'PINTEREST',
      position: { x: 50, y: 75 },
      color: 'var(--color-charcoal)',
      interactions: intelligence.platforms.includes('pinterest') ? intelligence.interactions : 456,
    },
  ], [intelligence]);

  // Progress-based timeline
  const showGrid = progress >= 0;
  const showInstagram = progress >= 15;
  const showGoogle = progress >= 23;
  const showPinterest = progress >= 30;
  const showConstruction = progress >= 40;
  const showPatterns = progress >= 53;
  const showColors = progress >= 60;
  const startFadeOut = progress >= 75;

  // Terminal messages synchronized to progress
  useEffect(() => {
    const newMessages: TerminalMessage[] = [];

    if (progress >= 0) {
      newMessages.push({ text: '▸ Initializing blueprint rendering engine', completed: progress > 8 });
    }
    if (progress >= 5) {
      newMessages.push({ text: '▸ Drawing construction grid...', completed: progress > 15 });
    }
    if (progress >= 15) {
      newMessages.push({ text: '✓ Foundation ready', completed: true });
      newMessages.push({ text: '▸ Connecting to OnFabric API endpoints', completed: progress > 20 });
    }
    if (progress >= 18) {
      newMessages.push({ text: `▸ Fetching Instagram data... ${dataSources[0].interactions} interactions`, completed: progress > 23 });
    }
    if (progress >= 23) {
      newMessages.push({ text: `▸ Fetching Google data... ${dataSources[1].interactions} interactions`, completed: progress > 30 });
    }
    if (progress >= 28) {
      newMessages.push({ text: `▸ Fetching Pinterest data... ${dataSources[2].interactions} interactions`, completed: progress > 35 });
    }
    if (progress >= 35) {
      newMessages.push({ text: '✓ Data streams established', completed: true });
    }
    if (progress >= 40) {
      newMessages.push({ text: '▸ Running pattern detection algorithms', completed: progress > 47 });
    }
    if (progress >= 47 && intelligence.patterns.length > 0) {
      intelligence.patterns.slice(0, 2).forEach((pattern) => {
        newMessages.push({ text: `▸ Detected: ${pattern.title}`, completed: progress > 53 });
      });
    }
    if (progress >= 53) {
      newMessages.push({ text: '▸ Generating color palette from data entropy', completed: progress > 60 });
    }
    if (progress >= 58 && intelligence.theme) {
      newMessages.push({ text: `▸ Color sampled: ${intelligence.theme.primary} (primary accent)`, completed: progress > 65 });
    }
    if (progress >= 63) {
      newMessages.push({ text: '▸ Orchestrating AI agents for UI selection', completed: progress > 68 });
    }
    if (progress >= 68) {
      newMessages.push({ text: '▸ Fabricating personalized widgets...', completed: progress > 75 });
    }
    if (progress >= 75) {
      newMessages.push({ text: '✓ Interface components assembled', completed: true });
      newMessages.push({ text: '▸ Finalizing render...', completed: progress > 88 });
    }
    if (progress >= 94) {
      newMessages.push({ text: '✓ Your dashboard is ready', completed: true });
    }

    setMessages(newMessages);
  }, [progress, intelligence, dataSources]);

  return (
    <div
      className="relative min-h-screen overflow-hidden"
      style={{ background: 'var(--color-paper)' }}
    >
      {/* Existing paper texture */}
      <div
        className="fixed inset-0 pointer-events-none opacity-20"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='100' height='100' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence baseFrequency='0.9' /%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03' /%3E%3C/svg%3E")`,
        }}
      />

      {/* Existing subtle grid */}
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

      {/* Red sun circle (from Landing) */}
      <div
        className="fixed"
        style={{
          top: '10%',
          right: '8%',
          width: '120px',
          height: '120px',
          borderRadius: '50%',
          background: 'var(--color-crimson)',
          opacity: 0.15,
        }}
      />

      {/* Blueprint Grid Overlay */}
      <AnimatePresence>
        {showGrid && !startFadeOut && (
          <motion.div
            className="fixed inset-0 pointer-events-none"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.8 }}
          >
            <svg className="w-full h-full">
              {/* Technical grid lines */}
              <defs>
                <pattern
                  id="blueprint-grid"
                  width="80"
                  height="80"
                  patternUnits="userSpaceOnUse"
                >
                  <path
                    d="M 80 0 L 0 0 0 80"
                    fill="none"
                    stroke="var(--color-stroke)"
                    strokeWidth="0.5"
                    opacity="0.3"
                  />
                </pattern>
              </defs>

              <rect width="100%" height="100%" fill="url(#blueprint-grid)" />

              {/* Corner brackets */}
              {[
                { x: '2%', y: '2%', rotate: 0 },
                { x: '98%', y: '2%', rotate: 90 },
                { x: '98%', y: '98%', rotate: 180 },
                { x: '2%', y: '98%', rotate: 270 },
              ].map((corner, i) => (
                <motion.g
                  key={i}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 0.4 }}
                  transition={{ delay: 0.5 + i * 0.1, duration: 0.5 }}
                  transform={`translate(${corner.x}, ${corner.y}) rotate(${corner.rotate})`}
                >
                  <path
                    d="M 0 0 L 40 0 M 0 0 L 0 40"
                    stroke="var(--color-charcoal)"
                    strokeWidth="2"
                    fill="none"
                  />
                </motion.g>
              ))}
            </svg>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Data Source Nodes */}
      <AnimatePresence>
        {[
          { show: showInstagram, delay: 0, source: dataSources[0] },
          { show: showGoogle, delay: 0.3, source: dataSources[1] },
          { show: showPinterest, delay: 0.6, source: dataSources[2] },
        ].map(({ show, delay, source }, index) => (
          show && !startFadeOut && (
            <motion.div
              key={source.name}
              className="fixed"
              style={{
                left: `${source.position.x}%`,
                top: `${source.position.y}%`,
                transform: 'translate(-50%, -50%)',
              }}
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.8 }}
              transition={{ delay, duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
            >
              {/* Node box */}
              <div
                className="relative border-2 bg-white px-6 py-4 min-w-[240px]"
                style={{
                  borderColor: 'var(--color-stroke)',
                  fontFamily: 'var(--font-family-mono)',
                }}
              >
                {/* Animated border reveal */}
                <motion.div
                  className="absolute inset-0 border-2 pointer-events-none"
                  style={{ borderColor: source.color }}
                  initial={{ clipPath: 'inset(0 100% 100% 0)' }}
                  animate={{ clipPath: 'inset(0 0 0 0)' }}
                  transition={{ delay: delay + 0.2, duration: 0.8 }}
                />

                <div className="space-y-1">
                  <div
                    className="font-medium tracking-wider mb-2"
                    style={{
                      fontSize: '12px',
                      letterSpacing: '0.15em',
                      color: 'var(--color-charcoal)',
                    }}
                  >
                    {source.name}
                  </div>
                  <div style={{ fontSize: '13px', color: 'var(--color-gray)' }}>
                    {source.interactions.toLocaleString()} interactions
                  </div>
                  <div style={{ fontSize: '11px', color: 'var(--color-gray)' }}>
                    2024-10-01 → now
                  </div>
                  <div className="flex items-center gap-2 mt-2">
                    <div
                      className="w-1.5 h-1.5 rounded-full"
                      style={{ background: source.color }}
                    />
                    <span style={{ fontSize: '11px', color: 'var(--color-gray)' }}>
                      fetched
                    </span>
                  </div>
                </div>
              </div>

              {/* Connecting line to center */}
              <svg
                className="absolute top-1/2 left-1/2 pointer-events-none"
                style={{
                  width: '100vw',
                  height: '100vh',
                  transform: 'translate(-50%, -50%)',
                }}
              >
                <motion.line
                  x1="50%"
                  y1="50%"
                  x2="50vw"
                  y2="50vh"
                  stroke={source.color}
                  strokeWidth="1"
                  opacity="0.3"
                  initial={{ pathLength: 0 }}
                  animate={{ pathLength: 1 }}
                  transition={{ delay: delay + 0.4, duration: 1 }}
                />
              </svg>

              {/* Data particles flowing */}
              {Array.from({ length: 8 }).map((_, i) => (
                <motion.div
                  key={i}
                  className="absolute w-2 h-2 rounded-full pointer-events-none"
                  style={{
                    background: source.color,
                    left: '50%',
                    top: '50%',
                  }}
                  initial={{ x: 0, y: 0, opacity: 0 }}
                  animate={{
                    x: (window.innerWidth / 2 - (source.position.x * window.innerWidth) / 100),
                    y: (window.innerHeight / 2 - (source.position.y * window.innerHeight) / 100),
                    opacity: [0, 0.8, 0],
                  }}
                  transition={{
                    delay: delay + 1 + i * 0.3,
                    duration: 2,
                    repeat: Infinity,
                    repeatDelay: 1,
                  }}
                />
              ))}
            </motion.div>
          )
        ))}
      </AnimatePresence>

      {/* Construction Zone */}
      <AnimatePresence>
        {showConstruction && !startFadeOut && (
          <motion.div
            className="fixed left-1/2 top-1/2"
            style={{ transform: 'translate(-50%, -50%)' }}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.8 }}
          >
            {/* Dashed construction frame */}
            <div
              className="relative border-2 border-dashed w-[400px] h-[300px] flex items-center justify-center"
              style={{
                borderColor: 'var(--color-stroke)',
                background: 'rgba(255, 255, 255, 0.5)',
              }}
            >
              {/* Pattern labels */}
              {showPatterns && intelligence.patterns.length > 0 && (
                <div className="absolute top-4 left-4 space-y-2">
                  {intelligence.patterns.slice(0, 2).map((pattern, i) => (
                    <motion.div
                      key={i}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.2, duration: 0.4 }}
                      style={{
                        fontFamily: 'var(--font-family-mono)',
                        fontSize: '11px',
                        color: 'var(--color-gray)',
                      }}
                    >
                      ▸ {pattern.title}
                    </motion.div>
                  ))}
                </div>
              )}

              {/* Color swatches */}
              {showColors && intelligence.theme && (
                <motion.div
                  className="absolute bottom-4 right-4 flex gap-2"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ duration: 0.5 }}
                >
                  {[
                    { color: 'var(--color-crimson)', label: 'crimson' },
                    { color: 'var(--color-terminal-green)', label: 'accent' },
                    { color: 'var(--color-charcoal)', label: 'primary' },
                  ].map((swatch, i) => (
                    <motion.div
                      key={i}
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      transition={{ delay: i * 0.1, duration: 0.3 }}
                    >
                      <div
                        className="w-6 h-6 border"
                        style={{
                          background: swatch.color,
                          borderColor: 'var(--color-stroke)',
                        }}
                      />
                      <div
                        style={{
                          fontFamily: 'var(--font-family-mono)',
                          fontSize: '8px',
                          color: 'var(--color-gray)',
                          marginTop: '2px',
                          textAlign: 'center',
                        }}
                      >
                        {swatch.label}
                      </div>
                    </motion.div>
                  ))}
                </motion.div>
              )}

              {/* Widget shapes assembling */}
              <div className="relative w-full h-full p-8">
                {[
                  { x: 20, y: 30, w: 80, h: 60 },
                  { x: 120, y: 40, w: 100, h: 80 },
                  { x: 40, y: 140, w: 120, h: 50 },
                ].map((shape, i) => (
                  showConstruction && (
                    <motion.div
                      key={i}
                      className="absolute border"
                      style={{
                        left: shape.x,
                        top: shape.y,
                        width: shape.w,
                        height: shape.h,
                        borderColor: 'var(--color-terminal-green)',
                      }}
                      initial={{ opacity: 0, scale: 0.8 }}
                      animate={{ opacity: 0.4, scale: 1 }}
                      transition={{ delay: 0.3 + i * 0.2, duration: 0.5 }}
                    />
                  )
                ))}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Top Status Bar */}
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
          <motion.div
            className="w-1.5 h-1.5 rounded-full"
            style={{ background: 'var(--color-terminal-green)' }}
            animate={{ opacity: [1, 0.3, 1] }}
            transition={{ duration: 1.5, repeat: Infinity }}
          />
          <span>{Math.round(progress)}%</span>
        </div>
      </div>

      {/* Terminal Log - Bottom Left */}
      <motion.div
        className="fixed bottom-8 left-8 z-20 border max-w-[500px] max-h-[300px] overflow-y-auto"
        style={{
          background: 'rgba(255, 255, 255, 0.95)',
          borderColor: 'var(--color-stroke)',
        }}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5, duration: 0.6 }}
      >
        <div className="p-4 space-y-1">
          {messages.map((msg, i) => (
            <motion.div
              key={i}
              className="flex items-start gap-3"
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3 }}
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
                {msg.text.startsWith('✓') ? '✓' : '▸'}
              </span>
              <span>{msg.text.replace(/^[▸✓]\s*/, '')}</span>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}
