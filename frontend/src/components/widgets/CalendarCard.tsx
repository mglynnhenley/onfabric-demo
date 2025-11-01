/**
 * CalendarCard Widget (EventCalendar)
 *
 * Displays upcoming events from Ticketmaster.
 * Shows a monthly calendar view with highlighted event dates.
 */

import { motion, AnimatePresence } from 'framer-motion';
import { Calendar, ChevronLeft, ChevronRight, MapPin } from 'lucide-react';
import { registerWidget } from './WidgetRegistry';
import type { WidgetProps } from './WidgetTypes';
import { useMemo, useState } from 'react';

interface Event {
  title: string;
  date: string;
  location: string;
  url: string;
  type?: string;
}

interface CalendarCardData {
  title: string;
  search_query: string;
  enriched_events: Event[];
}

function CalendarCard({ id, data, size }: WidgetProps) {
  const calendarData = data as CalendarCardData;
  const { title, search_query, enriched_events } = calendarData;
  const events = enriched_events || [];

  // Debug logging
  console.log('📅 CalendarCard received data:', {
    rawData: data,
    title,
    search_query,
    enriched_events,
    eventsCount: events.length,
    firstEvent: events[0],
    allEventDates: events.map(e => e.date)
  });

  // Get current month for calendar view - start from November 2025
  const [currentDate] = useState(new Date(2025, 10)); // Month 10 = November
  const [hoveredDay, setHoveredDay] = useState<number | null>(null);
  const [tooltipPosition, setTooltipPosition] = useState<{ x: number; y: number } | null>(null);

  // Get events by date
  const eventsByDate = useMemo(() => {
    console.log('📅 Building eventsByDate map from events:', events);
    const map = new Map<string, Event[]>();
    events.forEach(event => {
      try {
        const date = new Date(event.date);
        const dateKey = `${date.getFullYear()}-${date.getMonth()}-${date.getDate()}`;
        console.log('📅 Processing event:', {
          eventTitle: event.title,
          eventDate: event.date,
          parsedDate: date.toISOString(),
          dateKey
        });
        if (!map.has(dateKey)) {
          map.set(dateKey, []);
        }
        map.get(dateKey)!.push(event);
      } catch (e) {
        console.error('📅 Failed to parse event date:', event, e);
      }
    });
    console.log('📅 Final eventsByDate map:', Array.from(map.entries()));
    return map;
  }, [events]);

  // Generate calendar days
  const calendarDays = useMemo(() => {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const daysInMonth = lastDay.getDate();
    const startingDayOfWeek = firstDay.getDay();

    const days = [];

    // Add empty cells for days before month starts
    for (let i = 0; i < startingDayOfWeek; i++) {
      days.push(null);
    }

    // Add days of month
    for (let day = 1; day <= daysInMonth; day++) {
      const dateKey = `${year}-${month}-${day}`;
      const dayEvents = eventsByDate.get(dateKey) || [];
      days.push({
        day,
        events: dayEvents,
        date: new Date(year, month, day),
      });
    }

    return days;
  }, [currentDate, eventsByDate]);

  const monthName = currentDate.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });

  const weekDays = ['S', 'M', 'T', 'W', 'T', 'F', 'S'];

  // Get events for hovered day
  const hoveredDayEvents = useMemo(() => {
    if (hoveredDay === null) return [];
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    const dateKey = `${year}-${month}-${hoveredDay}`;
    return eventsByDate.get(dateKey) || [];
  }, [hoveredDay, currentDate, eventsByDate]);

  // Handle mouse enter on calendar day
  const handleDayMouseEnter = (day: number, event: React.MouseEvent<HTMLDivElement>) => {
    setHoveredDay(day);
    const rect = event.currentTarget.getBoundingClientRect();
    setTooltipPosition({
      x: rect.left + rect.width / 2,
      y: rect.top - 8,
    });
  };

  // Handle mouse leave
  const handleDayMouseLeave = () => {
    setHoveredDay(null);
    setTooltipPosition(null);
  };

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
            <Calendar className="w-4 h-4 text-primary" />
            {title}
          </h3>
        </div>

        {/* Month Display */}
        <div className="flex items-center justify-between mb-3">
          <span className="text-xs font-medium text-foreground">{monthName}</span>
          {search_query && (
            <span className="text-[9px] text-muted">{events.length} events</span>
          )}
        </div>

        {/* Calendar Grid */}
        <div className="flex-1 flex flex-col gap-1">
          {/* Week Day Headers */}
          <div className="grid grid-cols-7 gap-1 mb-1">
            {weekDays.map((day, idx) => (
              <div
                key={idx}
                className="text-[8px] font-medium text-muted text-center"
              >
                {day}
              </div>
            ))}
          </div>

          {/* Calendar Days */}
          <div className="grid grid-cols-7 gap-1 flex-1">
            {calendarDays.map((dayData, idx) => {
              if (!dayData) {
                return <div key={`empty-${idx}`} className="aspect-square" />;
              }

              const hasEvents = dayData.events.length > 0;
              const isToday = dayData.date.toDateString() === new Date().toDateString();

              return (
                <motion.div
                  key={idx}
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: idx * 0.01 }}
                  onMouseEnter={(e) => hasEvents && handleDayMouseEnter(dayData.day, e)}
                  onMouseLeave={handleDayMouseLeave}
                  className={`
                    aspect-square rounded-md flex items-center justify-center text-[9px] font-medium relative
                    transition-all duration-200
                    ${hasEvents
                      ? 'bg-primary text-black font-bold shadow-lg shadow-primary/50 cursor-pointer hover:shadow-xl hover:shadow-primary/70 hover:scale-110 ring-2 ring-primary/30'
                      : isToday
                      ? 'bg-muted/30 text-foreground ring-1 ring-primary cursor-default'
                      : 'text-muted hover:bg-muted/20 cursor-default'
                    }
                  `}
                >
                  <span>{dayData.day}</span>
                  {hasEvents && dayData.events.length > 1 && (
                    <div className="absolute bottom-0.5 right-0.5 flex gap-0.5">
                      {Array.from({ length: Math.min(dayData.events.length, 3) }).map((_, i) => (
                        <div key={i} className="w-1 h-1 rounded-full bg-black" />
                      ))}
                    </div>
                  )}
                </motion.div>
              );
            })}
          </div>
        </div>

        {/* Empty State */}
        {events.length === 0 && (
          <div className="flex flex-col items-center justify-center flex-1 text-center">
            <Calendar className="w-8 h-8 text-muted mb-2 opacity-30" />
            <p className="text-[9px] text-muted">No events this month</p>
          </div>
        )}
      </div>

      {/* Tooltip for events */}
      <AnimatePresence>
        {hoveredDay !== null && hoveredDayEvents.length > 0 && tooltipPosition && (
          <motion.div
            initial={{ opacity: 0, y: 10, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 10, scale: 0.9 }}
            transition={{ duration: 0.2 }}
            style={{
              position: 'fixed',
              left: `${tooltipPosition.x}px`,
              top: `${tooltipPosition.y}px`,
              transform: 'translate(-50%, -100%)',
              zIndex: 9999,
              pointerEvents: 'none',
            }}
            className="max-w-xs"
          >
            <div className="bg-black border-2 border-primary rounded-lg shadow-2xl shadow-primary/50 p-3 space-y-2">
              {hoveredDayEvents.map((event, idx) => (
                <div
                  key={idx}
                  className="space-y-1 pb-2 last:pb-0 border-b border-primary/30 last:border-0"
                >
                  <div className="flex items-start justify-between gap-2">
                    <h4 className="text-[10px] font-mono font-bold text-primary leading-tight">
                      {event.title}
                    </h4>
                    {event.type && (
                      <span
                        className={`text-[8px] px-1.5 py-0.5 rounded font-mono font-medium flex-shrink-0 ${
                          event.type === 'startup'
                            ? 'bg-primary/30 text-primary border border-primary/50'
                            : 'bg-secondary/30 text-secondary border border-secondary/50'
                        }`}
                      >
                        {event.type}
                      </span>
                    )}
                  </div>
                  <div className="flex items-center gap-1 text-[9px] text-secondary">
                    <MapPin className="w-2.5 h-2.5" />
                    <span className="leading-tight font-mono">{event.location}</span>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}

// Register this widget type as "calendar-card" (matches backend)
registerWidget('calendar-card', CalendarCard);

export default CalendarCard;
