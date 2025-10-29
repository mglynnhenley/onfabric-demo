/**
 * Widget Types
 *
 * Shared type definitions for the widget system.
 * Separated from WidgetRegistry to avoid circular dependencies.
 */

export interface WidgetData {
  [key: string]: any;
}

export interface WidgetProps {
  id: string;
  data: WidgetData;
  size: 'small' | 'medium' | 'large';
}
