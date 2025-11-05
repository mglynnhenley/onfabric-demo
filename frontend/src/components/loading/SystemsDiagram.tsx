import React from 'react';
import { motion } from 'framer-motion';

export const SystemsDiagram = () => {
  const COLORS = {
    crimson: '#DC143C',
    terminalGreen: '#00AA2E',
    stroke: '#E5E5E5',
    charcoal: '#2B2726',
    gray: '#8B8B8B',
    paper: '#FAFAFA',
  };

  return (
    <div className="p-6" style={{ fontFamily: 'var(--font-family-mono)' }}>
      <h2
        className="text-2xl mb-6 text-center"
        style={{
          fontFamily: 'var(--font-family-serif)',
          color: COLORS.charcoal,
          letterSpacing: '-0.02em'
        }}
      >
        OnFabric Pipeline Architecture
      </h2>

      <svg
        viewBox="0 0 800 600"
        className="w-full h-full"
        style={{ maxHeight: '500px' }}
      >
        {/* Background grid */}
        <defs>
          <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
            <path
              d="M 20 0 L 0 0 0 20"
              fill="none"
              stroke={COLORS.stroke}
              strokeWidth="0.5"
              opacity="0.3"
            />
          </pattern>

          {/* Arrow marker */}
          <marker
            id="arrowhead"
            markerWidth="10"
            markerHeight="10"
            refX="9"
            refY="3"
            orient="auto"
          >
            <polygon
              points="0 0, 10 3, 0 6"
              fill={COLORS.crimson}
            />
          </marker>

          {/* Gradient definitions */}
          <linearGradient id="dataGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor={COLORS.crimson} stopOpacity="0.1" />
            <stop offset="100%" stopColor={COLORS.crimson} stopOpacity="0.3" />
          </linearGradient>

          <linearGradient id="processGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor={COLORS.terminalGreen} stopOpacity="0.1" />
            <stop offset="100%" stopColor={COLORS.terminalGreen} stopOpacity="0.3" />
          </linearGradient>
        </defs>

        <rect width="800" height="600" fill="url(#grid)" />

        {/* Title Section */}
        <text x="400" y="30" textAnchor="middle" fill={COLORS.charcoal} fontSize="14" fontWeight="600">
          SYSTEM FLOW DIAGRAM
        </text>

        {/* Data Sources Layer */}
        <g transform="translate(50, 80)">
          <rect
            x="0" y="0" width="140" height="80"
            fill="url(#dataGradient)"
            stroke={COLORS.crimson}
            strokeWidth="2"
            rx="4"
          />
          <text x="70" y="25" textAnchor="middle" fill={COLORS.charcoal} fontSize="12" fontWeight="600">
            DATA SOURCES
          </text>
          <text x="70" y="45" textAnchor="middle" fill={COLORS.gray} fontSize="10">Instagram</text>
          <text x="70" y="58" textAnchor="middle" fill={COLORS.gray} fontSize="10">Google</text>
          <text x="70" y="71" textAnchor="middle" fill={COLORS.gray} fontSize="10">Pinterest</text>
        </g>

        {/* OnFabric API */}
        <g transform="translate(250, 80)">
          <rect
            x="0" y="0" width="140" height="80"
            fill={COLORS.paper}
            stroke={COLORS.charcoal}
            strokeWidth="1.5"
            rx="4"
          />
          <text x="70" y="30" textAnchor="middle" fill={COLORS.charcoal} fontSize="12" fontWeight="600">
            OnFabric API
          </text>
          <text x="70" y="50" textAnchor="middle" fill={COLORS.gray} fontSize="9">10,543 interactions</text>
        </g>

        {/* Arrow from Data Sources to OnFabric API */}
        <line
          x1="190" y1="120"
          x2="250" y2="120"
          stroke={COLORS.crimson}
          strokeWidth="2"
          markerEnd="url(#arrowhead)"
        />

        {/* Pattern Detector */}
        <g transform="translate(450, 80)">
          <rect
            x="0" y="0" width="140" height="80"
            fill="url(#processGradient)"
            stroke={COLORS.terminalGreen}
            strokeWidth="2"
            rx="4"
          />
          <text x="70" y="25" textAnchor="middle" fill={COLORS.charcoal} fontSize="12" fontWeight="600">
            Pattern Detector
          </text>
          <text x="70" y="43" textAnchor="middle" fill={COLORS.gray} fontSize="9">Machine Learning</text>
          <text x="70" y="56" textAnchor="middle" fill={COLORS.gray} fontSize="9">Persona Analysis</text>
        </g>

        {/* Arrow from OnFabric API to Pattern Detector */}
        <line
          x1="390" y1="120"
          x2="450" y2="120"
          stroke={COLORS.terminalGreen}
          strokeWidth="2"
          markerEnd="url(#arrowhead)"
        />

        {/* Theme Generator */}
        <g transform="translate(250, 200)">
          <rect
            x="0" y="0" width="140" height="80"
            fill={COLORS.paper}
            stroke={COLORS.charcoal}
            strokeWidth="1.5"
            rx="4"
          />
          <text x="70" y="30" textAnchor="middle" fill={COLORS.charcoal} fontSize="12" fontWeight="600">
            Theme Generator
          </text>
          <text x="70" y="50" textAnchor="middle" fill={COLORS.gray} fontSize="9">Visual Aesthetics</text>
        </g>

        {/* UI Generator */}
        <g transform="translate(450, 200)">
          <rect
            x="0" y="0" width="140" height="80"
            fill={COLORS.paper}
            stroke={COLORS.charcoal}
            strokeWidth="1.5"
            rx="4"
          />
          <text x="70" y="30" textAnchor="middle" fill={COLORS.charcoal} fontSize="12" fontWeight="600">
            UI Generator
          </text>
          <text x="70" y="50" textAnchor="middle" fill={COLORS.gray} fontSize="9">Widget Selection</text>
        </g>

        {/* Arrows from Pattern Detector */}
        <line
          x1="490" y1="160"
          x2="370" y2="200"
          stroke={COLORS.gray}
          strokeWidth="1.5"
          markerEnd="url(#arrowhead)"
        />
        <line
          x1="530" y1="160"
          x2="530" y2="200"
          stroke={COLORS.gray}
          strokeWidth="1.5"
          markerEnd="url(#arrowhead)"
        />

        {/* Content Writer */}
        <g transform="translate(250, 320)">
          <rect
            x="0" y="0" width="140" height="80"
            fill="url(#processGradient)"
            stroke={COLORS.terminalGreen}
            strokeWidth="2"
            rx="4"
          />
          <text x="70" y="30" textAnchor="middle" fill={COLORS.charcoal} fontSize="12" fontWeight="600">
            Content Writer
          </text>
          <text x="70" y="50" textAnchor="middle" fill={COLORS.gray} fontSize="9">AI Generation</text>
        </g>

        {/* API Enrichment - moved after UI Generator */}
        <g transform="translate(450, 320)">
          <rect
            x="0" y="0" width="140" height="80"
            fill="url(#dataGradient)"
            stroke={COLORS.crimson}
            strokeWidth="2"
            rx="4"
          />
          <text x="70" y="25" textAnchor="middle" fill={COLORS.charcoal} fontSize="12" fontWeight="600">
            API ENRICHMENT
          </text>
          <text x="70" y="43" textAnchor="middle" fill={COLORS.gray} fontSize="9">Weather API</text>
          <text x="70" y="56" textAnchor="middle" fill={COLORS.gray} fontSize="9">YouTube API</text>
          <text x="70" y="69" textAnchor="middle" fill={COLORS.gray} fontSize="9">Ticketmaster API</text>
        </g>

        {/* Dashboard Builder */}
        <g transform="translate(350, 450)">
          <rect
            x="0" y="0" width="140" height="80"
            fill={COLORS.paper}
            stroke={COLORS.crimson}
            strokeWidth="2.5"
            rx="4"
            strokeDasharray="5,3"
          />
          <text x="70" y="30" textAnchor="middle" fill={COLORS.charcoal} fontSize="13" fontWeight="700">
            Dashboard Builder
          </text>
          <text x="70" y="50" textAnchor="middle" fill={COLORS.gray} fontSize="9">Final Assembly</text>
        </g>

        {/* Arrow from UI Generator to API Enrichment */}
        <line
          x1="520" y1="280"
          x2="520" y2="320"
          stroke={COLORS.terminalGreen}
          strokeWidth="2"
          markerEnd="url(#arrowhead)"
        />

        {/* Arrow from Pattern Detector to Content Writer */}
        <line
          x1="520" y1="160"
          x2="320" y2="320"
          stroke={COLORS.gray}
          strokeWidth="1.5"
          markerEnd="url(#arrowhead)"
        />

        {/* Arrows to Dashboard Builder */}
        <line
          x1="320" y1="400"
          x2="380" y2="450"
          stroke={COLORS.crimson}
          strokeWidth="2"
          markerEnd="url(#arrowhead)"
        />

        <line
          x1="520" y1="400"
          x2="460" y2="450"
          stroke={COLORS.crimson}
          strokeWidth="2"
          markerEnd="url(#arrowhead)"
        />

        {/* Output */}
        <g transform="translate(600, 450)">
          <rect
            x="0" y="0" width="140" height="80"
            fill="url(#processGradient)"
            stroke={COLORS.terminalGreen}
            strokeWidth="3"
            rx="4"
          />
          <text x="70" y="30" textAnchor="middle" fill={COLORS.charcoal} fontSize="13" fontWeight="700">
            DASHBOARD
          </text>
          <text x="70" y="50" textAnchor="middle" fill={COLORS.gray} fontSize="9">Personalized UI</text>
        </g>

        {/* Final Arrow */}
        <line
          x1="490" y1="490"
          x2="600" y2="490"
          stroke={COLORS.terminalGreen}
          strokeWidth="3"
          markerEnd="url(#arrowhead)"
        />
      </svg>

      {/* Legend */}
      <div className="mt-6 flex justify-center gap-8 text-xs">
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded" style={{ backgroundColor: COLORS.crimson, opacity: 0.3 }} />
          <span style={{ color: COLORS.gray }}>Data Flow</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded" style={{ backgroundColor: COLORS.terminalGreen, opacity: 0.3 }} />
          <span style={{ color: COLORS.gray }}>Processing</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded border" style={{ borderColor: COLORS.charcoal }} />
          <span style={{ color: COLORS.gray }}>Service</span>
        </div>
      </div>
    </div>
  );
};