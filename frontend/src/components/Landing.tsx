/**
 * Landing screen - Zen Terminal aesthetic (Japanese Minimal + Terminal).
 */

import { useEffect, useRef, useState } from 'react';
import { motion, useScroll, useTransform, AnimatePresence } from 'framer-motion';
import type { PersonaType } from '../types';

interface LandingProps {
  onGenerate: (persona: PersonaType) => void;
}

export function Landing({ onGenerate }: LandingProps) {
  const [displayedText, setDisplayedText] = useState('');
  const [showContent, setShowContent] = useState(false);
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });
  const [isHovering, setIsHovering] = useState(false);
  const [buttonPos, setButtonPos] = useState({ x: 0, y: 0 });
  const containerRef = useRef<HTMLDivElement>(null);
  const buttonRef = useRef<HTMLButtonElement>(null);

  const bootText = '> system.initialize()';

  // Framer Motion scroll animations (keeping for future use)
  const { scrollYProgress } = useScroll();

  // Track mouse position for parallax
  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setMousePos({
        x: (e.clientX / window.innerWidth - 0.5) * 20,
        y: (e.clientY / window.innerHeight - 0.5) * 20
      });
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  // Smooth typing effect
  useEffect(() => {
    let charIndex = 0;
    const interval = setInterval(() => {
      if (charIndex <= bootText.length) {
        setDisplayedText(bootText.substring(0, charIndex));
        charIndex++;
      } else {
        clearInterval(interval);
        setTimeout(() => setShowContent(true), 600);
      }
    }, 60);

    return () => clearInterval(interval);
  }, []);

  return (
    <div
      ref={containerRef}
      className="relative min-h-screen"
      style={{ background: 'var(--color-paper)' }}
    >
      {/* Static dot grid with ripple effect on button hover */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden" style={{ zIndex: 5 }}>
        {[...Array(200)].map((_, i) => {
          // Create a grid pattern
          const gridCols = 20;
          const gridRows = 10;
          const col = i % gridCols;
          const row = Math.floor(i / gridCols);
          const dotX = (col / (gridCols - 1)) * window.innerWidth;
          const dotY = (row / (gridRows - 1)) * window.innerHeight;

          // Calculate distance from button
          const dx = dotX - buttonPos.x;
          const dy = dotY - buttonPos.y;
          const distance = Math.sqrt(dx * dx + dy * dy);

          // Wave delay based on distance (ripple effect)
          const waveDelay = isHovering ? distance / 500 : 0;

          return (
            <motion.div
              key={i}
              className="absolute rounded-full"
              style={{
                left: `${dotX}px`,
                top: `${dotY}px`,
                width: '4px',
                height: '4px',
                marginLeft: '-2px',
                marginTop: '-2px',
              }}
              animate={{
                backgroundColor: isHovering
                  ? i % 2 === 0
                    ? 'var(--color-crimson)'
                    : 'var(--color-terminal-green)'
                  : 'var(--color-stroke)',
                scale: isHovering ? [1, 1.5, 1] : 1,
                opacity: isHovering ? [0.2, 0.8, 0.3] : 0.2,
              }}
              transition={{
                duration: 1.5,
                delay: waveDelay,
                ease: 'easeOut',
              }}
            />
          );
        })}
      </div>

      {/* Subtle paper texture */}
      <div
        className="fixed inset-0 pointer-events-none opacity-20"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='100' height='100' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence baseFrequency='0.9' /%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03' /%3E%3C/svg%3E")`,
        }}
      />

      {/* Subtle grid - terminal aesthetic */}
      <div
        className="fixed inset-0 pointer-events-none opacity-5"
        style={{
          backgroundImage: `
            linear-gradient(to right, var(--color-stroke) 1px, transparent 1px),
            linear-gradient(to bottom, var(--color-stroke) 1px, transparent 1px)
          `,
          backgroundSize: '60px 60px',
        }}
      />

      {/* Red sun circle - static */}
      <div
        className="fixed"
        style={{
          top: '10%',
          right: '8%',
          width: '120px',
          height: '120px',
          borderRadius: '50%',
          background: 'var(--color-crimson)',
          opacity: 0.15,
        }}
      />

      {/* Secondary geometric elements */}
      <div
        className="fixed"
        style={{
          bottom: '15%',
          left: '5%',
          width: '80px',
          height: '80px',
          border: '1px solid var(--color-stroke)',
          opacity: 0.3,
          transform: `translate(${-mousePos.x * 0.5}px, ${-mousePos.y * 0.5}px) rotate(${mousePos.x}deg)`,
          transition: 'transform 0.3s ease-out',
        }}
      />

      <div
        className="fixed"
        style={{
          top: '40%',
          right: '15%',
          width: '1px',
          height: '150px',
          background: 'var(--color-crimson)',
          opacity: 0.2,
          transform: `translate(${mousePos.x * 0.3}px, ${mousePos.y * 0.3}px)`,
          transition: 'transform 0.2s ease-out',
        }}
      />

      {/* Main content container */}
      <div className="relative z-10 min-h-screen px-12 md:px-32 py-24 flex items-center">
        <div className="w-full">
          {/* Boot text - minimal */}
          <div
            className="mb-20 border-l-2 pl-6"
            style={{
              fontFamily: 'var(--font-family-mono)',
              fontSize: '14px',
              color: 'var(--color-gray)',
              fontWeight: 300,
              borderColor: 'var(--color-terminal-green)',
            }}
          >
            <div className="flex items-center gap-3">
              <span style={{ color: 'var(--color-terminal-green)' }}>▸</span>
              <span>{displayedText}</span>
              {!showContent && <span className="animate-blink">_</span>}
            </div>
          </div>

        {/* Main content - only show after boot */}
        {showContent && (
          <div className="max-w-[1400px] mx-auto">
            {/* Hero section - centered for demo */}
            <div className="max-w-[1200px]">
              <div
                className="mb-12 animate-fade-in"
                style={{
                  animationDelay: '0.1s',
                  fontFamily: 'var(--font-family-mono)',
                  fontSize: '13px',
                  letterSpacing: '0.25em',
                  color: 'var(--color-gray)',
                  fontWeight: 300,
                }}
              >
                ONFABRIC — INTELLIGENCE LAYER
              </div>

              <h1
                className="mb-20 animate-fade-in"
                style={{
                  animationDelay: '0.3s',
                  fontFamily: 'var(--font-family-serif)',
                  fontSize: 'clamp(4rem, 12vw, 10rem)',
                  color: 'var(--color-charcoal)',
                  lineHeight: 1.05,
                  fontWeight: 300,
                }}
              >
                Interfaces
                <br />
                that{' '}
                <span style={{ color: 'var(--color-crimson)' }}>
                  adapt
                </span>
              </h1>

              <div
                className="space-y-8 mb-24 max-w-[600px] animate-fade-in"
                style={{
                  animationDelay: '0.5s',
                  fontFamily: 'var(--font-family-mono)',
                  fontSize: '16px',
                  lineHeight: 2,
                  color: 'var(--color-gray)',
                  fontWeight: 300,
                }}
              >
                <p>
                  AI-generated interfaces built from your digital behavior.
                </p>
                <p>
                  Adaptive. Personal. Evolving.
                </p>
              </div>

              {/* CTA */}
              <div className="animate-fade-in" style={{ animationDelay: '0.7s' }}>
                <motion.button
                  ref={buttonRef}
                  onClick={() => onGenerate('demo')}
                  onMouseEnter={() => {
                    if (buttonRef.current) {
                      const rect = buttonRef.current.getBoundingClientRect();
                      setButtonPos({
                        x: rect.left + rect.width / 2,
                        y: rect.top + rect.height / 2,
                      });
                    }
                    setIsHovering(true);
                  }}
                  onMouseLeave={() => setIsHovering(false)}
                  className="relative px-14 py-6 border-2"
                  style={{
                    borderColor: 'var(--color-charcoal)',
                    background: 'var(--color-white)',
                    fontFamily: 'var(--font-family-mono)',
                    fontSize: '16px',
                    letterSpacing: '0.1em',
                    color: 'var(--color-charcoal)',
                    fontWeight: 500,
                    zIndex: 10,
                  }}
                  whileHover={{
                    x: 8,
                    borderColor: 'var(--color-crimson)',
                    boxShadow: '6px 6px 0px var(--color-crimson)',
                  }}
                  transition={{ type: 'spring', stiffness: 400, damping: 30 }}
                >
                  <span className="flex items-center gap-4">
                    <span>generate( )</span>
                    <motion.span
                      style={{ color: 'var(--color-crimson)', fontSize: '18px' }}
                      initial={{ x: 0 }}
                      whileHover={{ x: 4 }}
                    >
                      →
                    </motion.span>
                  </span>
                </motion.button>

                {/* Subtle hint text */}
                <p
                  className="mt-6 opacity-60"
                  style={{
                    fontFamily: 'var(--font-family-mono)',
                    fontSize: '13px',
                    color: 'var(--color-gray)',
                    fontWeight: 300,
                  }}
                >
                  see your personalized dashboard in ~3 seconds
                </p>
              </div>

              {/* Terminal-style status */}
              <div
                className="mt-16 pt-8 border-t animate-fade-in"
                style={{
                  animationDelay: '0.9s',
                  borderColor: 'var(--color-stroke)',
                  fontFamily: 'var(--font-family-mono)',
                  fontSize: '12px',
                  color: 'var(--color-gray)',
                  letterSpacing: '0.05em',
                  fontWeight: 300,
                }}
              >
                <div className="flex items-center gap-6">
                  <div className="flex items-center gap-2">
                    <div
                      className="w-2 h-2 rounded-full"
                      style={{ background: 'var(--color-terminal-green)' }}
                    />
                    <span>ready</span>
                  </div>
                  <div>·</div>
                  <div>instant</div>
                  <div>·</div>
                  <div>no_signup</div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  </div>
);
}
