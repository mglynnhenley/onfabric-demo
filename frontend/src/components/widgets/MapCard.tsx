/**
 * MapCard Widget
 *
 * Displays an interactive map with location markers.
 * Uses a simple visual representation with marker pins.
 */

import { motion } from 'framer-motion';
import { MapPin, Navigation } from 'lucide-react';
import { registerWidget } from './WidgetRegistry';
import type { WidgetProps } from './WidgetTypes';

interface Marker {
  lat: number;
  lng: number;
  title: string;
  description: string;
}

interface MapCardData {
  title: string;
  center: {
    lat: number;
    lng: number;
  };
  zoom: number;
  markers: Marker[];
}

function MapCard({ id, data, size }: WidgetProps) {
  const mapData = data as MapCardData;
  const { title, center, zoom, markers } = mapData;

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
      className="h-full"
    >
      <div className="card-background rounded-xl p-6 h-full flex flex-col shadow-lg border border-border/50">
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-bold text-foreground flex items-center gap-2">
            <Navigation className="w-5 h-5 text-primary" />
            {title}
          </h3>
          <span className="text-xs text-muted px-2 py-1 rounded-full bg-primary/10">
            {markers.length} {markers.length === 1 ? 'location' : 'locations'}
          </span>
        </div>

        {/* Map Visualization */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="flex-1 rounded-lg overflow-hidden relative bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-950/20 dark:to-indigo-950/20 border border-border/30"
        >
          {/* Grid pattern to simulate map */}
          <div className="absolute inset-0 opacity-10">
            <svg className="w-full h-full" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <pattern id={`grid-${id}`} width="40" height="40" patternUnits="userSpaceOnUse">
                  <path
                    d="M 40 0 L 0 0 0 40"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="0.5"
                    className="text-primary"
                  />
                </pattern>
              </defs>
              <rect width="100%" height="100%" fill={`url(#grid-${id})`} />
            </svg>
          </div>

          {/* Marker Pins - positioned in a visually pleasing layout */}
          <div className="absolute inset-0 p-6 flex items-center justify-center">
            <div className="relative w-full h-full">
              {markers.map((marker, index) => {
                // Distribute markers in a visually balanced way
                const positions = [
                  { top: '20%', left: '30%' },
                  { top: '50%', left: '60%' },
                  { top: '70%', left: '25%' },
                  { top: '30%', left: '70%' },
                  { top: '60%', left: '45%' },
                ];
                const position = positions[index % positions.length];

                return (
                  <motion.div
                    key={index}
                    initial={{ scale: 0, y: -50 }}
                    animate={{ scale: 1, y: 0 }}
                    transition={{
                      delay: 0.3 + index * 0.1,
                      type: 'spring',
                      stiffness: 200,
                    }}
                    className="absolute group cursor-pointer"
                    style={position}
                  >
                    {/* Pin */}
                    <div className="relative flex flex-col items-center">
                      <motion.div
                        whileHover={{ scale: 1.2 }}
                        className="w-8 h-8 rounded-full bg-primary shadow-lg flex items-center justify-center text-white border-2 border-white"
                      >
                        <MapPin className="w-5 h-5" />
                      </motion.div>

                      {/* Tooltip */}
                      <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        whileHover={{ opacity: 1, y: 0 }}
                        className="absolute top-10 z-10 hidden group-hover:block"
                      >
                        <div className="bg-foreground text-background px-3 py-2 rounded-lg shadow-xl text-xs whitespace-nowrap max-w-[200px]">
                          <p className="font-semibold mb-1">{marker.title}</p>
                          {marker.description && (
                            <p className="text-muted-foreground opacity-80">
                              {marker.description}
                            </p>
                          )}
                        </div>
                      </motion.div>
                    </div>
                  </motion.div>
                );
              })}
            </div>
          </div>
        </motion.div>

        {/* Marker List */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="mt-4 space-y-2 max-h-32 overflow-y-auto"
        >
          {markers.slice(0, 3).map((marker, index) => (
            <div
              key={index}
              className="flex items-start gap-2 text-xs p-2 rounded-lg bg-muted/20 hover:bg-muted/30 transition-colors"
            >
              <MapPin className="w-3 h-3 text-primary mt-0.5 flex-shrink-0" />
              <div className="flex-1 min-w-0">
                <p className="font-medium text-foreground truncate">{marker.title}</p>
                {marker.description && (
                  <p className="text-muted-foreground truncate">{marker.description}</p>
                )}
              </div>
            </div>
          ))}
          {markers.length > 3 && (
            <p className="text-xs text-muted text-center">
              +{markers.length - 3} more locations
            </p>
          )}
        </motion.div>
      </div>
    </motion.div>
  );
}

// Register this widget type
registerWidget('map-card', MapCard);

export default MapCard;
