/**
 * PinBoardLayout Component
 *
 * Creates a scattered pin board layout using react-grid-layout:
 * - Generates organized scatter positions for widgets
 * - Renders widgets from the registry
 * - Enables drag-to-reorder functionality
 * - Adds simultaneous emergence animations
 */

import { useState, useEffect, useMemo, useRef } from 'react';
import GridLayout, { Layout } from 'react-grid-layout';
import { motion } from 'framer-motion';
import { getWidget } from '../widgets/WidgetRegistry';
import 'react-grid-layout/css/styles.css';
import 'react-resizable/css/styles.css';

interface Widget {
  id: string;
  type: string;
  size: 'small' | 'medium' | 'large';
  priority: number;
  data: Record<string, any>;
}

interface PinBoardLayoutProps {
  widgets: Widget[];
}

// Convert widget size to grid units with better proportions
function sizeToGridUnits(size: string, type: string): { w: number; h: number } {
  // Smaller base sizes for "zoomed out" generative interface look
  const baseSizes = {
    small: { w: 3, h: 3 },
    medium: { w: 4, h: 4 },
    large: { w: 5, h: 5 },
  };

  // Type-specific width adjustments (content-heavy cards need more horizontal space)
  const widthMultipliers: Record<string, number> = {
    'content-card': 0.8,  // Very compact button
    'article-card': 2.0,  // Wider for article content
  };

  // Type-specific adjustments for content that needs more height
  const heightMultipliers: Record<string, number> = {
    'article-card': 1.5,  // Taller to fit more article content
    'content-card': 0.6,  // Very compact button height
    'video-card': 1.0,
    'event-calendar': 1.0,
  };

  const base = baseSizes[size as keyof typeof baseSizes] || baseSizes.medium;
  const widthMultiplier = widthMultipliers[type] || 1;
  const heightMultiplier = heightMultipliers[type] || 1;

  return {
    w: Math.round(base.w * widthMultiplier),
    h: Math.round(base.h * heightMultiplier),
  };
}

// Generate scattered layout positions
function generateScatteredLayout(widgets: Widget[]): Layout[] {
  const cols = 16;
  const layout: Layout[] = [];
  let currentY = 0;
  let currentX = 0;
  let currentRowMaxHeight = 0; // Track tallest widget in current row

  // Sort by priority first
  const sortedWidgets = [...widgets].sort((a, b) => a.priority - b.priority);

  sortedWidgets.forEach((widget, idx) => {
    const { w, h } = sizeToGridUnits(widget.size, widget.type);

    // Check if widget fits in current row
    if (currentX + w > cols) {
      // Move to next row, using the max height from previous row
      currentX = 0;
      currentY += currentRowMaxHeight;
      currentRowMaxHeight = 0; // Reset for new row
    }

    // Track the tallest widget in this row
    currentRowMaxHeight = Math.max(currentRowMaxHeight, h);

    const layoutItem = {
      i: widget.id,
      x: currentX,
      y: currentY,
      w,
      h,
      minW: w,
      minH: h,
    };

    console.log(`Widget ${idx} (${widget.type}): x=${currentX}, y=${currentY}, w=${w}, h=${h} [rowMaxH=${currentRowMaxHeight}]`);
    layout.push(layoutItem);

    // Update position for next widget
    currentX += w;
  });

  console.log('Generated layout with row-based positioning:', layout);
  return layout;
}

export function PinBoardLayout({ widgets }: PinBoardLayoutProps) {
  const [layout, setLayout] = useState<Layout[]>([]);
  const [mounted, setMounted] = useState(false);
  const [containerWidth, setContainerWidth] = useState(1200);
  const containerRef = useRef<HTMLDivElement>(null);

  // De-duplicate widgets by ID (in case backend sends duplicates)
  const uniqueWidgets = useMemo(() => {
    const seen = new Set<string>();
    const unique = widgets.filter(widget => {
      if (seen.has(widget.id)) {
        console.warn(`Duplicate widget ID detected and removed: ${widget.id}`);
        return false;
      }
      seen.add(widget.id);
      return true;
    });
    return unique;
  }, [widgets]);

  // Measure container width
  useEffect(() => {
    if (!containerRef.current) return;

    const updateWidth = () => {
      if (containerRef.current) {
        const width = containerRef.current.offsetWidth;
        console.log('Container width measured:', width);
        setContainerWidth(width);
      }
    };

    updateWidth();
    window.addEventListener('resize', updateWidth);
    return () => window.removeEventListener('resize', updateWidth);
  }, []);

  // Generate initial layout
  useEffect(() => {
    const initialLayout = generateScatteredLayout(uniqueWidgets);
    console.log('Initial layout generated with', initialLayout.length, 'widgets');
    setLayout(initialLayout);
    setTimeout(() => setMounted(true), 100);
  }, [uniqueWidgets]);

  // Handle layout changes (drag-and-drop)
  const onLayoutChange = (newLayout: Layout[]) => {
    setLayout(newLayout);
  };

  // Stagger animation delays
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, scale: 0.8, y: 20 },
    visible: {
      opacity: 1,
      scale: 1,
      y: 0,
      transition: {
        type: 'spring',
        stiffness: 100,
        damping: 15,
      },
    },
  };

  if (containerWidth === 0) {
    return <div className="w-full max-w-[1600px] mx-auto px-8 py-12">Loading...</div>;
  }

  return (
    <motion.div
      ref={containerRef}
      variants={containerVariants}
      initial="hidden"
      animate={mounted ? 'visible' : 'hidden'}
      className="w-full max-w-[1600px] mx-auto px-8 py-12"
    >
      <GridLayout
        className="layout"
        layout={layout}
        cols={16}
        rowHeight={80}
        width={containerWidth}
        onLayoutChange={onLayoutChange}
        isDraggable={true}
        isResizable={false}
        compactType={null}
        preventCollision={true}
        margin={[16, 16]}
      >
        {uniqueWidgets.map((widget, idx) => {
          const WidgetComponent = getWidget(widget.type);

          if (!WidgetComponent) {
            console.warn(`Widget type "${widget.type}" not found in registry`);
            return (
              <div key={widget.id} className="bg-red-100 p-4 rounded-lg">
                <p className="text-red-600">
                  Unknown widget type: {widget.type}
                </p>
              </div>
            );
          }

          return (
            <div key={widget.id}>
              <WidgetComponent
                id={widget.id}
                data={widget.data}
                size={widget.size}
              />
            </div>
          );
        })}
      </GridLayout>
    </motion.div>
  );
}

export default PinBoardLayout;
