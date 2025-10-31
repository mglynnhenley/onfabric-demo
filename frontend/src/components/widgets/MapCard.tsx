/**
 * MapCard Widget
 *
 * Displays an interactive Mapbox map with location markers.
 */

import { motion } from 'framer-motion';
import { MapPin, Navigation } from 'lucide-react';
import { registerWidget } from './WidgetRegistry';
import type { WidgetProps } from './WidgetTypes';
import { useEffect, useRef, useState } from 'react';
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';

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

const MAPBOX_TOKEN = import.meta.env.VITE_MAPBOX_TOKEN;

function MapCard({ id, data, size }: WidgetProps) {
  const mapData = data as MapCardData;
  const { title, center, zoom, markers } = mapData;
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<mapboxgl.Map | null>(null);
  const [mapLoaded, setMapLoaded] = useState(false);
  const [mapError, setMapError] = useState<string | null>(null);

  useEffect(() => {
    if (!mapContainer.current || map.current) return;

    // Check if token exists
    console.log('MAPBOX_TOKEN loaded:', MAPBOX_TOKEN ? `${MAPBOX_TOKEN.substring(0, 20)}...` : 'undefined');
    if (!MAPBOX_TOKEN) {
      console.error('Mapbox token is missing!');
      setMapError('Mapbox token not configured');
      return;
    }

    console.log('Initializing Mapbox map with center:', center, 'zoom:', zoom);

    // Initialize map
    mapboxgl.accessToken = MAPBOX_TOKEN;

    try {
      map.current = new mapboxgl.Map({
        container: mapContainer.current,
        style: 'mapbox://styles/mapbox/light-v11',
        center: [center.lng, center.lat],
        zoom: zoom || 12,
      });

      // Add markers
      map.current.on('load', () => {
        console.log('Map loaded successfully');
        setMapLoaded(true);

        markers.forEach((marker) => {
          if (!map.current) return;

          // Create marker element
          const el = document.createElement('div');
          el.className = 'custom-marker';
          el.style.width = '32px';
          el.style.height = '32px';
          el.style.backgroundColor = 'var(--color-primary)';
          el.style.borderRadius = '50%';
          el.style.border = '3px solid white';
          el.style.boxShadow = '0 2px 8px rgba(0,0,0,0.3)';
          el.style.cursor = 'pointer';
          el.style.display = 'flex';
          el.style.alignItems = 'center';
          el.style.justifyContent = 'center';

          // Add pin icon
          const icon = document.createElement('div');
          icon.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="white" stroke="white" stroke-width="2"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"></path><circle cx="12" cy="10" r="3"></circle></svg>`;
          el.appendChild(icon);

          // Create popup
          const popup = new mapboxgl.Popup({ offset: 25 }).setHTML(
            `<div style="padding: 8px;">
              <p style="font-weight: 600; margin-bottom: 4px; font-size: 14px;">${marker.title}</p>
              ${marker.description ? `<p style="color: #666; font-size: 12px;">${marker.description}</p>` : ''}
            </div>`
          );

          // Add marker to map
          new mapboxgl.Marker(el)
            .setLngLat([marker.lng, marker.lat])
            .setPopup(popup)
            .addTo(map.current);
        });
      });

      map.current.on('error', (e) => {
        console.error('Mapbox error:', e);
        setMapError(`Map error: ${e.error?.message || 'Unknown error'}`);
      });
    } catch (error) {
      console.error('Failed to initialize map:', error);
      setMapError(`Failed to initialize map: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }

    // Cleanup
    return () => {
      map.current?.remove();
    };
  }, [center, zoom, markers]);

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
      className="h-full"
    >
      <div className="card-background rounded-lg p-4 h-full flex flex-col shadow-lg border border-border/50">
        {/* Header */}
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-sm font-heading font-bold text-foreground flex items-center gap-1.5">
            <Navigation className="w-4 h-4 text-primary" />
            {title}
          </h3>
        </div>

        {/* Mapbox Map */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="flex-1 rounded-md overflow-hidden relative"
          style={{ minHeight: '300px' }}
        >
          <div ref={mapContainer} className="w-full h-full" />
          {mapError && (
            <div className="absolute inset-0 flex items-center justify-center bg-destructive/10">
              <div className="text-sm text-destructive px-4 text-center">
                <p className="font-semibold mb-1">Map Error</p>
                <p className="text-xs">{mapError}</p>
              </div>
            </div>
          )}
          {!mapLoaded && !mapError && (
            <div className="absolute inset-0 flex items-center justify-center bg-muted/20">
              <div className="text-sm text-muted">Loading map...</div>
            </div>
          )}
        </motion.div>
      </div>
    </motion.div>
  );
}

// Register this widget type
registerWidget('map-card', MapCard);

export default MapCard;
