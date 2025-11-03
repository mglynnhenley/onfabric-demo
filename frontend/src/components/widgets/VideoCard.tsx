/**
 * VideoCard Widget (VideoFeed)
 *
 * Displays YouTube video recommendations with thumbnails.
 * Shows a feed of relevant videos based on user interests.
 */

import { motion } from 'framer-motion';
import { Play, Youtube } from 'lucide-react';
import { registerWidget } from './WidgetRegistry';
import type { WidgetProps } from './WidgetTypes';

interface Video {
  title: string;
  thumbnail: string;
  url: string;
}

interface VideoCardData {
  title: string;
  query: string;
  videos: Video[];
}

function VideoCard({ id: _id, data, size: _size }: WidgetProps) {
  const videoData = data as VideoCardData;
  const { title, query, videos } = videoData;

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
      className="h-full"
    >
      <div className="card-background rounded-lg p-6 h-full flex flex-col shadow-lg border border-border/50">
        {/* Header */}
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-sm font-heading font-bold text-foreground flex items-center gap-1.5">
            <Youtube className="w-4 h-4 text-red-500" />
            {title}
          </h3>
        </div>

        {/* Search Query Badge */}
        {query && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="mb-4"
          >
            <p className="text-xs text-muted">
              Based on:{' '}
              <span className="font-medium text-foreground">{query}</span>
            </p>
          </motion.div>
        )}

        {/* Single Video (show only first one) */}
        <div className="flex-1 overflow-hidden">
          {videos.slice(0, 1).map((video, index) => (
            <motion.a
              key={index}
              href={video.url}
              target="_blank"
              rel="noopener noreferrer"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 * (index + 1) }}
              whileHover={{ scale: 1.02 }}
              className="group block"
            >
              <div className="flex flex-col gap-2 rounded-lg hover:bg-muted/10 transition-colors">
                {/* Thumbnail */}
                <div className="relative w-full aspect-video flex-shrink-0 rounded-lg overflow-hidden bg-gradient-to-br from-red-500/20 to-pink-500/20">
                  {video.thumbnail ? (
                    <img
                      src={video.thumbnail}
                      alt={video.title}
                      className="w-full h-full object-cover"
                      loading="lazy"
                    />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center">
                      <Play className="w-8 h-8 text-red-500 opacity-50" />
                    </div>
                  )}

                  {/* Play button overlay */}
                  <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                    <div className="w-10 h-10 rounded-full bg-red-500 flex items-center justify-center">
                      <Play className="w-5 h-5 text-white fill-white" />
                    </div>
                  </div>
                </div>

                {/* Video Info */}
                <div className="flex-1 min-w-0">
                  <h4 className="text-xs font-body font-medium text-foreground line-clamp-2 group-hover:text-primary transition-colors">
                    {video.title}
                  </h4>
                </div>
              </div>
            </motion.a>
          ))}

          {/* Empty State */}
          {videos.length === 0 && (
            <div className="flex flex-col items-center justify-center py-8 text-center">
              <Youtube className="w-12 h-12 text-muted mb-3 opacity-30" />
              <p className="text-sm text-muted">No videos found</p>
              <p className="text-xs text-muted-foreground mt-1">
                Try adjusting your interests
              </p>
            </div>
          )}
        </div>

      </div>
    </motion.div>
  );
}

// Register this widget type as "video-card" (matches backend)
registerWidget('video-card', VideoCard);

export default VideoCard;
