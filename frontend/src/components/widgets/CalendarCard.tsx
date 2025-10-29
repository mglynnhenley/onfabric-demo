/**
 * CalendarCard Widget (EventCalendar)
 *
 * Displays upcoming events from Ticketmaster.
 * Shows event name, date, location with clean timeline UI.
 */

import { motion } from 'framer-motion';
import { Calendar, MapPin, ExternalLink, Clock } from 'lucide-react';
import { registerWidget } from './WidgetRegistry';
import type { WidgetProps } from './WidgetTypes';

interface Event {
  name: string;
  date: string;
  location: string;
  url: string;
}

interface CalendarCardData {
  title: string;
  query: string;
  events: Event[];
}

function CalendarCard({ id, data, size }: WidgetProps) {
  const calendarData = data as CalendarCardData;
  const { title, query, events } = calendarData;

  // Format date to readable format
  const formatDate = (dateString: string) => {
    try {
      const date = new Date(dateString);
      return {
        month: date.toLocaleDateString('en-US', { month: 'short' }),
        day: date.getDate(),
        time: date.toLocaleTimeString('en-US', {
          hour: 'numeric',
          minute: '2-digit',
          hour12: true,
        }),
      };
    } catch {
      return { month: '', day: '', time: '' };
    }
  };

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
            <Calendar className="w-5 h-5 text-primary" />
            {title}
          </h3>
          <span className="text-xs text-muted px-2 py-1 rounded-full bg-primary/10">
            {events.length} {events.length === 1 ? 'event' : 'events'}
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
              Related to:{' '}
              <span className="font-medium text-foreground">{query}</span>
            </p>
          </motion.div>
        )}

        {/* Events Timeline */}
        <div className="flex-1 overflow-y-auto space-y-3">
          {events.map((event, index) => {
            const { month, day, time } = formatDate(event.date);

            return (
              <motion.a
                key={index}
                href={event.url}
                target="_blank"
                rel="noopener noreferrer"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.1 * (index + 1) }}
                whileHover={{ scale: 1.02 }}
                className="group block"
              >
                <div className="flex gap-4 p-3 rounded-lg hover:bg-muted/20 transition-colors border border-border/30">
                  {/* Date Badge */}
                  <div className="flex-shrink-0 w-14 h-14 rounded-lg bg-gradient-to-br from-primary to-secondary flex flex-col items-center justify-center text-white shadow-md">
                    <span className="text-xs font-medium uppercase">{month}</span>
                    <span className="text-xl font-bold">{day}</span>
                  </div>

                  {/* Event Info */}
                  <div className="flex-1 min-w-0">
                    <h4 className="text-sm font-semibold text-foreground line-clamp-2 mb-1 group-hover:text-primary transition-colors">
                      {event.name}
                    </h4>

                    <div className="space-y-1">
                      {/* Location */}
                      {event.location && (
                        <div className="flex items-start gap-1.5 text-xs text-muted">
                          <MapPin className="w-3 h-3 mt-0.5 flex-shrink-0" />
                          <span className="line-clamp-1">{event.location}</span>
                        </div>
                      )}

                      {/* Time */}
                      {time && (
                        <div className="flex items-center gap-1.5 text-xs text-muted">
                          <Clock className="w-3 h-3 flex-shrink-0" />
                          <span>{time}</span>
                        </div>
                      )}
                    </div>

                    {/* External Link Indicator */}
                    <div className="flex items-center gap-1 text-xs text-primary mt-2 opacity-0 group-hover:opacity-100 transition-opacity">
                      <span>View details</span>
                      <ExternalLink className="w-3 h-3" />
                    </div>
                  </div>
                </div>
              </motion.a>
            );
          })}

          {/* Empty State */}
          {events.length === 0 && (
            <div className="flex flex-col items-center justify-center py-8 text-center">
              <Calendar className="w-12 h-12 text-muted mb-3 opacity-30" />
              <p className="text-sm text-muted">No upcoming events</p>
              <p className="text-xs text-muted-foreground mt-1">
                Check back later for new events
              </p>
            </div>
          )}
        </div>

        {/* Footer */}
        {events.length > 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
            className="mt-4 pt-4 border-t border-border/30"
          >
            <a
              href={`https://www.ticketmaster.com/search?q=${encodeURIComponent(query)}`}
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs text-primary hover:underline flex items-center gap-1"
            >
              <span>Find more events on Ticketmaster</span>
              <ExternalLink className="w-3 h-3" />
            </a>
          </motion.div>
        )}
      </div>
    </motion.div>
  );
}

// Register this widget type as "calendar-card" (matches backend)
registerWidget('calendar-card', CalendarCard);

export default CalendarCard;
