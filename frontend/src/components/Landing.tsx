/**
 * Landing screen - Humanist Tech design with asymmetric bento layout.
 */

import { motion } from 'framer-motion';
import type { PersonaType } from '../types';

interface LandingProps {
  onGenerate: (persona: PersonaType) => void;
}

const personas = [
  {
    id: 'fitness-enthusiast' as PersonaType,
    label: 'Fitness Enthusiast',
    description: 'Workouts, nutrition, wellness tracking',
    icon: (
      <svg className="w-full h-full" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
        <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z" />
      </svg>
    ),
    accentColor: '#D4734B',
  },
  {
    id: 'creative-professional' as PersonaType,
    label: 'Creative Professional',
    description: 'Design, art, creative inspiration',
    icon: (
      <svg className="w-full h-full" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
        <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" />
        <polyline points="3.27 6.96 12 12.01 20.73 6.96" />
        <line x1="12" y1="22.08" x2="12" y2="12" />
      </svg>
    ),
    accentColor: '#E8A960',
  },
  {
    id: 'tech-learner' as PersonaType,
    label: 'Tech Learner',
    description: 'Coding, AI, technology trends',
    icon: (
      <svg className="w-full h-full" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
        <polyline points="16 18 22 12 16 6" />
        <polyline points="8 6 2 12 8 18" />
      </svg>
    ),
    accentColor: '#2C5F5D',
  },
  {
    id: 'remote-worker' as PersonaType,
    label: 'Remote Worker',
    description: 'Travel, productivity, work-life balance',
    icon: (
      <svg className="w-full h-full" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
        <circle cx="12" cy="12" r="10" />
        <line x1="2" y1="12" x2="22" y2="12" />
        <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" />
      </svg>
    ),
    accentColor: '#A8998F',
  },
];

