/**
 * Widget Registry
 *
 * Maps widget type strings to React components.
 * This allows the backend to specify which widget to render
 * without the frontend needing to know the implementation details.
 */

import type { ComponentType } from 'react';
import type { WidgetProps } from './WidgetTypes';

// Re-export types for convenience
export type { WidgetData, WidgetProps } from './WidgetTypes';

// Widget type registry
const WIDGET_REGISTRY: Record<string, ComponentType<WidgetProps>> = {};

/**
 * Register a widget component
 */
export function registerWidget(
  type: string,
  component: ComponentType<WidgetProps>
): void {
  WIDGET_REGISTRY[type] = component;
}

/**
 * Get a widget component by type
 */
export function getWidget(type: string): ComponentType<WidgetProps> | null {
  return WIDGET_REGISTRY[type] || null;
}

/**
 * Get all registered widget types
 */
export function getRegisteredWidgetTypes(): string[] {
  return Object.keys(WIDGET_REGISTRY);
}
