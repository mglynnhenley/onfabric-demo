import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Info, X } from 'lucide-react';
import { PipelineStage } from './PipelineStage';
import { SystemsDiagram } from './SystemsDiagram';
import type { LoadingState, PipelineStageConfig } from './types';

interface LoadingOverlayProps {
  show: boolean;
  progress: LoadingState;
  onComplete?: () => void;
}

const PIPELINE_STAGES: PipelineStageConfig[] = [
  {
    id: 'data',
    title: 'Data Fetch',
    icon: 'D',
    websocketStep: ['data', 'initializing'],
  },
  {
    id: 'patterns',
    title: 'Persona Detection',
    icon: 'P',
    websocketStep: ['patterns', 'patterns_complete'],
  },
  {
    id: 'theme',
    title: 'Theme Generation',
    icon: 'T',
    websocketStep: ['theme', 'theme_complete'],
  },
  {
    id: 'widgets',
    title: 'Component Selection',
    icon: 'C',
    websocketStep: ['widgets', 'widgets_complete'],
  },
  {
    id: 'enrichment',
    title: 'API Enrichment',
    icon: 'A',
    websocketStep: ['search', 'enriching', 'content'],
  },
  {
    id: 'building',
    title: 'Dashboard Assembly',
    icon: 'B',
    websocketStep: ['building'],
  },
];

