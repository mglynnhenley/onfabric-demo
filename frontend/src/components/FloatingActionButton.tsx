/**
 * Floating Action Button (FAB) Component
 *
 * Circular button with icon, tooltip, and smooth animations
 */

import { motion } from 'framer-motion';
import { useState } from 'react';

interface FloatingActionButtonProps {
  icon: React.ReactNode;
  onClick: () => void;
  tooltip: string;
  primary?: boolean;
}

export function FloatingActionButton({
  icon,
  onClick,
  tooltip,
  primary = false,
}: FloatingActionButtonProps) {
  const [showTooltip, setShowTooltip] = useState(false);

  return (
    <div
      className="relative"
      onMouseEnter={() => setShowTooltip(true)}
      onMouseLeave={() => setShowTooltip(false)}
    >
      {/* Tooltip */}
      {showTooltip && (
        <motion.div
          initial={{ opacity: 0, x: 10 }}
          animate={{ opacity: 1, x: 0 }}
          className="absolute right-16 top-1/2 -translate-y-1/2 px-3 py-2 rounded-lg text-sm font-medium whitespace-nowrap pointer-events-none shadow-lg"
          style={{
            backgroundColor: 'var(--card-background)',
            color: 'var(--color-foreground)',
            backdropFilter: 'blur(12px)',
          }}
        >
          {tooltip}
        </motion.div>
      )}

      {/* FAB Button */}
      <motion.button
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.95 }}
        onClick={onClick}
        className="w-14 h-14 rounded-full flex items-center justify-center shadow-lg transition-all"
        style={{
          backgroundColor: primary
            ? 'var(--color-primary)'
            : 'var(--card-background)',
          color: primary ? '#ffffff' : 'var(--color-foreground)',
          backdropFilter: 'blur(12px)',
        }}
      >
        {icon}
      </motion.button>
    </div>
  );
}
