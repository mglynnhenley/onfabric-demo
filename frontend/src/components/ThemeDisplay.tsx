/**
 * Theme display - Enhanced design for color scheme.
 */

import { motion } from 'framer-motion';
import type { ThemeData } from '../types';

interface ThemeDisplayProps {
  theme: ThemeData;
}

export function ThemeDisplay({ theme }: ThemeDisplayProps) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
      whileHover={{ scale: 1.02 }}
      className="bg-white border-2 border-warm-gray rounded-2xl p-6 shadow-editorial hover:shadow-editorial-lg transition-all"
    >
      <h3 className="font-display text-xl font-bold text-charcoal mb-5">
        Color Theme
      </h3>

      <div className="flex items-start gap-5 mb-5">
        {/* Color Swatch */}
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ duration: 0.5, type: "spring", delay: 0.2 }}
          className="relative"
        >
          <div
            className="w-24 h-24 rounded-2xl shadow-editorial-lg border-2 border-warm-gray"
            style={{ backgroundColor: theme.primary }}
          />
          <motion.div
            animate={{ scale: [1, 1.2, 1] }}
            transition={{ duration: 2, repeat: Infinity }}
            className="absolute -top-1 -right-1 w-4 h-4 bg-terracotta rounded-full"
          />
        </motion.div>

        {/* Theme Info */}
        <div className="flex-1">
          <div className="mb-3">
            <div className="text-xs text-charcoal/50 mb-1 uppercase tracking-wide">Mood</div>
            <div className="font-semibold text-lg text-charcoal capitalize">
              {theme.mood}
            </div>
          </div>
          <div>
            <div className="text-xs text-charcoal/50 mb-1 uppercase tracking-wide">Color Code</div>
            <div className="font-mono text-sm text-charcoal/70 bg-warm-gray/50 px-3 py-1 rounded-lg inline-block">
              {theme.primary}
            </div>
          </div>
        </div>
      </div>

      {/* Rationale */}
      {theme.rationale && (
        <div className="pt-4 border-t border-warm-gray">
          <p className="text-sm text-charcoal/60 leading-relaxed">
            {theme.rationale}
          </p>
        </div>
      )}
    </motion.div>
  );
}
