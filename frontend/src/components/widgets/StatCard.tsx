/**
 * StatCard Widget
 *
 * Displays a statistic with title, value, and optional change indicator.
 * Uses shadcn-style card design with Framer Motion animations.
 */

import { motion } from 'framer-motion';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { registerWidget } from './WidgetRegistry';
import type { WidgetProps } from './WidgetTypes';
import { useEffect } from 'react';

interface StatCardData {
  title: string;
  value: string | number;
  change?: number; // Percentage change (e.g., 12.5 for +12.5%)
  icon?: string; // Icon name or emoji
  unit?: string; // Unit label (e.g., "posts", "hours", "followers")
}

function StatCard({ id, data, size }: WidgetProps) {
  const statData = data as StatCardData;
  const { title, value, change, icon, unit } = statData;

  // Determine trend direction
  const getTrendIcon = () => {
    if (!change) return null;
    if (change > 0) return <TrendingUp className="w-4 h-4 text-green-500" />;
    if (change < 0) return <TrendingDown className="w-4 h-4 text-red-500" />;
    return <Minus className="w-4 h-4 text-gray-400" />;
  };

  const getTrendColor = () => {
    if (!change) return 'text-gray-600';
    return change > 0 ? 'text-green-600' : 'text-red-600';
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
      className="h-full"
    >
      <div className="card-background rounded-xl p-6 h-full flex flex-col justify-between shadow-lg border border-border/50">
        {/* Icon */}
        {icon && (
          <div className="mb-4">
            <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center text-2xl">
              {icon}
            </div>
          </div>
        )}

        {/* Content */}
        <div className="flex-1">
          <h3 className="text-sm font-medium text-muted mb-2">{title}</h3>
          <div className="flex items-baseline gap-2">
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2, duration: 0.5 }}
              className="text-4xl font-bold text-foreground"
            >
              {value}
            </motion.p>
            {unit && <span className="text-sm text-muted">{unit}</span>}
          </div>
        </div>

        {/* Change indicator */}
        {change !== undefined && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4, duration: 0.5 }}
            className="flex items-center gap-1 mt-4"
          >
            {getTrendIcon()}
            <span className={`text-sm font-medium ${getTrendColor()}`}>
              {change > 0 ? '+' : ''}
              {change}%
            </span>
            <span className="text-xs text-muted ml-1">vs last period</span>
          </motion.div>
        )}
      </div>
    </motion.div>
  );
}

// Register this widget type
registerWidget('stat-card', StatCard);

export default StatCard;
