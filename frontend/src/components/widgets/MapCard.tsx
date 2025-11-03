/**
 * MapCard Widget
 *
 * Displays an interactive Mapbox map with location markers.
 */

import { motion } from 'framer-motion';
import { Navigation } from 'lucide-react';
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

function MapCard({ id: _id, data, size: _size }: WidgetProps) {
  const mapData = data as MapCardData;
  const { title, center, zoom, markers } = mapData;
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<mapboxgl.Map | null>(null);
  const [mapLoaded, setMapLoaded] = useState(false);
  const [mapError, setMapError] = useState<string | null>(null);

  useEffect(() => {
    console.log('🗺️ MapCard data received:', {
      rawData: data,
      title,
      center,
      zoom,
      markers,
      hasCenter: !!center,
      hasZoom: zoom !== undefined,
      markerCount: markers?.length || 0
    });

    if (!mapContainer.current || map.current) return;

    // Check if token exists
    console.log('MAPBOX_TOKEN loaded:', MAPBOX_TOKEN ? `${MAPBOX_TOKEN.substring(0, 20)}...` : 'undefined');
    if (!MAPBOX_TOKEN) {
      console.error('Mapbox token is missing!');
      setMapError('Mapbox token not configured');
      return;
    }

    // Initialize map
    mapboxgl.accessToken = MAPBOX_TOKEN;

    const initMap = (width: number, height: number) => {
      if (!mapContainer.current || map.current) return;

      console.log('Initializing Mapbox map with dimensions:', { width, height });

      try {
        map.current = new mapboxgl.Map({
          container: mapContainer.current,
          style: 'mapbox://styles/mapbox/satellite-streets-v12',
          center: [center.lng, center.lat],
          zoom: zoom || 12,
        });

        // Set a timeout to detect stuck loading
        const loadTimeout = setTimeout(() => {
          if (!mapLoaded) {
            console.error('Map loading timeout - map.load event never fired');
            setMapError('Map loading timed out. Check network and Mapbox token.');
          }
        }, 10000); // 10 second timeout

        // Add markers when map loads
        map.current.on('load', () => {
          console.log('Map loaded successfully');
          clearTimeout(loadTimeout);
          setMapLoaded(true);

          // Force resize when map loads to ensure proper rendering
          if (map.current) {
            map.current.resize();
            console.log('Resized map on load');
          }

          // Calculate bounds to fit all markers
          const bounds = new mapboxgl.LngLatBounds();
          markers.forEach((marker) => {
            bounds.extend([marker.lng, marker.lat]);
          });

          // Fit map to show all markers with padding
          if (map.current && markers.length > 0) {
            map.current.fitBounds(bounds, {
              padding: 60,
              maxZoom: 13
            });
          }

          markers.forEach((marker) => {
            if (!map.current) return;

            // Create marker element (smaller size)
            const el = document.createElement('div');
            el.className = 'custom-marker';
            el.style.width = '24px';
            el.style.height = '24px';
            el.style.backgroundColor = 'var(--color-primary)';
            el.style.borderRadius = '50%';
            el.style.border = '2px solid white';
            el.style.boxShadow = '0 2px 6px rgba(0,0,0,0.3)';
            el.style.cursor = 'pointer';
            el.style.display = 'flex';
            el.style.alignItems = 'center';
            el.style.justifyContent = 'center';

            // Add pin icon (smaller)
            const icon = document.createElement('div');
            icon.innerHTML = `<svg width="12" height="12" viewBox="0 0 24 24" fill="white" stroke="white" stroke-width="2"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"></path><circle cx="12" cy="10" r="3"></circle></svg>`;
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

            // Show popup on hover
            el.addEventListener('mouseenter', () => {
              popup.addTo(map.current!);
            });

            el.addEventListener('mouseleave', () => {
              popup.remove();
            });
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
    };

    // Use ResizeObserver to wait for container to have proper dimensions
    const resizeObserver = new ResizeObserver((entries) => {
      for (const entry of entries) {
        const { width, height } = entry.contentRect;
        console.log('Container resized:', { width, height });

        // Once container has reasonable dimensions, initialize map
        if (width > 100 && height > 100 && !map.current) {
          console.log('Container ready, initializing map...');
          initMap(width, height);

          // Force resize after grid layout settles
          setTimeout(() => {
            if (map.current) {
              console.log('Forcing map resize after layout settle');
              map.current.resize();
            }
          }, 500);
        } else if (map.current && width > 100 && height > 100) {
          // Resize existing map when container changes
          console.log('Resizing existing map to:', { width, height });
          map.current.resize();
        }
      }
    });

    resizeObserver.observe(mapContainer.current);

    // Cleanup
    return () => {
      resizeObserver.disconnect();
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
