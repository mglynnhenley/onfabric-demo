/**
 * ThemeProvider Component
 *
 * Applies backend-generated theme to the entire dashboard:
 * - Injects CSS variables for colors
 * - Loads Google Fonts dynamically
 * - Applies background theme (solid/gradient/pattern)
 * - Handles backdrop blur for glass morphism
 */

import { useEffect } from 'react';
import type { ReactNode } from 'react';
import type { ColorScheme } from '../../types';

interface ThemeProviderProps {
  theme: ColorScheme;
  children: ReactNode;
}

export function ThemeProvider({ theme, children }: ThemeProviderProps) {
  useEffect(() => {
    console.log('🔍 LAYER 6: THEMEPROVIDER RECEIVED THEME');
    console.log('  Theme object:', theme);
    console.log('  Primary:', theme.primary);
    console.log('  Background theme:', theme.background_theme);

    // 1. Inject CSS color variables
    const root = document.documentElement;
    const body = document.body;

    console.log('🔍 LAYER 7: DOM MANIPULATION STARTING');
    console.log('  Body exists:', !!body);
    console.log('  Body current bg:', body.style.background);

    root.style.setProperty('--color-primary', theme.primary);
    root.style.setProperty('--color-secondary', theme.secondary);
    root.style.setProperty('--color-accent', theme.accent);
    root.style.setProperty('--color-foreground', theme.foreground);
    root.style.setProperty('--color-muted', theme.muted);
    root.style.setProperty('--color-success', theme.success);
    root.style.setProperty('--color-warning', theme.warning);
    root.style.setProperty('--color-destructive', theme.destructive);
    root.style.setProperty('--color-border', theme.muted + '40'); // 25% opacity

    console.log('✅ CSS variables set:', {
      primary: getComputedStyle(root).getPropertyValue('--color-primary'),
      cardBg: getComputedStyle(root).getPropertyValue('--card-background'),
    });

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

    // 3. Apply background theme directly to body
    const bg = theme.background_theme;
    let backgroundStyle = '';
    let backgroundSize: string | null = null;

    if (bg.type === 'solid') {
      backgroundStyle = bg.color || '#ffffff';
    } else if (bg.type === 'gradient' && bg.gradient) {
      const { type, colors, direction } = bg.gradient;
      if (type === 'linear') {
        const dir = direction || 'to-br';
        // Convert abbreviated directions to full CSS syntax
        const directionMap: Record<string, string> = {
          'to-br': 'to bottom right',
          'to-bl': 'to bottom left',
          'to-tr': 'to top right',
          'to-tl': 'to top left',
          'to-b': 'to bottom',
          'to-t': 'to top',
          'to-l': 'to left',
          'to-r': 'to right',
        };
        const cssDir = directionMap[dir] || dir;
        backgroundStyle = `linear-gradient(${cssDir}, ${colors.join(', ')})`;
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
      // Create pattern backgrounds using CSS
      const { type, color, opacity, scale } = bg.pattern;
      const patternColor = `${color}${Math.round(opacity * 255).toString(16).padStart(2, '0')}`;

      console.log('🎨 PATTERN DETECTED:', {
        type,
        color,
        opacity,
        scale,
        patternColor,
        bgColor: bg.color
      });

      if (type === 'grid') {
        // Criss-cross grid pattern
        const size = 20 * scale;
        backgroundStyle = `
          repeating-linear-gradient(0deg, transparent, transparent ${size - 1}px, ${patternColor} ${size - 1}px, ${patternColor} ${size}px),
          repeating-linear-gradient(90deg, transparent, transparent ${size - 1}px, ${patternColor} ${size - 1}px, ${patternColor} ${size}px),
          ${bg.color || '#000000'}
        `;
      } else if (type === 'dots') {
        // Dots/circles pattern with base color
        const spacing = 20 * scale; // Scale affects spacing between dots
        const dotRadius = Math.max(3, scale * 1.5); // Scale dot size with pattern scale (min 3px)
        backgroundStyle = `radial-gradient(circle, ${patternColor} ${dotRadius}px, transparent ${dotRadius}px), ${bg.color || '#000000'}`;
        backgroundSize = `${spacing}px ${spacing}px`;

        console.log('🔵 DOTS PATTERN CREATED:', {
          spacing,
          dotRadius,
          backgroundStyle,
          backgroundSize
        });
      } else {
        backgroundStyle = bg.color || '#000000';
      }
    }

    // Set CSS variables
    root.style.setProperty('--background', backgroundStyle);
    root.style.setProperty('--card-background', bg.card_background);

    // Apply background and text colors directly to body element
    // No conflicts now - data-screen="dashboard" clears the CSS layer background
    body.style.background = backgroundStyle;
    body.style.fontFamily = 'var(--font-body)';
    body.style.color = theme.foreground;

    // CRITICAL: Set backgroundSize AFTER setting background (shorthand resets it)
    if (backgroundSize) {
      body.style.backgroundSize = backgroundSize;
      console.log('✅ Background size set AFTER background:', backgroundSize);
    }

    console.log('🔍 LAYER 7: DOM MANIPULATION COMPLETE');
    console.log('  Background style:', backgroundStyle);
    console.log('  Body.style.background:', body.style.background);
    console.log('  Body.style.color:', body.style.color);
    console.log('  Body.style.fontFamily:', body.style.fontFamily);
    console.log('  BG type:', bg.type);
    console.log('  Card background:', bg.card_background);
    console.log('  Backdrop blur:', bg.card_backdrop_blur);

    // Apply backdrop blur if enabled
    if (bg.card_backdrop_blur) {
      root.style.setProperty('--card-backdrop-blur', 'blur(12px)');
    } else {
      root.style.setProperty('--card-backdrop-blur', 'none');
    }

    // Set animation CSS variables and apply animation class to body if defined
    if (theme.background_theme.animation && theme.background_theme.animation.name !== 'none') {
      root.style.setProperty('--animation-duration', theme.background_theme.animation.duration || '20s');
      root.style.setProperty('--animation-timing', theme.background_theme.animation.timing || 'ease-in-out');

      // Apply animation class to body element
      const animationClass = `animate-${theme.background_theme.animation.name}`;
      body.classList.add(animationClass);

      console.log('🎬 Animation applied to body:', {
        duration: theme.background_theme.animation.duration,
        timing: theme.background_theme.animation.timing,
        name: theme.background_theme.animation.name,
        className: animationClass
      });
    }

    // Cleanup on unmount
    return () => {
      document.head.removeChild(headingLink);
      document.head.removeChild(bodyLink);
      document.head.removeChild(monoLink);

      // Reset body styles to defaults
      body.style.background = '';
      body.style.fontFamily = '';
      body.style.color = '';

      // Remove animation class if it was added
      if (theme.background_theme.animation && theme.background_theme.animation.name !== 'none') {
        const animationClass = `animate-${theme.background_theme.animation.name}`;
        body.classList.remove(animationClass);
      }
    };
  }, [theme]);

  return <>{children}</>;
}

export default ThemeProvider;
