/**
 * Widget grid - Enhanced with better animations.
 */

import { motion } from 'framer-motion';

interface WidgetGridProps {
  widgets: string[];
}

const widgetInfo: Record<string, { label: string; icon: string; color: string }> = {
  'info-card': { label: 'Weather', icon: '🌤️', color: 'from-blue-100 to-cyan-50' },
  'map-card': { label: 'Map', icon: '🗺️', color: 'from-green-100 to-emerald-50' },
  'video-feed': { label: 'Videos', icon: '📺', color: 'from-purple-100 to-pink-50' },
  'event-calendar': { label: 'Events', icon: '📅', color: 'from-red-100 to-orange-50' },
  'task-list': { label: 'Tasks', icon: '✓', color: 'from-yellow-100 to-amber-50' },
  'content-card': { label: 'Article', icon: '📄', color: 'from-gray-100 to-slate-50' },
};

export function WidgetGrid({ widgets }: WidgetGridProps) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
      whileHover={{ scale: 1.02 }}
      className="bg-white border-2 border-warm-gray rounded-2xl p-6 shadow-editorial hover:shadow-editorial-lg transition-all"
    >
      <h3 className="font-display text-xl font-bold text-charcoal mb-5">
        Live Widgets
      </h3>

      <div className="grid grid-cols-3 gap-3">
        {widgets.slice(0, 6).map((widget, index) => {
          const info = widgetInfo[widget] || { label: widget, icon: '📊', color: 'from-gray-100 to-slate-50' };
          return (
            <motion.div
              key={widget}
              initial={{ opacity: 0, scale: 0.8, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              transition={{
                duration: 0.4,
                delay: index * 0.08,
                type: "spring",
                stiffness: 200
              }}
              whileHover={{ scale: 1.1, rotate: 5 }}
              className={`bg-gradient-to-br ${info.color} p-4 rounded-xl text-center border-2 border-warm-gray hover:border-terracotta transition-all cursor-default`}
            >
              <motion.div
                className="text-4xl mb-2"
                animate={{ scale: [1, 1.1, 1] }}
                transition={{ duration: 2, repeat: Infinity, delay: index * 0.2 }}
              >
                {info.icon}
              </motion.div>
              <div className="text-xs font-semibold text-charcoal/80">
                {info.label}
              </div>
            </motion.div>
          );
        })}
      </div>
    </motion.div>
  );
}
