/**
 * Dashboard screen - Renders generated HTML directly in page (no iframe).
 */

import { motion } from 'framer-motion';
import { useEffect, useRef } from 'react';

interface DashboardProps {
  html: string;
  persona: string;
  onGenerateNew: () => void;
}

export function Dashboard({ html, persona, onGenerateNew }: DashboardProps) {
  const contentRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (contentRef.current && html) {
      // Parse HTML and extract body content
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, 'text/html');

      // Get the body content
      const bodyContent = doc.body.innerHTML;

      // Get styles from head
      const styles = Array.from(doc.head.querySelectorAll('style'))
        .map(style => style.innerHTML)
        .join('\n');

      // Inject styles
      const styleElement = document.createElement('style');
      styleElement.innerHTML = styles;
      contentRef.current.innerHTML = '';
      contentRef.current.appendChild(styleElement);

      // Inject body content
      const contentDiv = document.createElement('div');
      contentDiv.innerHTML = bodyContent;
      contentRef.current.appendChild(contentDiv);

      // Execute scripts if any
      const scripts = doc.querySelectorAll('script');
      scripts.forEach(script => {
        const newScript = document.createElement('script');
        if (script.src) {
          newScript.src = script.src;
        } else {
          newScript.textContent = script.textContent;
        }
        contentRef.current?.appendChild(newScript);
      });
    }
  }, [html]);

  const handleDownload = () => {
    const blob = new Blob([html], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    const timestamp = new Date().toISOString().split('T')[0];
    a.download = `fabric-dashboard-${persona}-${timestamp}.html`;
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
    <div className="min-h-screen bg-cream">
      {/* Sticky Header */}
      <motion.div
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="sticky top-0 z-50 glass border-b-2 border-warm-gray shadow-editorial backdrop-blur-xl"
      >
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between flex-wrap gap-4">
            {/* Left: Title */}
            <div className="flex items-center gap-4">
              <motion.div
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ duration: 2, repeat: Infinity }}
                className="w-3 h-3 bg-terracotta rounded-full"
              />
              <div>
                <h1 className="font-display text-2xl md:text-3xl font-bold text-charcoal">
                  Your Dashboard
                </h1>
                <p className="text-sm text-charcoal/50 capitalize">
                  {persona.replace('-', ' ')} persona
                </p>
              </div>
            </div>

            {/* Right: Actions */}
            <div className="flex items-center gap-3">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleShare}
                className="group flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-terracotta to-accent-sage text-white rounded-xl font-semibold text-sm shadow-editorial hover:shadow-editorial-lg transition-all"
              >
                <svg className="w-5 h-5 group-hover:rotate-12 transition-transform" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z" />
                </svg>
                <span className="hidden sm:inline">Share</span>
              </motion.button>

              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleDownload}
                className="group flex items-center gap-2 px-6 py-3 bg-white border-2 border-warm-gray hover:border-terracotta text-charcoal rounded-xl font-semibold text-sm transition-all shadow-editorial"
              >
                <svg className="w-5 h-5 group-hover:translate-y-0.5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
                <span className="hidden sm:inline">Download</span>
              </motion.button>

              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={onGenerateNew}
                className="group flex items-center gap-2 px-6 py-3 bg-white border-2 border-warm-gray hover:border-sage text-charcoal rounded-xl font-semibold text-sm transition-all shadow-editorial"
              >
                <svg className="w-5 h-5 group-hover:rotate-180 transition-transform duration-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
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
        className="max-w-7xl mx-auto px-6 py-8"
      >
        {/* Success Banner */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-r from-terracotta/10 via-sage/10 to-terracotta/10 border-2 border-warm-gray rounded-2xl p-6 mb-8 shadow-editorial"
        >
          <div className="flex items-start gap-4">
            <motion.div
              animate={{ rotate: [0, 10, -10, 0] }}
              transition={{ duration: 0.5, delay: 0.5 }}
              className="text-4xl"
            >
              ✨
            </motion.div>
            <div className="flex-1">
              <h3 className="font-display text-xl font-bold text-charcoal mb-2">
                Your Dashboard is Ready!
              </h3>
              <p className="text-sm text-charcoal/60 leading-relaxed">
                AI analyzed your digital behavior and created a personalized dashboard with unique insights and live widgets.
                Scroll down to explore, then share your results or download the HTML file.
              </p>
            </div>
          </div>
        </motion.div>

        {/* Rendered Dashboard */}
        <motion.div
          initial={{ opacity: 0, scale: 0.98 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.4, duration: 0.6 }}
          className="bg-white rounded-3xl shadow-editorial-xl overflow-hidden border-2 border-warm-gray"
        >
          <div
            ref={contentRef}
            className="dashboard-content"
          />
        </motion.div>

        {/* Footer Actions */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6 }}
          className="text-center mt-12 space-y-4"
        >
          <p className="text-sm text-charcoal/50">
            Love your dashboard? Share it with friends or try another persona!
          </p>
          <div className="flex justify-center gap-4">
            <button
              onClick={handleShare}
              className="text-terracotta hover:underline font-medium text-sm"
            >
              Share on Twitter →
            </button>
            <button
              onClick={onGenerateNew}
              className="text-sage hover:underline font-medium text-sm"
            >
              Generate New Dashboard →
            </button>
          </div>
          <p className="text-xs text-charcoal/30 mt-6">
            Generated with Fabric • Powered by Claude AI
          </p>
        </motion.div>
      </motion.div>
    </div>
  );
}
