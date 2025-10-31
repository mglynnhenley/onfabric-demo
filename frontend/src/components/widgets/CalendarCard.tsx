/**
 * CalendarCard Widget (EventCalendar)
 *
 * Displays upcoming events from Ticketmaster.
 * Shows a monthly calendar view with highlighted event dates.
 */

import { motion } from 'framer-motion';
import { Calendar, ChevronLeft, ChevronRight } from 'lucide-react';
import { registerWidget } from './WidgetRegistry';
import type { WidgetProps } from './WidgetTypes';
import { useMemo, useState } from 'react';

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

  // Get current month for calendar view
  const [currentDate] = useState(new Date());

  // Get events by date
  const eventsByDate = useMemo(() => {
    const map = new Map<string, Event[]>();
    events.forEach(event => {
      try {
        const date = new Date(event.date);
        const dateKey = `${date.getFullYear()}-${date.getMonth()}-${date.getDate()}`;
        if (!map.has(dateKey)) {
          map.set(dateKey, []);
        }
        map.get(dateKey)!.push(event);
      } catch (e) {
        // Skip invalid dates
      }
    });
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
          {query && (
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
                  className={`
                    aspect-square rounded-md flex items-center justify-center text-[9px] font-medium relative
                    transition-colors cursor-default
                    ${hasEvents
                      ? 'bg-gradient-to-br from-primary to-secondary text-white shadow-sm'
                      : isToday
                      ? 'bg-muted/30 text-foreground ring-1 ring-primary'
                      : 'text-muted hover:bg-muted/20'
                    }
                  `}
                  title={hasEvents ? `${dayData.events.length} event${dayData.events.length > 1 ? 's' : ''}` : ''}
                >
                  <span>{dayData.day}</span>
                  {hasEvents && dayData.events.length > 1 && (
                    <div className="absolute bottom-0.5 right-0.5 w-1 h-1 rounded-full bg-white/80" />
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
    </motion.div>
  );
}

// Register this widget type as "calendar-card" (matches backend)
registerWidget('calendar-card', CalendarCard);

export default CalendarCard;
