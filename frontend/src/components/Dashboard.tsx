/**
 * Dashboard screen - Renders JSON dashboard with dynamic widgets
 */

import { motion } from 'framer-motion';
import { useState } from 'react';
import { ThemeProvider } from './theme/ThemeProvider';
import { PinBoardLayout } from './dashboard/PinBoardLayout';

// Import widgets to ensure they register
import './widgets/StatCard';
import './widgets/ArticleCard';
import './widgets/InfoCard';
import './widgets/MapCard';
import './widgets/VideoCard';
import './widgets/CalendarCard';
import './widgets/TaskCard';
import './widgets/ContentCard';

interface PersonaProfile {
  writing_style: string;
  interests: string[];
  activity_level: string;
  professional_context?: string;
  tone_preference: string;
  age_range?: string;
  content_depth_preference: string;
}

interface FontScheme {
  heading: string;
  body: string;
  mono: string;
  heading_url: string;
  body_url: string;
  mono_url: string;
}

interface BackgroundTheme {
  type: string;
  color?: string;
  gradient?: {
    type: string;
    colors: string[];
    direction?: string;
  };
  pattern?: {
    type: string;
    color: string;
    opacity: number;
    scale: number;
  };
  card_background: string;
  card_backdrop_blur: boolean;
}

interface ColorScheme {
  primary: string;
  secondary: string;
  accent: string;
  foreground: string;
  muted: string;
  success: string;
  warning: string;
  destructive: string;
  background_theme: BackgroundTheme;
  fonts: FontScheme;
  mood: string;
  rationale: string;
}

interface Widget {
  id: string;
  type: string;
  size: 'small' | 'medium' | 'large';
  priority: number;
  data: Record<string, any>;
}

interface DashboardJSON {
  id: string;
  generated_at: string;
  widgets: Widget[];
  theme: ColorScheme;
  persona: PersonaProfile;
}

interface DashboardProps {
  dashboardData: DashboardJSON;
  onGenerateNew: () => void;
}

export function Dashboard({ dashboardData, onGenerateNew }: DashboardProps) {
  const [isReady, setIsReady] = useState(true);

  const handleDownload = () => {
    // Convert dashboard data to JSON and download
    const json = JSON.stringify(dashboardData, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    const timestamp = new Date().toISOString().split('T')[0];
    a.download = `fabric-dashboard-${dashboardData.id}-${timestamp}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleShare = () => {
    const text = `Just generated my personalized intelligence dashboard with @FabricAI! 🎨✨\n\nAI discovered patterns in my digital behavior and created a beautiful dashboard with live widgets. See what AI can discover about you!`;
    const url = `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}`;
    window.open(url, '_blank', 'width=550,height=420');
  };

  return (
    <ThemeProvider theme={dashboardData.theme}>
      <div className="min-h-screen">
        {/* Sticky Header */}
        <motion.div
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="sticky top-0 z-50 backdrop-blur-xl border-b border-border/50"
          style={{
            background: 'var(--card-background)',
            backdropFilter: 'var(--card-backdrop-blur)',
          }}
        >
          <div className="max-w-7xl mx-auto px-6 py-4">
            <div className="flex items-center justify-between flex-wrap gap-4">
              {/* Left: Title */}
              <div className="flex items-center gap-4">
                <motion.div
                  animate={{ scale: [1, 1.2, 1] }}
                  transition={{ duration: 2, repeat: Infinity }}
                  className="w-3 h-3 rounded-full"
                  style={{ backgroundColor: 'var(--color-primary)' }}
                />
                <div>
                  <h1
                    className="text-2xl md:text-3xl font-bold"
                    style={{
                      fontFamily: 'var(--font-heading)',
                      color: 'var(--color-foreground)',
                    }}
                  >
                    Your Dashboard
                  </h1>
                  <p
                    className="text-sm capitalize"
                    style={{ color: 'var(--color-muted)' }}
                  >
                    {dashboardData.persona.writing_style} persona
                  </p>
                </div>
              </div>

              {/* Right: Actions */}
              <div className="flex items-center gap-3">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={handleShare}
                  className="group flex items-center gap-2 px-6 py-3 text-white rounded-xl font-semibold text-sm shadow-lg transition-all"
                  style={{ backgroundColor: 'var(--color-primary)' }}
                >
                  <svg
                    className="w-5 h-5 group-hover:rotate-12 transition-transform"
                    fill="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z" />
                  </svg>
                  <span className="hidden sm:inline">Share</span>
                </motion.button>

                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={handleDownload}
                  className="group flex items-center gap-2 px-6 py-3 rounded-xl font-semibold text-sm transition-all shadow-lg border"
                  style={{
                    backgroundColor: 'var(--card-background)',
                    color: 'var(--color-foreground)',
                    borderColor: 'var(--color-border)',
                  }}
                >
                  <svg
                    className="w-5 h-5 group-hover:translate-y-0.5 transition-transform"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                    />
                  </svg>
                  <span className="hidden sm:inline">Download</span>
                </motion.button>

                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={onGenerateNew}
                  className="group flex items-center gap-2 px-6 py-3 rounded-xl font-semibold text-sm transition-all shadow-lg border"
                  style={{
                    backgroundColor: 'var(--card-background)',
                    color: 'var(--color-foreground)',
                    borderColor: 'var(--color-border)',
                  }}
                >
                  <svg
                    className="w-5 h-5 group-hover:rotate-180 transition-transform duration-500"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                    />
                  </svg>
                  <span className="hidden sm:inline">New</span>
                </motion.button>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Dashboard Content */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="py-8"
        >
          {/* Pin Board Layout with Widgets */}
          <PinBoardLayout widgets={dashboardData.widgets} />

          {/* Footer Actions */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.6 }}
            className="text-center mt-12 space-y-4 px-6"
          >
            <p className="text-sm" style={{ color: 'var(--color-muted)' }}>
              Love your dashboard? Share it with friends or try another persona!
            </p>
            <div className="flex justify-center gap-4">
              <button
                onClick={handleShare}
                className="font-medium text-sm hover:underline"
                style={{ color: 'var(--color-primary)' }}
              >
                Share on Twitter →
              </button>
              <button
                onClick={onGenerateNew}
                className="font-medium text-sm hover:underline"
                style={{ color: 'var(--color-secondary)' }}
              >
                Generate New Dashboard →
              </button>
            </div>
            <p className="text-xs mt-6" style={{ color: 'var(--color-muted)' }}>
              Generated with Fabric • Powered by Claude AI
            </p>
          </motion.div>
        </motion.div>
      </div>
    </ThemeProvider>
  );
}
