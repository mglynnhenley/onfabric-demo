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
import { useState } from 'react';

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

function ArticleCard({ id, data, size }: WidgetProps) {
  const articleData = data as ArticleCardData;
  const { title, excerpt, content, readingTime, sources } = articleData;
  const [isExpanded, setIsExpanded] = useState(false);

  // Convert size to max lines for excerpt
  const maxLines = size === 'small' ? 3 : size === 'medium' ? 4 : 6;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="h-full"
    >
      <div className="card-background rounded-xl p-6 h-full flex flex-col shadow-lg border border-border/50 hover:border-primary/50 transition-colors">
        {/* Header */}
        <div className="mb-4">
          <motion.h2
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.1, duration: 0.5 }}
            className="text-2xl font-heading font-bold text-foreground mb-2 leading-tight"
          >
            {title}
          </motion.h2>

          <div className="flex items-center gap-2 text-sm text-muted">
            <Clock className="w-4 h-4" />
            <span>{readingTime}</span>
          </div>
        </div>

        {/* Excerpt */}
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2, duration: 0.5 }}
          className="text-base text-foreground/90 mb-4 leading-relaxed"
          style={{
            display: '-webkit-box',
            WebkitLineClamp: isExpanded ? 'unset' : maxLines,
            WebkitBoxOrient: 'vertical',
            overflow: 'hidden',
          }}
        >
          {excerpt}
        </motion.p>

        {/* Content preview (first few lines of markdown) */}
        {!isExpanded && size !== 'small' && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3, duration: 0.5 }}
            className="text-sm text-muted leading-relaxed mb-4 line-clamp-3"
          >
            {content.substring(0, 150)}...
          </motion.div>
        )}

        {/* Expand/Collapse button */}
        {size !== 'small' && (
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="text-sm font-medium text-primary hover:text-primary/80 transition-colors mb-4 text-left"
          >
            {isExpanded ? 'Show less' : 'Read more'} →
          </button>
        )}

        {/* Expanded content */}
        {isExpanded && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
            className="prose prose-sm mb-4 text-foreground"
          >
            {/* Simple markdown rendering - in production, use a proper markdown library */}
            <div className="whitespace-pre-wrap">{content}</div>
          </motion.div>
        )}

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