export const LoadingOverlay = ({ show, progress, onComplete }: LoadingOverlayProps) => {
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });
  const [showDiagram, setShowDiagram] = useState(false);

  // Keep overlay visible if diagram is open, even if loading completes
  const shouldShowOverlay = show || showDiagram;

  // Color constants for animations (matching Landing page)
  const COLORS = {
    crimson: '#DC143C',
    terminalGreen: '#00AA2E',
    stroke: '#E5E5E5',
    charcoal: '#2B2726',
  };

  // Track mouse position for subtle parallax
  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setMousePos({
        x: (e.clientX / window.innerWidth - 0.5) * 10,
        y: (e.clientY / window.innerHeight - 0.5) * 10
      });
    };

    if (shouldShowOverlay) {
      window.addEventListener('mousemove', handleMouseMove);
      return () => window.removeEventListener('mousemove', handleMouseMove);
    }
  }, [shouldShowOverlay]);

  // Determine active stage index for dot animation
  const activeStageIndex = PIPELINE_STAGES.findIndex(
    stage => progress.stageStatuses[stage.id as keyof typeof progress.stageStatuses] === 'active'
  );

  return (
    <AnimatePresence>
      {shouldShowOverlay && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 z-50 overflow-y-auto"
          style={{
            background: 'var(--color-paper)',
            fontFamily: 'var(--font-family-mono)'
          }}
        >
          {/* Animated dot grid background - pulse near active stage */}
          <div className="fixed inset-0 pointer-events-none overflow-hidden" style={{ zIndex: 1 }}>
            {[...Array(120)].map((_, i) => {
              const gridCols = 15;
              const gridRows = 8;
              const col = i % gridCols;
              const row = Math.floor(i / gridCols);
              const dotX = (col / (gridCols - 1)) * 100;
              const dotY = (row / (gridRows - 1)) * 100;

              // Calculate distance from active stage position
              const stageY = activeStageIndex >= 0 ? (activeStageIndex / PIPELINE_STAGES.length) * 100 : 50;
              const distance = Math.abs(dotY - stageY);
              const isNearActive = distance < 25;

              return (
                <motion.div
                  key={i}
                  className="absolute rounded-full"
                  style={{
                    left: `${dotX}%`,
                    top: `${dotY}%`,
                    width: '3px',
                    height: '3px',
                  }}
                  animate={{
                    backgroundColor: isNearActive
                      ? [COLORS.stroke, COLORS.crimson, COLORS.terminalGreen, COLORS.stroke]
                      : COLORS.stroke,
                    scale: isNearActive ? [1, 1.3, 1] : 1,
                    opacity: isNearActive ? [0.2, 0.6, 0.2] : 0.15,
                  }}
                  transition={{
                    duration: 2,
                    repeat: Infinity,
                    delay: i * 0.01,
                    ease: 'easeInOut',
                  }}
                />
              );
            })}
          </div>

          {/* Subtle paper texture */}
          <div
            className="fixed inset-0 pointer-events-none opacity-20"
            style={{
              zIndex: 1,
              backgroundImage: `url("data:image/svg+xml,%3Csvg width='100' height='100' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence baseFrequency='0.9' /%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03' /%3E%3C/svg%3E")`,
            }}
          />

          {/* Terminal grid */}
          <div
            className="fixed inset-0 pointer-events-none opacity-5"
            style={{
              zIndex: 1,
              backgroundImage: `
                linear-gradient(to right, var(--color-stroke) 1px, transparent 1px),
                linear-gradient(to bottom, var(--color-stroke) 1px, transparent 1px)
              `,
              backgroundSize: '40px 40px',
            }}
          />

          {/* Geometric elements */}
          <div
            className="fixed"
            style={{
              zIndex: 1,
              top: '15%',
              right: '10%',
              width: '80px',
              height: '80px',
              borderRadius: '50%',
              background: 'var(--color-crimson)',
              opacity: 0.1,
              transform: `translate(${mousePos.x}px, ${mousePos.y}px)`,
              transition: 'transform 0.3s ease-out',
            }}
          />

          <div
            className="fixed"
            style={{
              zIndex: 1,
              bottom: '20%',
              left: '8%',
              width: '60px',
              height: '60px',
              border: '1px solid var(--color-terminal-green)',
              opacity: 0.2,
              transform: `rotate(${progress.percent * 3.6}deg) translate(${-mousePos.x}px, ${-mousePos.y}px)`,
              transition: 'transform 0.5s ease-out',
            }}
          />

          <div className="relative z-10 min-h-screen flex flex-col items-center justify-start py-12 px-4">
            {/* Info Button */}
            <motion.button
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.5 }}
              onClick={() => setShowDiagram(true)}
              className="fixed top-6 right-6 z-20 p-3 rounded-full"
              style={{
                backgroundColor: 'var(--color-paper)',
                border: '2px solid var(--color-crimson)',
                boxShadow: '0 4px 20px rgba(220, 20, 60, 0.2)',
              }}
              whileHover={{
                scale: 1.1,
                boxShadow: '0 6px 30px rgba(220, 20, 60, 0.3)',
              }}
              whileTap={{ scale: 0.95 }}
            >
              <Info size={20} color="var(--color-crimson)" />
            </motion.button>

            {/* Systems Diagram Modal */}
            <AnimatePresence>
              {showDiagram && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="fixed inset-0 z-50 flex items-center justify-center p-4"
                  style={{ backgroundColor: 'rgba(0, 0, 0, 0.7)' }}
                  onClick={() => setShowDiagram(false)}
                >
                  <motion.div
                    initial={{ scale: 0.8, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    exit={{ scale: 0.8, opacity: 0 }}
                    transition={{ type: 'spring', stiffness: 200, damping: 20 }}
                    className="relative max-w-4xl w-full max-h-[90vh] overflow-auto rounded-lg"
                    style={{
                      backgroundColor: 'var(--color-paper)',
                      border: '2px solid var(--color-crimson)',
                      boxShadow: '0 20px 60px rgba(0, 0, 0, 0.5)',
                    }}
                    onClick={(e) => e.stopPropagation()}
                  >
                    <button
                      onClick={() => setShowDiagram(false)}
                      className="absolute top-4 right-4 z-10 p-2 rounded-full"
                      style={{
                        backgroundColor: 'var(--color-crimson)',
                        color: 'var(--color-paper)',
                      }}
                    >
                      <X size={20} />
                    </button>
                    <SystemsDiagram />
                  </motion.div>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Header with typing animation */}
            <motion.div
              initial={{ y: -20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              className="text-center mb-12 w-full max-w-3xl"
            >
              {/* Terminal prompt style */}
              <div
                className="mb-8 text-left inline-block"
                style={{
                  fontFamily: 'var(--font-family-mono)',
                  fontSize: '14px',
                  color: 'var(--color-gray)',
                }}
              >
                <span style={{ color: 'var(--color-terminal-green)' }}>▸ </span>
                <span className="typing-text">system.build_dashboard()</span>
                <span className="animate-blink">_</span>
              </div>

              <h1
                className="text-5xl mb-3"
                style={{
                  fontFamily: 'var(--font-family-serif)',
                  color: 'var(--color-charcoal)',
                  fontWeight: 300,
                  letterSpacing: '-0.02em'
                }}
              >
                Crafting Your
                <br />
                <span style={{ color: 'var(--color-crimson)' }}>
                  Personalized
                </span> Experience
              </h1>

              {/* Stage Progress Dots instead of bar */}
              <div className="flex items-center justify-center gap-3 mb-8">
                {PIPELINE_STAGES.map((stage, index) => {
                  const stageStatus = progress.stageStatuses[stage.id as keyof typeof progress.stageStatuses];
                  return (
                    <motion.div
                      key={stage.id}
                      initial={{ scale: 0, opacity: 0 }}
                      animate={{ scale: 1, opacity: 1 }}
                      transition={{ delay: index * 0.05 }}
                      className="relative"
                    >
                      <motion.div
                        className="w-2 h-2 rounded-full"
                        style={{
                          backgroundColor: stageStatus === 'complete'
                            ? COLORS.terminalGreen
                            : stageStatus === 'active'
                            ? COLORS.crimson
                            : COLORS.stroke,
                        }}
                        animate={stageStatus === 'active' ? {
                          scale: [1, 1.5, 1],
                        } : {}}
                        transition={{
                          duration: 1,
                          repeat: Infinity,
                          ease: 'easeInOut'
                        }}
                      />
                      {stageStatus === 'active' && (
                        <motion.div
                          className="absolute inset-0 rounded-full"
                          style={{
                            backgroundColor: COLORS.crimson,
                            opacity: 0.3
                          }}
                          animate={{
                            scale: [1, 2.5, 1],
                            opacity: [0.3, 0, 0.3]
                          }}
                          transition={{
                            duration: 1.5,
                            repeat: Infinity,
                            ease: 'easeOut'
                          }}
                        />
                      )}
                    </motion.div>
                  );
                })}
              </div>

              {/* Current Step Explanation */}
              <div className="text-center space-y-3 max-w-2xl mx-auto">
                <motion.div
                  key={progress.message}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="text-base"
                  style={{
                    fontFamily: 'var(--font-family-mono)',
                    color: 'var(--color-charcoal)',
                    letterSpacing: '0.02em',
                    lineHeight: 1.6
                  }}
                >
                  {progress.message || '> Initializing pipeline...'}
                </motion.div>

                {/* Show persona card when detected */}
                {progress.stageData.patterns?.persona && (
                  <motion.div
                    initial={{ scale: 0.8, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    transition={{ type: 'spring', stiffness: 200, damping: 20 }}
                    className="mx-auto mt-8 mb-6 p-6 rounded-lg max-w-xl"
                    style={{
                      background: 'linear-gradient(135deg, rgba(220, 20, 60, 0.05), rgba(0, 170, 46, 0.05))',
                      border: '2px solid var(--color-crimson)',
                      boxShadow: '0 10px 40px rgba(220, 20, 60, 0.15)',
                    }}
                  >
                    <div
                      className="text-sm uppercase tracking-wider mb-3"
                      style={{
                        color: 'var(--color-crimson)',
                        fontFamily: 'var(--font-family-mono)',
                        fontWeight: 600,
                      }}
                    >
                      Persona Detected
                    </div>

                    <motion.p
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: 0.3 }}
                      className="text-lg mb-4"
                      style={{
                        fontFamily: 'var(--font-family-serif)',
                        color: 'var(--color-charcoal)',
                        lineHeight: 1.6,
                        fontStyle: 'italic',
                      }}
                    >
                      "{progress.stageData.patterns.persona.professional_context || progress.stageData.patterns.persona.writing_style}"
                    </motion.p>

                    {progress.stageData.patterns.persona.interests && (
                      <div className="flex flex-wrap gap-2 justify-center">
                        {progress.stageData.patterns.persona.interests.slice(0, 5).map((interest: string, idx: number) => (
                          <motion.span
                            key={interest}
                            initial={{ scale: 0, rotate: -10 }}
                            animate={{ scale: 1, rotate: 0 }}
                            transition={{ delay: 0.4 + idx * 0.1, type: 'spring' }}
                            className="px-3 py-1 text-xs rounded-full"
                            style={{
                              backgroundColor: idx % 2 === 0 ? 'rgba(220, 20, 60, 0.1)' : 'rgba(0, 170, 46, 0.1)',
                              border: `1px solid ${idx % 2 === 0 ? 'var(--color-crimson)' : 'var(--color-terminal-green)'}`,
                              fontFamily: 'var(--font-family-mono)',
                            }}
                          >
                            {interest}
                          </motion.span>
                        ))}
                      </div>
                    )}

                    {/* Tone and Content Depth */}
                    {(progress.stageData.patterns.persona.tone_preference || progress.stageData.patterns.persona.content_depth_preference) && (
                      <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.8 }}
                        className="mt-4 pt-4 border-t space-y-2"
                        style={{ borderColor: 'rgba(220, 20, 60, 0.2)' }}
                      >
                        {progress.stageData.patterns.persona.tone_preference && (
                          <div className="text-xs" style={{ fontFamily: 'var(--font-family-mono)', color: 'var(--color-gray)' }}>
                            <span style={{ color: 'var(--color-crimson)', fontWeight: 600 }}>Tone:</span> {progress.stageData.patterns.persona.tone_preference}
                          </div>
                        )}
                        {progress.stageData.patterns.persona.content_depth_preference && (
                          <div className="text-xs" style={{ fontFamily: 'var(--font-family-mono)', color: 'var(--color-gray)' }}>
                            <span style={{ color: 'var(--color-terminal-green)', fontWeight: 600 }}>Content Depth:</span> {progress.stageData.patterns.persona.content_depth_preference}
                          </div>
                        )}
                      </motion.div>
                    )}
                  </motion.div>
                )}

                {/* Detailed explanation based on active stage */}
                {(() => {
                  const activeStage = PIPELINE_STAGES.find(
                    stage => progress.stageStatuses[stage.id as keyof typeof progress.stageStatuses] === 'active'
                  );

                  const explanations: Record<string, string> = {
                    data: "Analyzing your digital interactions across platforms to understand your unique patterns and preferences.",
                    patterns: "Using machine learning to identify your interests, communication style, and behavioral patterns.",
                    theme: "Generating a visual aesthetic that reflects your personality—colors, typography, and design elements.",
                    widgets: "Selecting the perfect UI components based on your interests—maps for travelers, videos for learners, events for socializers.",
                    enrichment: "Connecting to live APIs to bring real-time data into your dashboard—weather, events, videos, and more.",
                    building: "Assembling everything into a cohesive, beautiful dashboard that feels uniquely yours."
                  };

                  return activeStage && !progress.stageData.patterns?.persona ? (
                    <motion.p
                      key={activeStage.id}
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: 0.2 }}
                      className="text-sm"
                      style={{
                        fontFamily: 'var(--font-family-sans)',
                        color: 'var(--color-gray)',
                        maxWidth: '600px',
                        margin: '0 auto',
                        lineHeight: 1.6
                      }}
                    >
                      {explanations[activeStage.id]}
                    </motion.p>
                  ) : null;
                })()}
              </div>
            </motion.div>

            {/* Pipeline Stages with enhanced design */}
            <div className="w-full max-w-3xl space-y-6">
              {PIPELINE_STAGES.map((stage, index) => (
                <React.Fragment key={stage.id}>
                  <motion.div
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                  >
                    <PipelineStage
                      id={stage.id}
                      title={stage.title}
                      icon={stage.icon}
                      status={progress.stageStatuses[stage.id as keyof typeof progress.stageStatuses]}
                      data={progress.stageData[stage.id as keyof typeof progress.stageData]}
                      index={index}
                    />
                  </motion.div>

                  {/* Enhanced arrow connector */}
                  {index < PIPELINE_STAGES.length - 1 && (
                    <div className="flex justify-center">
                      <motion.div
                        className="relative"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: index * 0.1 + 0.05 }}
                      >
                        <div
                          className="relative w-0.5 h-8"
                          style={{
                            background: progress.stageStatuses[PIPELINE_STAGES[index + 1].id as keyof typeof progress.stageStatuses] !== 'pending'
                              ? `linear-gradient(180deg, ${COLORS.terminalGreen}, ${COLORS.crimson})`
                              : 'var(--color-stroke)'
                          }}
                        >
                          <motion.div
                            className="absolute bottom-0 left-1/2 -translate-x-1/2 translate-y-1"
                            animate={{
                              y: progress.stageStatuses[PIPELINE_STAGES[index + 1].id as keyof typeof progress.stageStatuses] !== 'pending'
                                ? [1, 4, 1]
                                : 1
                            }}
                            transition={{
                              duration: 1,
                              repeat: Infinity,
                              ease: 'easeInOut'
                            }}
                            style={{
                              width: 0,
                              height: 0,
                              borderLeft: '5px solid transparent',
                              borderRight: '5px solid transparent',
                              borderTop: `5px solid ${
                                progress.stageStatuses[PIPELINE_STAGES[index + 1].id as keyof typeof progress.stageStatuses] !== 'pending'
                                  ? COLORS.crimson
                                  : 'var(--color-stroke)'
                              }`,
                            }}
                          />
                        </div>
                      </motion.div>
                    </div>
                  )}
                </React.Fragment>
              ))}
            </div>

            {/* Next Button - appears when generation is complete */}
            <AnimatePresence>
              {progress.percent === 100 && onComplete && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 20 }}
                  transition={{ delay: 0.5, type: 'spring', stiffness: 200, damping: 20 }}
                  className="mt-8 flex justify-center"
                >
                  <motion.button
                    onClick={onComplete}
                    className="px-8 py-4 text-lg font-semibold rounded-lg"
                    style={{
                      backgroundColor: 'var(--color-crimson)',
                      color: 'var(--color-paper)',
                      fontFamily: 'var(--font-family-mono)',
                      border: '2px solid var(--color-crimson)',
                      boxShadow: '0 8px 24px rgba(220, 20, 60, 0.3)',
                      letterSpacing: '0.05em',
                    }}
                    whileHover={{
                      scale: 1.05,
                      boxShadow: '0 12px 32px rgba(220, 20, 60, 0.4)',
                      y: -2,
                    }}
                    whileTap={{
                      scale: 0.95,
                    }}
                  >
                    <span className="flex items-center gap-2">
                      <span>Continue to Dashboard</span>
                      <motion.span
                        animate={{ x: [0, 4, 0] }}
                        transition={{ repeat: Infinity, duration: 1.5, ease: 'easeInOut' }}
                      >
                        →
                      </motion.span>
                    </span>
                  </motion.button>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Status bar at bottom */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.8 }}
              className="mt-12 pt-6 border-t w-full max-w-3xl"
              style={{
                borderColor: 'var(--color-stroke)',
                fontFamily: 'var(--font-family-mono)',
                fontSize: '12px',
                color: 'var(--color-gray)',
                letterSpacing: '0.05em',
              }}
            >
              <div className="flex items-center gap-6">
                <div className="flex items-center gap-2">
                  <motion.div
                    className="w-2 h-2 rounded-full"
                    style={{ background: 'var(--color-terminal-green)' }}
                    animate={{
                      scale: [1, 1.2, 1],
                      opacity: [0.8, 1, 0.8]
                    }}
                    transition={{
                      duration: 2,
                      repeat: Infinity,
                      ease: 'easeInOut'
                    }}
                  />
                  <span>processing</span>
                </div>
                <div>·</div>
                <div>real-time</div>
                <div>·</div>
                <div>adaptive_ui</div>
              </div>
            </motion.div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};
