/**
 * ArticleCard Widget
 *
 * Displays article content with title, excerpt, body (markdown), and sources.
 * Uses shadcn-style card design with Framer Motion animations.
 */

import { motion } from 'framer-motion';
import { Clock, ExternalLink } from 'lucide-react';
import { registerWidget } from './WidgetRegistry';
import type { WidgetProps } from './WidgetTypes';

interface Source {
  title: string;
  url: string;
}

interface ArticleCardData {
  title: string;
  excerpt: string;
  content: string; // Markdown content
  readingTime: string; // e.g., "3 min"
  sources?: Source[];
}

function ArticleCard({ id: _id, data, size: _size }: WidgetProps) {
  const articleData = data as ArticleCardData;
  const { title, excerpt, content, readingTime, sources } = articleData;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="h-full"
    >
      <div className="card-background rounded-lg p-3 h-full flex flex-col shadow-lg border border-border/50 hover:border-primary/50 transition-colors overflow-hidden">
        {/* Header */}
        <div className="mb-3">
          <motion.h2
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.1, duration: 0.5 }}
            className="text-sm font-heading font-bold text-foreground mb-1 leading-tight"
          >
            {title}
          </motion.h2>

          <div className="flex items-center gap-1 text-xs text-muted">
            <Clock className="w-3 h-3" />
            <span>{readingTime}</span>
          </div>
        </div>

        {/* Excerpt */}
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2, duration: 0.5 }}
          className="text-[10px] text-foreground/90 mb-2 leading-relaxed break-words whitespace-normal overflow-wrap-anywhere line-clamp-2"
        >
          {excerpt}
        </motion.p>

        {/* Content preview or full content */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3, duration: 0.5 }}
          className="text-xs leading-relaxed mb-2 break-words whitespace-normal flex-1 overflow-y-auto pr-2"
          style={{
            color: 'var(--color-foreground)',
            opacity: 0.9,
          }}
        >
          <div className="whitespace-pre-wrap" style={{ color: 'var(--color-foreground)' }}>{content}</div>
        </motion.div>

        {/* Sources */}
        {sources && sources.length > 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4, duration: 0.5 }}
            className="mt-auto pt-4 border-t border-border/50"
          >
            <p className="text-xs font-medium text-muted mb-2">Sources:</p>
            <div className="flex flex-wrap gap-2">
              {sources.slice(0, 3).map((source, idx) => (
                <a
                  key={idx}
                  href={source.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1 text-xs text-primary hover:text-primary/80 transition-colors"
                >
                  <ExternalLink className="w-3 h-3" />
                  <span className="truncate max-w-[150px]">{source.title}</span>
                </a>
              ))}
              {sources.length > 3 && (
                <span className="text-xs text-muted">+{sources.length - 3} more</span>
              )}
            </div>
          </motion.div>
        )}
      </div>
    </motion.div>
  );
}

// Register this widget type
registerWidget('article-card', ArticleCard);

export default ArticleCard;
