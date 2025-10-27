/**
 * Progress screen - Immersive full-bleed experience.
 */

import { motion, AnimatePresence } from 'framer-motion';
import { PatternCard } from './PatternCard';
import { ThemeDisplay } from './ThemeDisplay';
import { WidgetGrid } from './WidgetGrid';
import type { IntelligenceData } from '../types';

interface ProgressProps {
  progress: number;
  currentStep: string;
  currentMessage: string;
  intelligence: IntelligenceData;
}

export function Progress({ progress, currentStep, currentMessage, intelligence }: ProgressProps) {
  const showPatterns = intelligence.patterns.length > 0;
  const showTheme = intelligence.theme !== null;
  const showWidgets = intelligence.widgets.length > 0;
  const showData = intelligence.interactions > 0;

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Full-bleed progress bar background */}
      <div className="fixed inset-0 pointer-events-none">
        <motion.div
          className="absolute inset-0 bg-gradient-to-br from-terracotta/5 via-transparent to-teal/5"
          animate={{
            opacity: [0.3, 0.5, 0.3],
          }}
          transition={{ duration: 3, repeat: Infinity }}
        />

        {/* Animated progress-based gradient */}
        <motion.div
          className="absolute inset-0 bg-gradient-to-r from-terracotta/10 via-amber/8 to-teal/10"
          initial={{ x: '-100%' }}
          animate={{ x: `${progress - 100}%` }}
          transition={{ duration: 0.8, ease: "easeOut" }}
        />
      </div>

      {/* Left sidebar progress indicator */}
      <div className="fixed left-0 top-0 bottom-0 w-1 bg-warm-gray/30 z-20">
        <motion.div
          className="absolute left-0 top-0 w-full bg-gradient-to-b from-terracotta via-amber to-teal"
          initial={{ height: '0%' }}
          animate={{ height: `${progress}%` }}
          transition={{ duration: 0.5, ease: "easeOut" }}
        />
      </div>

      <div className="relative z-10 min-h-screen flex flex-col">
        {/* Top status bar */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="px-12 py-8 flex items-center justify-between"
        >
          <div className="flex items-center gap-6">
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
              className="w-12 h-12 rounded-full border-2 border-warm-gray border-t-terracotta"
            />
            <div>
              <h1 className="text-3xl font-serif font-semibold text-charcoal">
                AI Generation in Progress
              </h1>
              <motion.p
                key={currentMessage}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                className="text-charcoal/60 font-mono text-sm mt-1"
              >
                {currentMessage}
              </motion.p>
            </div>
          </div>

          <div className="text-right">
            <div className="text-5xl font-serif font-semibold text-charcoal">
              {progress}
              <span className="text-2xl text-charcoal/40">%</span>
            </div>
            <div className="text-xs font-mono text-charcoal/40 mt-1">
              {currentStep}
            </div>
          </div>
        </motion.div>

        {/* Main content area - centered and spacious */}
        <div className="flex-1 px-12 pb-12">
          {/* Intelligence display - flowing layout */}
          <div className="max-w-[1600px] mx-auto space-y-8">

            {/* Data stats - horizontal flow */}
            <AnimatePresence>
              {showData && (
                <motion.div
                  initial={{ opacity: 0, y: 30 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0 }}
                  className="flex items-center gap-12"
                >
                  <div>
                    <div className="text-6xl font-serif font-semibold gradient-text mb-2">
                      {intelligence.interactions}
                    </div>
                    <div className="text-sm text-charcoal/50 font-mono">Interactions analyzed</div>
                  </div>

                  <div className="h-16 w-px bg-warm-gray" />

                  <div>
                    <div className="text-4xl font-serif font-semibold text-charcoal mb-2">
                      {intelligence.platforms.length}
                    </div>
                    <div className="text-sm text-charcoal/50 font-mono">Platforms</div>
                  </div>

                  {intelligence.platforms.length > 0 && (
                    <>
                      <div className="h-16 w-px bg-warm-gray" />
                      <div className="flex flex-wrap gap-3">
                        {intelligence.platforms.map((platform, i) => (
                          <motion.span
                            key={platform}
                            initial={{ opacity: 0, scale: 0.8 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ delay: i * 0.1 }}
                            className="px-4 py-2 glass rounded-full text-charcoal/70 font-mono text-xs capitalize shadow-warm"
                          >
                            {platform}
                          </motion.span>
                        ))}
                      </div>
                    </>
                  )}
                </motion.div>
              )}
            </AnimatePresence>

            {/* Patterns - masonry style */}
            <AnimatePresence>
              {showPatterns && (
                <motion.div
                  initial={{ opacity: 0, y: 30 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0 }}
                  className="space-y-4"
                >
                  <h2 className="text-2xl font-serif font-semibold text-charcoal">
                    Patterns Discovered
                  </h2>
                  <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-5">
                    {intelligence.patterns.map((pattern, index) => (
                      <PatternCard key={index} pattern={pattern} index={index} />
                    ))}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Theme & Widgets */}
            <div className="grid lg:grid-cols-2 gap-8">
              <AnimatePresence>
                {showTheme && intelligence.theme && (
                  <ThemeDisplay theme={intelligence.theme} />
                )}
              </AnimatePresence>

              <AnimatePresence>
                {showWidgets && (
                  <WidgetGrid widgets={intelligence.widgets} />
                )}
              </AnimatePresence>
            </div>

            {/* Cards preview - horizontal scroll */}
            <AnimatePresence>
              {intelligence.cards.length > 0 && (
                <motion.div
                  initial={{ opacity: 0, y: 30 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0 }}
                  className="space-y-4"
                >
                  <h3 className="text-2xl font-serif font-semibold text-charcoal">
                    Content Generated
                  </h3>
                  <div className="flex gap-4 overflow-x-auto pb-4 -mx-12 px-12">
                    {intelligence.cards.slice(0, 5).map((card, index) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.1 }}
                        className="flex-shrink-0 w-64 glass rounded-2xl p-5 shadow-warm hover-lift"
                      >
                        <div className="flex items-start gap-3">
                          <div className="flex-shrink-0 w-6 h-6 rounded-full bg-gradient-to-br from-terracotta/30 to-amber/20 flex items-center justify-center">
                            <svg className="w-3 h-3 text-terracotta" fill="currentColor" viewBox="0 0 20 20">
                              <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                            </svg>
                          </div>
                          <span className="text-sm font-medium text-charcoal line-clamp-3 leading-relaxed">
                            {card.title}
                          </span>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </div>
    </div>
  );
}
