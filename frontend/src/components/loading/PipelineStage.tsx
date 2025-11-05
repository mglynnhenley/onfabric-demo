import { memo } from 'react';
import { motion } from 'framer-motion';
import { Check } from 'lucide-react';
import { StageDetail } from './StageDetail';
import type { StageStatus, StageData } from './types';

interface PipelineStageProps {
  id: string;
  title: string;
  icon: string;
  status: StageStatus;
  data?: StageData[keyof StageData];
  index: number;
}

export const PipelineStage = memo(({
  id,
  title,
  icon,
  status,
  data,
  index,
}: PipelineStageProps) => {
  const getStatusStyles = () => {
    switch (status) {
      case 'active':
        return {
          borderColor: 'var(--color-crimson)',
          backgroundColor: 'rgba(220, 20, 60, 0.03)',
          boxShadow: '0 0 0 1px var(--color-crimson), 8px 8px 0 rgba(220, 20, 60, 0.1)',
          transform: 'translate(-2px, -2px)',
        };
      case 'complete':
        return {
          borderColor: 'var(--color-terminal-green)',
          backgroundColor: 'var(--color-paper)',
          boxShadow: '0 0 0 1px var(--color-terminal-green)',
        };
      case 'pending':
      default:
        return {
          borderColor: 'var(--color-stroke)',
          backgroundColor: 'var(--color-paper)',
          opacity: 0.5,
        };
    }
  };

  const getStatusIndicator = () => {
    switch (status) {
      case 'active':
        return (
          <motion.div className="relative">
            <motion.div
              className="w-4 h-4 rounded-full"
              style={{ backgroundColor: 'var(--color-crimson)' }}
              animate={{
                scale: [1, 1.3, 1],
                opacity: [1, 0.8, 1]
              }}
              transition={{ repeat: Infinity, duration: 1.5, ease: 'easeInOut' }}
            />
            <motion.div
              className="absolute inset-0 rounded-full"
              style={{
                backgroundColor: 'var(--color-crimson)',
                opacity: 0.4
              }}
              animate={{
                scale: [1, 1.8, 1],
                opacity: [0.4, 0, 0.4]
              }}
              transition={{ repeat: Infinity, duration: 1.5, ease: 'easeOut' }}
            />
          </motion.div>
        );
      case 'complete':
        return (
          <motion.div
            initial={{ scale: 0, rotate: -180 }}
            animate={{ scale: 1, rotate: 0 }}
            transition={{ type: 'spring', stiffness: 300, damping: 20 }}
            className="relative"
          >
            <div
              className="w-6 h-6 rounded-full flex items-center justify-center"
              style={{
                backgroundColor: 'var(--color-terminal-green)',
              }}
            >
              <Check size={14} color="var(--color-white)" strokeWidth={3} />
            </div>
          </motion.div>
        );
      case 'pending':
      default:
        return (
          <div className="relative">
            <div
              className="w-4 h-4 border-2 rounded-full"
              style={{ borderColor: 'var(--color-stroke)' }}
            />
            <motion.div
              className="absolute inset-0 w-4 h-4 border-t-2 rounded-full"
              style={{ borderColor: 'var(--color-gray)' }}
              animate={{ rotate: 360 }}
              transition={{ repeat: Infinity, duration: 3, ease: 'linear' }}
            />
          </div>
        );
    }
  };

  const getTerminalPrompt = () => {
    switch (status) {
      case 'active':
        return '▸ processing';
      case 'complete':
        return '✓ complete';
      case 'pending':
      default:
        return '○ waiting';
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, x: -30 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: index * 0.08, duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
      className="relative border-2 p-5 transition-all duration-300"
      style={{
        ...getStatusStyles(),
        fontFamily: 'var(--font-family-mono)',
      }}
      whileHover={status === 'active' ? {
        x: 2,
        y: -2,
        boxShadow: '0 0 0 1px var(--color-crimson), 12px 12px 0 rgba(220, 20, 60, 0.15)',
      } : undefined}
    >
      {/* Terminal-style header */}
      <div className="mb-4">
        <div
          className="text-xs mb-2"
          style={{
            color: status === 'active' ? 'var(--color-crimson)' :
                   status === 'complete' ? 'var(--color-terminal-green)' :
                   'var(--color-gray)',
            letterSpacing: '0.05em',
            fontWeight: 500,
          }}
        >
          {getTerminalPrompt()}
        </div>

        {/* Main header row */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div>
              <h3
                className="font-semibold text-lg"
                style={{
                  color: 'var(--color-charcoal)',
                  letterSpacing: '-0.01em'
                }}
              >
                {title}
              </h3>
              {status === 'active' && (
                <motion.div
                  initial={{ opacity: 0, y: -5 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="text-xs mt-1"
                  style={{ color: 'var(--color-gray)' }}
                >
                  <span className="animate-pulse">executing...</span>
                </motion.div>
              )}
            </div>
          </div>
          <div className="flex items-center gap-2">
            {getStatusIndicator()}
          </div>
        </div>
      </div>

      {/* Detail Content with animation */}
      <motion.div
        initial={false}
        animate={{
          height: status === 'pending' ? 0 : 'auto',
          opacity: status === 'pending' ? 0 : 1,
        }}
        transition={{ duration: 0.3, ease: 'easeOut' }}
        className="overflow-hidden"
      >
        <div
          className="border-t pt-3"
          style={{
            borderColor: 'var(--color-stroke)',
            color: 'var(--color-charcoal)',
            fontSize: '13px',
          }}
        >
          <StageDetail type={id} data={data} status={status} />
        </div>
      </motion.div>

      {/* Progress indicator for active stage */}
      {status === 'active' && (
        <motion.div
          className="absolute bottom-0 left-0 h-0.5"
          style={{ backgroundColor: 'var(--color-crimson)' }}
          initial={{ width: 0 }}
          animate={{ width: '100%' }}
          transition={{ duration: 3, ease: 'linear' }}
        />
      )}
    </motion.div>
  );
});

PipelineStage.displayName = 'PipelineStage';
