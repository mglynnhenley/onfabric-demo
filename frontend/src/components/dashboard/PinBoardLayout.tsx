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
import GridLayout from 'react-grid-layout';
import type { Layout } from 'react-grid-layout';
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
function sizeToGridUnits(size: string, type: string, widget?: Widget): { w: number; h: number } {
  // Smaller base sizes for "zoomed out" generative interface look
  const baseSizes = {
    compact: { w: 3, h: 2 },  // Very compact
    small: { w: 3, h: 3 },
    medium: { w: 4, h: 4 },
    large: { w: 5, h: 6 },     // Taller for large content
  };

  // Type-specific width adjustments (content-heavy cards need more horizontal space)
  const widthMultipliers: Record<string, number> = {
    'content-card': 0.8,  // Very compact button
    'article-card': 2.0,  // Wider for article content
  };

  // For article cards, calculate height based on actual content length
  if (type === 'article-card' && widget?.data?.content) {
    const contentLength = (widget.data.content as string).length;
    const base = baseSizes[size as keyof typeof baseSizes] || baseSizes.medium;
    const widthMultiplier = widthMultipliers[type] || 1;

    // Estimate height based on content length
    // rowHeight is 80px, text-xs ~12px with 1.5 line-height = 18px/line
    // At 80px per grid row, we fit ~4 lines
    // Each line ~100 chars at article card width
    // So ~400 chars per grid row, using 360 to add ~60px more height
    const estimatedRows = Math.ceil(contentLength / 360); // Reduced to add ~60px
    const minRows = 3; // Minimum height for readability
    const maxRows = 9; // Maximum to prevent excessive height
    const calculatedHeight = Math.min(maxRows, Math.max(minRows, estimatedRows + 1)); // +1 for header/footer

    return {
      w: Math.round(base.w * widthMultiplier),
      h: calculatedHeight,
    };
  }

  // For task cards, calculate height based on number of tasks
  if (type === 'task-card' && widget?.data?.tasks) {
    const taskCount = (widget.data.tasks as any[]).length;
    const base = baseSizes[size as keyof typeof baseSizes] || baseSizes.medium;
    const widthMultiplier = widthMultipliers[type] || 1;

    // Each task takes ~60px (p-3 button with text + spacing)
    // Header ~100px, Footer ~60px, Progress bar ~30px = ~190px overhead
    // rowHeight is 80px, so:
    // 3 rows = 240px (fits ~1 task + header/footer)
    // 4 rows = 320px (fits ~2-3 tasks)
    // 5 rows = 400px (fits ~3-4 tasks)
    // 6 rows = 480px (fits ~5-6 tasks)
    const estimatedRows = Math.ceil((taskCount * 60 + 190) / 80);
    const minRows = 4; // Minimum for header + at least 1 task
    const maxRows = 8; // Maximum to prevent excessive height
    const calculatedHeight = Math.min(maxRows, Math.max(minRows, estimatedRows));

    return {
      w: Math.round(base.w * widthMultiplier),
      h: calculatedHeight,
    };
  }

  // Type-specific adjustments for content that needs more height
  const heightMultipliers: Record<string, number> = {
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

// Generate scattered layout positions with random offsets
function generateScatteredLayout(widgets: Widget[]): Layout[] {
  const cols = 16;
  const layout: Layout[] = [];
  let currentY = 0;
  let currentX = 0;
  let currentRowMaxHeight = 0; // Track tallest widget in current row

  // Use widgets as-is (already shuffled by backend)
  widgets.forEach((widget, idx) => {
    const { w, h } = sizeToGridUnits(widget.size, widget.type, widget);

    // Check if widget fits in current row
    if (currentX + w > cols) {
      // Move to next row, using the max height from previous row
      currentX = 0;
      currentY += currentRowMaxHeight;
      currentRowMaxHeight = 0; // Reset for new row
    }

    // Track the tallest widget in this row
    currentRowMaxHeight = Math.max(currentRowMaxHeight, h);

    // Add subtle random offset for organic scatter (tighter positioning)
    const maxXOffset = Math.min(1, cols - (currentX + w)); // Max 1 column offset
    const randomXOffset = Math.random() < 0.3 ? maxXOffset : 0; // 30% chance of offset
    const randomYOffset = Math.random() < 0.2 ? 1 : 0; // 20% chance of 1 row offset

    const layoutItem = {
      i: widget.id,
      x: currentX + randomXOffset,
      y: currentY + randomYOffset,
      w,
      h,
      minW: w,
      minH: h,
    };

    console.log(`Widget ${idx} (${widget.type}): x=${currentX + randomXOffset}, y=${currentY + randomYOffset}, w=${w}, h=${h} (offset: +${randomXOffset}x, +${randomYOffset}y)`);
    layout.push(layoutItem);

    // Update position for next widget
    currentX += w;
  });

  console.log('Generated layout with organic scatter:', layout);
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
        margin={[20, 20]}
      >
        {uniqueWidgets.map((widget) => {
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
