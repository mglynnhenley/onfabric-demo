/**
 * ThemeProvider Component
 *
 * Applies backend-generated theme to the entire dashboard:
 * - Injects CSS variables for colors
 * - Loads Google Fonts dynamically
 * - Applies background theme (solid/gradient/pattern)
 * - Handles backdrop blur for glass morphism
 */

import { useEffect, ReactNode } from 'react';

interface FontScheme {
  heading: string;
  body: string;
  mono: string;
  heading_url: string;
  body_url: string;
  mono_url: string;
}

interface GradientConfig {
  type: 'linear' | 'radial' | 'mesh';
  colors: string[];
  direction?: string;
}

interface PatternConfig {
  type: 'dots' | 'grid' | 'noise' | 'geometric';
  color: string;
  opacity: number;
  scale: number;
}

interface BackgroundTheme {
  type: 'solid' | 'gradient' | 'pattern' | 'animated';
  color?: string;
  gradient?: GradientConfig;
  pattern?: PatternConfig;
  card_background: string;
  card_backdrop_blur: boolean;
}

interface ColorScheme {
  // Primary palette
  primary: string;
  secondary: string;
  accent: string;

  // Text
  foreground: string;
  muted: string;

  // Semantic
  success: string;
  warning: string;
  destructive: string;

  // Theming
  background_theme: BackgroundTheme;
  fonts: FontScheme;

  // Metadata
  mood: string;
  rationale: string;
}

interface ThemeProviderProps {
  theme: ColorScheme;
  children: ReactNode;
}

export function ThemeProvider({ theme, children }: ThemeProviderProps) {
  useEffect(() => {
    // 1. Inject CSS color variables
    const root = document.documentElement;

    root.style.setProperty('--color-primary', theme.primary);
    root.style.setProperty('--color-secondary', theme.secondary);
    root.style.setProperty('--color-accent', theme.accent);
    root.style.setProperty('--color-foreground', theme.foreground);
    root.style.setProperty('--color-muted', theme.muted);
    root.style.setProperty('--color-success', theme.success);
    root.style.setProperty('--color-warning', theme.warning);
    root.style.setProperty('--color-destructive', theme.destructive);
    root.style.setProperty('--color-border', theme.muted + '40'); // 25% opacity

    // 2. Load Google Fonts
    const loadFont = (url: string) => {
      const link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = url;
      document.head.appendChild(link);
      return link;
    };

    const headingLink = loadFont(theme.fonts.heading_url);
    const bodyLink = loadFont(theme.fonts.body_url);
    const monoLink = loadFont(theme.fonts.mono_url);

    // Set font families
    root.style.setProperty('--font-heading', theme.fonts.heading);
    root.style.setProperty('--font-body', theme.fonts.body);
    root.style.setProperty('--font-mono', theme.fonts.mono);

    // 3. Apply background theme
    const bg = theme.background_theme;
    let backgroundStyle = '';

    if (bg.type === 'solid') {
      backgroundStyle = bg.color || '#ffffff';
    } else if (bg.type === 'gradient' && bg.gradient) {
      const { type, colors, direction } = bg.gradient;
      if (type === 'linear') {
        const dir = direction || 'to-br';
        const cssDir = dir.replace('to-', '').replace('-', ' ');
        backgroundStyle = `linear-gradient(to ${cssDir}, ${colors.join(', ')})`;
      } else if (type === 'radial') {
        backgroundStyle = `radial-gradient(circle, ${colors.join(', ')})`;
      } else if (type === 'mesh') {
        // Mesh gradient approximation using multiple radial gradients
        backgroundStyle = colors
          .map((color, i) => {
            const x = (i * 30 + 20) % 100;
            const y = (i * 40 + 30) % 100;
            return `radial-gradient(at ${x}% ${y}%, ${color} 0%, transparent 50%)`;
          })
          .join(', ');
      }
    } else if (bg.type === 'pattern' && bg.pattern) {
      // Pattern backgrounds would require SVG generation
      // For now, use a simple fallback
      backgroundStyle = bg.color || '#ffffff';
    }

    root.style.setProperty('--background', backgroundStyle);
    root.style.setProperty('--card-background', bg.card_background);

    // Apply backdrop blur if enabled
    if (bg.card_backdrop_blur) {
      root.style.setProperty('--card-backdrop-blur', 'blur(12px)');
    } else {
      root.style.setProperty('--card-backdrop-blur', 'none');
    }

    // Cleanup on unmount
    return () => {
      document.head.removeChild(headingLink);
      document.head.removeChild(bodyLink);
      document.head.removeChild(monoLink);
    };
  }, [theme]);

  return (
    <div
      className="theme-wrapper min-h-screen"
      style={{
        background: 'var(--background)',
        fontFamily: 'var(--font-body)',
      }}
    >
      {children}
    </div>
  );
}

export default ThemeProvider;
