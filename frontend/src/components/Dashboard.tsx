/**
 * Dashboard screen - Minimal header with generated HTML display.
 */

import { useEffect, useRef } from 'react';

interface DashboardProps {
  html: string;
  persona: string;
  onGenerateNew: () => void;
}

export function Dashboard({ html, onGenerateNew }: DashboardProps) {
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
    a.download = `dashboard-${timestamp}.html`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div
      className="min-h-screen flex flex-col"
      style={{ background: 'var(--color-paper)' }}
    >
      {/* Subtle paper texture */}
      <div
        className="fixed inset-0 pointer-events-none opacity-20"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='100' height='100' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence baseFrequency='0.9' /%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03' /%3E%3C/svg%3E")`,
        }}
      />

      {/* Zen Terminal Header */}
      <div
        className="relative z-10 border-b px-8 py-6 flex items-center justify-between"
        style={{ borderColor: 'var(--color-stroke)' }}
      >
        <div
          className="flex items-center gap-3"
          style={{
            fontFamily: 'var(--font-family-mono)',
            fontSize: '12px',
            color: 'var(--color-gray)',
            fontWeight: 300,
          }}
        >
          <span style={{ color: 'var(--color-terminal-green)' }}>▸</span>
          <span>dashboard.ready()</span>
        </div>
        <div className="flex items-center gap-8">
          <button
            onClick={handleDownload}
            className="group flex items-center gap-2 transition-all duration-300 hover:translate-x-1"
            style={{
              fontFamily: 'var(--font-family-mono)',
              fontSize: '11px',
              letterSpacing: '0.05em',
              color: 'var(--color-gray)',
              fontWeight: 400,
            }}
          >
            <span className="group-hover:text-charcoal transition-colors" style={{ color: 'inherit' }}>
              download
            </span>
            <span style={{ color: 'var(--color-crimson)' }}>↓</span>
          </button>
          <button
            onClick={onGenerateNew}
            className="group flex items-center gap-2 px-4 py-2 border transition-all duration-300 hover:shadow-sm"
            style={{
              borderColor: 'var(--color-stroke)',
              background: 'var(--color-white)',
              fontFamily: 'var(--font-family-mono)',
              fontSize: '11px',
              letterSpacing: '0.05em',
              color: 'var(--color-charcoal)',
              fontWeight: 400,
            }}
          >
            <span>new</span>
            <span style={{ color: 'var(--color-terminal-green)' }}>→</span>
          </button>
        </div>
      </div>

      {/* Dashboard Content */}
      <div ref={contentRef} className="relative z-10 flex-1" />
    </div>
  );
}
