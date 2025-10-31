/**
 * ContentCard Widget
 *
 * Displays Perplexity article recommendations with deep dive content.
 * Shows article title, overview, source, and publish date.
 */

import { motion } from 'framer-motion';
import { BookOpen, ExternalLink, Calendar, Newspaper } from 'lucide-react';
import { registerWidget } from './WidgetRegistry';
import type { WidgetProps } from './WidgetTypes';

interface ContentCardData {
  title: string;
  overview: string;
  url: string;
  sourceName: string;
  publishedDate: string;
}

function ContentCard({ id, data, size }: WidgetProps) {
  const contentData = data as ContentCardData;
  const { title, overview, url, sourceName, publishedDate } = contentData;

  // Format date to readable format
  const formatDate = (dateString: string) => {
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
      });
    } catch {
      return dateString;
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
      className="h-full"
    >
      <div className="card-background rounded-lg p-3 h-full flex flex-col shadow-lg border border-border/50">
        {/* Header Badge */}
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="flex items-center gap-2 mb-3"
        >
          <div className="flex items-center gap-1.5 text-xs text-muted px-2 py-1 rounded-full bg-accent/10">
            <BookOpen className="w-3 h-3 text-accent" />
            <span>Deep Dive</span>
          </div>
        </motion.div>

        {/* Content */}
        <div className="flex-1 flex flex-col gap-3">
          {/* Title */}
          <motion.h3
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="text-xs font-bold text-foreground leading-tight break-words whitespace-normal"
          >
            {title}
          </motion.h3>

          {/* Overview */}
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4 }}
            className="text-[10px] text-muted-foreground leading-relaxed flex-1 break-words whitespace-normal overflow-wrap-anywhere"
          >
            {overview}
          </motion.p>

          {/* Metadata */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
            className="space-y-2"
          >
            {/* Source */}
            {sourceName && (
              <div className="flex items-center gap-2 text-xs text-muted">
                <Newspaper className="w-3 h-3" />
                <span className="font-medium">{sourceName}</span>
              </div>
            )}

            {/* Published Date */}
            {publishedDate && (
              <div className="flex items-center gap-2 text-xs text-muted">
                <Calendar className="w-3 h-3" />
                <span>{formatDate(publishedDate)}</span>
              </div>
            )}
          </motion.div>

          {/* Read More Button */}
          <motion.a
            href={url}
            target="_blank"
            rel="noopener noreferrer"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="group flex items-center justify-between gap-3 px-4 py-3 rounded-lg font-semibold text-sm transition-all shadow-md border"
            style={{
              backgroundColor: 'var(--color-primary)',
              color: 'white',
              borderColor: 'var(--color-primary)',
            }}
          >
            <span>Read Full Article</span>
            <ExternalLink className="w-4 h-4 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
          </motion.a>
        </div>
      </div>
    </motion.div>
  );
}

// Register this widget type as "content-card" (matches backend)
registerWidget('content-card', ContentCard);

export default ContentCard;
