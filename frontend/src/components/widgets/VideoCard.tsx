/**
 * VideoCard Widget (VideoFeed)
 *
 * Displays YouTube video recommendations with thumbnails.
 * Shows a feed of relevant videos based on user interests.
 */

import { motion } from 'framer-motion';
import { Play, Youtube, ExternalLink } from 'lucide-react';
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

function VideoCard({ id, data, size }: WidgetProps) {
  const videoData = data as VideoCardData;
  const { title, query, videos } = videoData;

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
            <Youtube className="w-5 h-5 text-red-500" />
            {title}
          </h3>
          <span className="text-xs text-muted px-2 py-1 rounded-full bg-red-500/10">
            {videos.length} videos
          </span>
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

        {/* Video Feed */}
        <div className="flex-1 space-y-3 overflow-y-auto">
          {videos.map((video, index) => (
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
              <div className="flex gap-3 p-2 rounded-lg hover:bg-muted/20 transition-colors">
                {/* Thumbnail */}
                <div className="relative w-32 h-20 flex-shrink-0 rounded-lg overflow-hidden bg-gradient-to-br from-red-500/20 to-pink-500/20">
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
                <div className="flex-1 min-w-0 flex flex-col justify-center">
                  <h4 className="text-sm font-medium text-foreground line-clamp-2 mb-1 group-hover:text-primary transition-colors">
                    {video.title}
                  </h4>
                  <div className="flex items-center gap-1 text-xs text-muted">
                    <Youtube className="w-3 h-3" />
                    <span>Watch on YouTube</span>
                    <ExternalLink className="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity" />
                  </div>
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

        {/* Footer */}
        {videos.length > 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
            className="mt-4 pt-4 border-t border-border/30"
          >
            <a
              href={`https://www.youtube.com/results?search_query=${encodeURIComponent(query)}`}
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs text-primary hover:underline flex items-center gap-1"
            >
              <span>View more on YouTube</span>
              <ExternalLink className="w-3 h-3" />
            </a>
          </motion.div>
        )}
      </div>
    </motion.div>
  );
}

// Register this widget type as "video-card" (matches backend)
registerWidget('video-card', VideoCard);

export default VideoCard;
