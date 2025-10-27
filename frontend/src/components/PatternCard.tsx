/**
 * Pattern card - Enhanced with better visual design.
 */

import { motion } from 'framer-motion';
import type { Pattern } from '../types';

interface PatternCardProps {
  pattern: Pattern;
  index: number;
}

export function PatternCard({ pattern, index }: PatternCardProps) {
  const confidencePercent = Math.round(pattern.confidence * 100);

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.4, delay: index * 0.1 }}
      whileHover={{ scale: 1.02 }}
      className="bg-white border-2 border-warm-gray rounded-2xl p-6 shadow-editorial hover:shadow-editorial-lg transition-all group"
    >
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <h3 className="font-display text-lg font-bold text-charcoal group-hover:text-terracotta transition-colors">
            {pattern.title}
          </h3>
        </div>
        <div className="flex items-center gap-2 px-3 py-1 bg-gradient-to-br from-terracotta/10 to-transparent rounded-full border border-terracotta/20">
          <span className="text-sm font-bold text-terracotta">
            {confidencePercent}%
          </span>
        </div>
      </div>

      <p className="text-sm text-charcoal/60 leading-relaxed mb-4">
        {pattern.description}
      </p>

      {/* Enhanced progress bar */}
      <div className="relative h-2 bg-warm-gray rounded-full overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${confidencePercent}%` }}
          transition={{ duration: 1, delay: index * 0.1 + 0.3, ease: "easeOut" }}
          className="h-full bg-gradient-to-r from-terracotta to-accent-sage rounded-full relative"
        >
          <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent animate-shimmer" />
        </motion.div>
      </div>
    </motion.div>
  );
}
