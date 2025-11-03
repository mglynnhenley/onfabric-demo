/**
 * ContentCard Widget
 *
 * Displays Perplexity article recommendations with deep dive content.
 * Shows article title, overview, source, and publish date.
 */

import { motion } from 'framer-motion';
import { BookOpen, ExternalLink } from 'lucide-react';
import { registerWidget } from './WidgetRegistry';
import type { WidgetProps } from './WidgetTypes';

interface ContentCardData {
  title: string;
  overview: string;
  url: string;
  sourceName: string;
  publishedDate: string;
}

function ContentCard({ id: _id, data, size: _size }: WidgetProps) {
  const contentData = data as ContentCardData;
  const { title, overview: _overview, url, sourceName: _sourceName, publishedDate: _publishedDate } = contentData;

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
      className="h-full"
    >
      <motion.a
        href={url}
        target="_blank"
        rel="noopener noreferrer"
        whileHover={{ scale: 1.02, y: -1 }}
        whileTap={{ scale: 0.98 }}
        className="h-full rounded-lg px-2 py-1.5 flex flex-col justify-between shadow-sm border transition-all cursor-pointer group card-background hover:border-primary/50 font-body"
        style={{
          borderColor: 'var(--color-border)',
        }}
      >
        {/* Badge + Title */}
        <div className="flex flex-col gap-0.5">
          <div className="flex items-center gap-1">
            <BookOpen className="w-2.5 h-2.5 text-primary" />
            <span className="text-[7px] font-medium uppercase tracking-wide text-primary">
              Deep Dive
            </span>
          </div>

          <h3 className="text-[10px] font-bold leading-tight break-words whitespace-normal overflow-hidden line-clamp-2 text-foreground font-heading">
            {title}
          </h3>
        </div>

        {/* Arrow indicator */}
        <div className="flex items-center justify-end mt-1">
          <ExternalLink className="w-3 h-3 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform text-primary" />
        </div>
      </motion.a>
    </motion.div>
  );
}

// Register this widget type as "content-card" (matches backend)
registerWidget('content-card', ContentCard);

export default ContentCard;
