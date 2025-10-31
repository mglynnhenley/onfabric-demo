/**
 * InfoCard Widget
 *
 * Displays weather information with location, temperature, and conditions.
 * Uses weather-based accent colors and Framer Motion animations.
 */

import { motion } from 'framer-motion';
import { MapPin, Cloud, Sun, CloudRain, CloudSnow, Wind } from 'lucide-react';
import { registerWidget } from './WidgetRegistry';
import type { WidgetProps } from './WidgetTypes';

interface InfoCardData {
  title: string;        // "San Francisco Weather"
  value: string;        // "72°F"
  subtitle: string;     // "Sunny" or "Cloudy"
  location: string;     // "San Francisco, CA"
}

function InfoCard({ id, data, size }: WidgetProps) {
  const infoData = data as InfoCardData;
  const { title, value, subtitle, location } = infoData;

  // Get weather emoji and accent color based on condition
  const getWeatherEmoji = (condition: string) => {
    const lower = condition.toLowerCase();
    if (lower.includes('sunny') || lower.includes('clear')) return '☀️';
    if (lower.includes('rain')) return '🌧️';
    if (lower.includes('snow')) return '❄️';
    if (lower.includes('cloud')) return '☁️';
    if (lower.includes('wind')) return '💨';
    if (lower.includes('storm')) return '⛈️';
    return '🌤️';
  };

  const getWeatherColor = (condition: string) => {
    const lower = condition.toLowerCase();
    if (lower.includes('sunny') || lower.includes('clear')) return 'from-orange-400 to-yellow-300';
    if (lower.includes('rain')) return 'from-blue-400 to-cyan-300';
    if (lower.includes('snow')) return 'from-blue-200 to-slate-100';
    if (lower.includes('cloud')) return 'from-gray-400 to-slate-300';
    if (lower.includes('wind')) return 'from-teal-400 to-emerald-300';
    if (lower.includes('storm')) return 'from-purple-500 to-indigo-400';
    return 'from-sky-400 to-blue-300';
  };

  const getWeatherAccent = (condition: string) => {
    const lower = condition.toLowerCase();
    if (lower.includes('sunny') || lower.includes('clear')) return 'bg-orange-500/10 text-orange-600';
    if (lower.includes('rain')) return 'bg-blue-500/10 text-blue-600';
    if (lower.includes('snow')) return 'bg-blue-300/10 text-blue-400';
    if (lower.includes('cloud')) return 'bg-gray-500/10 text-gray-600';
    if (lower.includes('wind')) return 'bg-teal-500/10 text-teal-600';
    if (lower.includes('storm')) return 'bg-purple-500/10 text-purple-600';
    return 'bg-sky-500/10 text-sky-600';
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
      className="h-full"
    >
      <div className="card-background rounded-lg p-6 h-full flex flex-col justify-between shadow-lg border border-border/50 overflow-hidden relative">
        {/* Gradient background overlay */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.1 }}
          transition={{ delay: 0.2, duration: 0.8 }}
          className={`absolute inset-0 bg-gradient-to-br ${getWeatherColor(subtitle)}`}
        />

        <div className="relative z-10">
          {/* Location header */}
          <div className="flex items-center gap-2 mb-6">
            <MapPin className="w-4 h-4 text-primary" />
            <h3 className="text-sm font-medium text-muted">{location}</h3>
          </div>

          {/* Weather emoji icon */}
          <motion.div
            initial={{ scale: 0, rotate: -180 }}
            animate={{ scale: 1, rotate: 0 }}
            transition={{ delay: 0.3, type: "spring", stiffness: 200 }}
            className="mb-6"
          >
            <div className={`w-16 h-16 rounded-full ${getWeatherAccent(subtitle)} flex items-center justify-center text-4xl`}>
              {getWeatherEmoji(subtitle)}
            </div>
          </motion.div>

          {/* Temperature */}
          <div className="mb-3">
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4, duration: 0.5 }}
              className="text-5xl font-bold text-foreground"
            >
              {value}
            </motion.p>
          </div>

          {/* Condition */}
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5, duration: 0.5 }}
            className="text-lg font-medium text-muted-foreground"
          >
            {subtitle}
          </motion.p>
        </div>
      </div>
    </motion.div>
  );
}

// Register this widget type
registerWidget('info-card', InfoCard);

export default InfoCard;