export function Landing({ onGenerate }: LandingProps) {
  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Decorative floating shapes */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <motion.div
          animate={{
            x: [0, 30, 0],
            y: [0, -30, 0],
            rotate: [0, 5, 0]
          }}
          transition={{ duration: 15, repeat: Infinity, ease: "easeInOut" }}
          className="absolute top-20 right-[10%] w-64 h-64 rounded-[40%_60%_70%_30%/60%_30%_70%_40%] bg-gradient-to-br from-terracotta/10 to-amber/5 blur-2xl"
        />
        <motion.div
          animate={{
            x: [0, -40, 0],
            y: [0, 40, 0],
            rotate: [0, -5, 0]
          }}
          transition={{ duration: 20, repeat: Infinity, ease: "easeInOut" }}
          className="absolute bottom-32 left-[5%] w-96 h-96 rounded-[60%_40%_30%_70%/40%_60%_70%_30%] bg-gradient-to-tr from-teal/10 to-soft-peach/10 blur-3xl"
        />
      </div>

      <div className="max-w-[1400px] mx-auto px-8 py-12 relative z-10">
        {/* Hero Section - Asymmetric */}
        <div className="grid lg:grid-cols-[2fr_1fr] gap-8 mb-12">
          {/* Left: Main hero */}
          <motion.div
            className="animate-reveal"
          >
            <div className="inline-flex items-center gap-2 glass rounded-full px-4 py-2 mb-6 shadow-warm">
              <span className="w-2 h-2 rounded-full bg-terracotta animate-pulse-glow" />
              <span className="text-sm font-mono font-medium text-charcoal">Live AI Generation</span>
            </div>

            <h1 className="text-[clamp(3rem,8vw,5.5rem)] font-serif font-semibold text-charcoal mb-6 leading-[0.95] tracking-tight">
              Your Personal
              <br />
              <span className="gradient-text">Intelligence</span>
              {' '}Dashboard
            </h1>

            <p className="text-lg text-charcoal/60 mb-8 max-w-xl leading-relaxed font-sans">
              Watch AI discover patterns in your digital behavior and generate a beautiful, personalized dashboard in real-time.
            </p>

            <div className="flex flex-wrap gap-4 text-sm">
              {[
                { label: 'Pattern Detection', icon: '◆' },
                { label: 'Theme Generation', icon: '◇' },
                { label: 'Live Widgets', icon: '◈' }
              ].map((item, i) => (
                <motion.div
                  key={item.label}
                  className={`animate-reveal-delay-${i * 100 + 100} flex items-center gap-2 px-4 py-2 glass rounded-full shadow-warm`}
                >
                  <span className="text-terracotta font-mono">{item.icon}</span>
                  <span className="font-medium text-charcoal">{item.label}</span>
                </motion.div>
              ))}
            </div>
          </motion.div>

          {/* Right: Stats card */}
          <motion.div
            className="animate-reveal-delay-200 glass rounded-3xl p-8 shadow-warm-lg flex flex-col justify-center"
          >
            <div className="space-y-6">
              <div>
                <div className="text-4xl font-serif font-semibold text-charcoal mb-1">~30s</div>
                <div className="text-sm text-charcoal/50 font-sans">Generation time</div>
              </div>
              <div>
                <div className="text-4xl font-serif font-semibold text-charcoal mb-1">100%</div>
                <div className="text-sm text-charcoal/50 font-sans">AI-powered</div>
              </div>
              <div>
                <div className="text-4xl font-serif font-semibold text-charcoal mb-1">0</div>
                <div className="text-sm text-charcoal/50 font-sans">Setup required</div>
              </div>
            </div>
          </motion.div>
        </div>

        {/* Persona Section - Asymmetric Bento */}
        <motion.div className="animate-reveal-delay-300">
          <h2 className="text-3xl font-serif font-semibold text-charcoal mb-2">
            Choose Your Demo Persona
          </h2>
          <p className="text-charcoal/50 mb-8 font-sans">
            Select a profile to see how AI analyzes behavior patterns
          </p>

          {/* Asymmetric grid layout */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Large card - spans 2 columns on lg */}
            <motion.button
              onClick={() => onGenerate(personas[0].id)}
              className="lg:col-span-2 group relative glass rounded-3xl p-10 text-left hover-lift shadow-warm-lg overflow-hidden"
              style={{
                borderLeft: `4px solid ${personas[0].accentColor}`,
              }}
            >
              <div className="relative z-10">
                <div
                  className="w-16 h-16 mb-6 text-charcoal/80 group-hover:text-charcoal transition-colors"
                  style={{ color: personas[0].accentColor }}
                >
                  {personas[0].icon}
                </div>
                <h3 className="text-3xl font-serif font-semibold text-charcoal mb-3">
                  {personas[0].label}
                </h3>
                <p className="text-charcoal/60 leading-relaxed font-sans">
                  {personas[0].description}
                </p>
              </div>

              <motion.div
                className="absolute -right-8 -bottom-8 w-48 h-48 rounded-full blur-3xl opacity-0 group-hover:opacity-20 transition-opacity"
                style={{ backgroundColor: personas[0].accentColor }}
              />
            </motion.button>

            {/* Regular card */}
            <motion.button
              onClick={() => onGenerate(personas[1].id)}
              className="group relative glass rounded-3xl p-8 text-left hover-lift shadow-warm overflow-hidden"
              style={{
                borderLeft: `4px solid ${personas[1].accentColor}`,
              }}
            >
              <div className="relative z-10">
                <div
                  className="w-14 h-14 mb-5 text-charcoal/80 group-hover:text-charcoal transition-colors"
                  style={{ color: personas[1].accentColor }}
                >
                  {personas[1].icon}
                </div>
                <h3 className="text-2xl font-serif font-semibold text-charcoal mb-2">
                  {personas[1].label}
                </h3>
                <p className="text-sm text-charcoal/60 leading-relaxed font-sans">
                  {personas[1].description}
                </p>
              </div>

              <motion.div
                className="absolute -right-6 -bottom-6 w-32 h-32 rounded-full blur-2xl opacity-0 group-hover:opacity-20 transition-opacity"
                style={{ backgroundColor: personas[1].accentColor }}
              />
            </motion.button>

            {/* Regular card */}
            <motion.button
              onClick={() => onGenerate(personas[2].id)}
              className="group relative glass rounded-3xl p-8 text-left hover-lift shadow-warm overflow-hidden"
              style={{
                borderLeft: `4px solid ${personas[2].accentColor}`,
              }}
            >
              <div className="relative z-10">
                <div
                  className="w-14 h-14 mb-5 text-charcoal/80 group-hover:text-charcoal transition-colors"
                  style={{ color: personas[2].accentColor }}
                >
                  {personas[2].icon}
                </div>
                <h3 className="text-2xl font-serif font-semibold text-charcoal mb-2">
                  {personas[2].label}
                </h3>
                <p className="text-sm text-charcoal/60 leading-relaxed font-sans">
                  {personas[2].description}
                </p>
              </div>

              <motion.div
                className="absolute -right-6 -bottom-6 w-32 h-32 rounded-full blur-2xl opacity-0 group-hover:opacity-20 transition-opacity"
                style={{ backgroundColor: personas[2].accentColor }}
              />
            </motion.button>

            {/* Large card - spans 2 columns on lg */}
            <motion.button
              onClick={() => onGenerate(personas[3].id)}
              className="lg:col-span-2 group relative glass rounded-3xl p-10 text-left hover-lift shadow-warm-lg overflow-hidden"
              style={{
                borderLeft: `4px solid ${personas[3].accentColor}`,
              }}
            >
              <div className="relative z-10">
                <div
                  className="w-16 h-16 mb-6 text-charcoal/80 group-hover:text-charcoal transition-colors"
                  style={{ color: personas[3].accentColor }}
                >
                  {personas[3].icon}
                </div>
                <h3 className="text-3xl font-serif font-semibold text-charcoal mb-3">
                  {personas[3].label}
                </h3>
                <p className="text-charcoal/60 leading-relaxed font-sans">
                  {personas[3].description}
                </p>
              </div>

              <motion.div
                className="absolute -right-8 -bottom-8 w-48 h-48 rounded-full blur-3xl opacity-0 group-hover:opacity-20 transition-opacity"
                style={{ backgroundColor: personas[3].accentColor }}
              />
            </motion.button>
          </div>
        </motion.div>

        {/* Footer */}
        <motion.div
          className="text-center mt-16 space-y-2 animate-reveal-delay-300"
        >
          <p className="text-sm text-charcoal/40 font-mono">
            Demo mode • No signup • Real Claude AI
          </p>
        </motion.div>
      </div>
    </div>
  );
}
