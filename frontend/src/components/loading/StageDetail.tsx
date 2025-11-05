import { motion } from 'framer-motion';
import type { StageData } from './types';

interface StageDetailProps {
  type: string;
  data?: StageData[keyof StageData];
  status: 'pending' | 'active' | 'complete';
}

export const StageDetail = ({ type, data, status }: StageDetailProps) => {
  if (status === 'pending') {
    return (
      <div className="text-gray-400 text-sm">
        <motion.span
          animate={{ opacity: [0.3, 0.7, 0.3] }}
          transition={{ duration: 2, repeat: Infinity }}
        >
          Queued for processing...
        </motion.span>
      </div>
    );
  }

  if (!data && status === 'active') {
    return (
      <div className="text-sm">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="flex items-center gap-2"
        >
          <motion.div
            className="w-2 h-2 bg-current rounded-full"
            animate={{ scale: [1, 1.2, 1] }}
            transition={{ duration: 1, repeat: Infinity }}
          />
          <span>Initializing...</span>
        </motion.div>
      </div>
    );
  }

  if (!data) return null;

  switch (type) {
    case 'data':
      return <DataStageDetail data={data as StageData['data']} status={status} />;
    case 'patterns':
      return <PersonaStageDetail data={data as StageData['patterns']} status={status} />;
    case 'theme':
      return <ThemeStageDetail data={data as StageData['theme']} status={status} />;
    case 'widgets':
      return <WidgetsStageDetail data={data as StageData['widgets']} status={status} />;
    case 'enrichment':
      return <EnrichmentStageDetail data={data as StageData['enrichment']} status={status} />;
    case 'building':
      return <BuildingStageDetail data={data as StageData['building']} status={status} />;
    default:
      return null;
  }
};

// Sub-components for each stage type
const DataStageDetail = ({ data, status }: { data?: StageData['data']; status: string }) => {
  if (!data) return null;
  return (
    <div className="space-y-3">
      <motion.div
        className="grid grid-cols-2 gap-4"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
      >
        <div
          className="p-3 rounded"
          style={{
            backgroundColor: 'rgba(220, 20, 60, 0.05)',
            border: '1px solid rgba(220, 20, 60, 0.2)'
          }}
        >
          <div className="text-2xl font-bold" style={{ color: 'var(--color-crimson)' }}>
            {data.interactions.toLocaleString()}
          </div>
          <div className="text-xs opacity-70 mt-1">interactions analyzed</div>
        </div>
        <div
          className="p-3 rounded"
          style={{
            backgroundColor: 'rgba(0, 170, 46, 0.05)',
            border: '1px solid rgba(0, 170, 46, 0.2)'
          }}
        >
          <div className="text-2xl font-bold" style={{ color: 'var(--color-terminal-green)' }}>
            {data.platforms.length}
          </div>
          <div className="text-xs opacity-70 mt-1">data sources</div>
        </div>
      </motion.div>

      <motion.div
        className="flex gap-2 flex-wrap"
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
      >
        {data.platforms.map((platform, i) => (
          <motion.span
            key={platform}
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.3 + i * 0.1 }}
            className="px-2 py-1 rounded text-xs"
            style={{
              backgroundColor: 'var(--color-paper)',
              border: '1px solid var(--color-stroke)',
              fontFamily: 'var(--font-family-mono)'
            }}
          >
            {platform}
          </motion.span>
        ))}
      </motion.div>
    </div>
  );
};

const PersonaStageDetail = ({ data, status }: { data?: StageData['patterns']; status: string }) => {
  if (!data) return null;

  const persona = data.persona;
  const patterns = data.patterns;

  // If we have patterns data, show them
  if (patterns && patterns.length > 0) {
    return (
      <div className="space-y-3">
        {/* Patterns detected */}
        <div className="text-xs opacity-60 mb-2">Behavior patterns detected:</div>
        <div className="space-y-2">
          {patterns.slice(0, 5).map((pattern, index) => (
            <motion.div
              key={pattern.title}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 * index }}
              className="p-3 rounded"
              style={{
                background: index === 0
                  ? 'linear-gradient(135deg, rgba(220, 20, 60, 0.08), rgba(220, 20, 60, 0.03))'
                  : 'rgba(0, 170, 46, 0.03)',
                border: `1px solid ${index === 0 ? 'rgba(220, 20, 60, 0.3)' : 'rgba(0, 170, 46, 0.2)'}`,
              }}
            >
              <div className="flex items-start justify-between mb-1">
                <div className="flex items-center gap-2">
                  <span
                    className="text-sm font-semibold"
                    style={{ color: 'var(--color-charcoal)' }}
                  >
                    {pattern.title}
                  </span>
                  {pattern.confidence && (
                    <span
                      className="text-xs px-2 py-0.5 rounded"
                      style={{
                        backgroundColor: pattern.confidence > 0.85
                          ? 'rgba(0, 170, 46, 0.1)'
                          : 'rgba(255, 176, 0, 0.1)',
                        color: pattern.confidence > 0.85
                          ? 'var(--color-terminal-green)'
                          : '#FFB000',
                        border: `1px solid ${pattern.confidence > 0.85
                          ? 'rgba(0, 170, 46, 0.3)'
                          : 'rgba(255, 176, 0, 0.3)'}`,
                        fontFamily: 'var(--font-family-mono)',
                      }}
                    >
                      {Math.round(pattern.confidence * 100)}%
                    </span>
                  )}
                </div>
              </div>
              <p
                className="text-xs leading-relaxed mb-2"
                style={{ color: 'var(--color-gray)' }}
              >
                {pattern.description.length > 120
                  ? `${pattern.description.slice(0, 120)}...`
                  : pattern.description}
              </p>
              {pattern.keywords && pattern.keywords.length > 0 && (
                <div className="flex flex-wrap gap-1">
                  {pattern.keywords.slice(0, 4).map((keyword) => (
                    <span
                      key={keyword}
                      className="text-xs px-1.5 py-0.5 rounded"
                      style={{
                        backgroundColor: 'var(--color-paper)',
                        border: '1px solid var(--color-stroke)',
                        color: 'var(--color-gray)',
                        fontFamily: 'var(--font-family-mono)',
                        fontSize: '10px'
                      }}
                    >
                      {keyword}
                    </span>
                  ))}
                </div>
              )}
            </motion.div>
          ))}
        </div>

        {/* Persona summary if available */}
        {persona && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
            className="mt-3 pt-3"
            style={{ borderTop: '1px solid var(--color-stroke)' }}
          >
            <div className="text-xs opacity-60 mb-2">Overall persona:</div>
            <p
              className="text-xs italic"
              style={{ color: 'var(--color-charcoal)' }}
            >
              {persona.professional_context || persona.writing_style}
            </p>
          </motion.div>
        )}
      </div>
    );
  }

  // Fallback to original persona-only display if no patterns
  if (persona) {
    return (
      <div className="space-y-3">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ type: 'spring', stiffness: 200, damping: 20 }}
          className="p-4 rounded-lg"
          style={{
            background: 'linear-gradient(135deg, rgba(220, 20, 60, 0.05), rgba(0, 170, 46, 0.03))',
            border: '1px solid rgba(220, 20, 60, 0.2)',
          }}
        >
          <div className="mb-2 text-xs uppercase tracking-wider" style={{ color: 'var(--color-crimson)', opacity: 0.8 }}>
            Your Persona:
          </div>
          <p
            className="text-sm leading-relaxed mb-3"
            style={{
              color: 'var(--color-charcoal)',
              fontFamily: 'var(--font-family-serif)',
              fontStyle: 'italic',
              fontSize: '13px'
            }}
          >
            "{persona.professional_context || 'Creative professional'}"
          </p>

          {persona.writing_style && (
            <p
              className="text-xs leading-relaxed"
              style={{
                color: 'var(--color-gray)',
                fontFamily: 'var(--font-family-mono)',
                borderTop: '1px solid rgba(220, 20, 60, 0.1)',
                paddingTop: '8px',
                marginTop: '8px'
              }}
            >
              {persona.writing_style.length > 150
                ? `${persona.writing_style.slice(0, 150)}...`
                : persona.writing_style}
            </p>
          )}
        </motion.div>

        {persona.interests && (
          <div>
            <div className="text-xs opacity-60 mb-2">Key interests identified:</div>
            <div className="grid grid-cols-2 gap-2">
              {persona.interests.slice(0, 6).map((interest, index) => (
                <motion.div
                  key={interest}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.1 * (index + 1) }}
                  className="flex items-center gap-2"
                >
                  <span
                    className="w-1.5 h-1.5 rounded-full"
                    style={{
                      backgroundColor: index % 2 === 0 ? 'var(--color-crimson)' : 'var(--color-terminal-green)',
                      opacity: 0.6
                    }}
                  />
                  <span className="text-xs">{interest}</span>
                </motion.div>
              ))}
            </div>
          </div>
        )}
      </div>
    );
  }

  return null;
};

const ThemeStageDetail = ({ data, status }: { data?: StageData['theme']; status: string }) => {
  if (!data) return null;

  // Generate palette based on the actual theme primary color
  const primaryColor = data.primary || '#FFB000';
  const palette = [
    primaryColor,
    primaryColor + 'CC', // 80% opacity
    primaryColor + '88', // 50% opacity
    primaryColor + '44', // 25% opacity
    primaryColor + '22', // 13% opacity
  ];

  return (
    <div className="space-y-3">
      <div className="flex items-center gap-3">
        <div className="flex -space-x-2">
          {palette.map((color, i) => (
            <motion.div
              key={i}
              initial={{ scale: 0, rotate: -180 }}
              animate={{ scale: 1, rotate: 0 }}
              transition={{ delay: i * 0.05, type: 'spring', stiffness: 300 }}
              className="w-8 h-8 rounded-full border-2"
              style={{
                backgroundColor: color,
                borderColor: '#000000',
                zIndex: palette.length - i,
              }}
            />
          ))}
        </div>
        <div className="flex-1">
          <div className="text-xs opacity-60">Theme mood</div>
          <div className="font-semibold" style={{ color: primaryColor }}>{data.mood}</div>
        </div>
      </div>

      {data.rationale && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="p-3 rounded text-xs"
          style={{
            backgroundColor: `${primaryColor}11`,
            border: `1px solid ${primaryColor}44`,
            color: 'var(--color-gray)'
          }}
        >
          <span style={{ color: primaryColor, opacity: 0.8, fontWeight: 600 }}>Rationale: </span>
          {data.rationale.length > 80
            ? `${data.rationale.slice(0, 80)}...`
            : data.rationale}
        </motion.div>
      )}
    </div>
  );
};

const WidgetsStageDetail = ({ data, status }: { data?: StageData['widgets']; status: string }) => {
  if (!data?.widgets) return null;

  const widgetIcons: Record<string, string> = {
    'Weather': 'W',
    'Map': 'M',
    'Events': 'E',
    'Video': 'V',
    'Ticker': 'T',
    'Todo': 'T',
    'Activity': 'A',
    'Gallery': 'G',
    'Music': 'M',
  };

  return (
    <div className="space-y-3">
      <div className="text-xs opacity-60">Selected components:</div>
      <div className="grid grid-cols-3 gap-2">
        {data.widgets.map((widget, index) => {
          const icon = Object.entries(widgetIcons).find(([key]) =>
            widget.toLowerCase().includes(key.toLowerCase())
          )?.[1] || '🧩';

          return (
            <motion.div
              key={widget}
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{
                delay: 0.05 * index,
                type: 'spring',
                stiffness: 300,
                damping: 20
              }}
              className="p-2 rounded text-center"
              style={{
                backgroundColor: status === 'active'
                  ? 'rgba(220, 20, 60, 0.05)'
                  : 'rgba(0, 170, 46, 0.05)',
                border: `1px solid ${status === 'active'
                  ? 'rgba(220, 20, 60, 0.2)'
                  : 'rgba(0, 170, 46, 0.2)'}`
              }}
            >
              <div className="text-lg mb-1">{icon}</div>
              <div className="text-xs truncate">{widget}</div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
};

const EnrichmentStageDetail = ({ data, status }: { data?: StageData['enrichment']; status: string }) => {
  if (!data?.apis) return null;

  return (
    <div className="space-y-2">
      <div className="text-xs opacity-60">Live data sources:</div>
      {data.apis.map((api, index) => (
        <motion.div
          key={api}
          initial={{ opacity: 0, x: -10 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: index * 0.1 }}
          className="flex items-center gap-2"
        >
          <motion.div
            className="w-1.5 h-1.5 rounded-full"
            style={{ backgroundColor: 'var(--color-terminal-green)' }}
            animate={status === 'active' ? {
              scale: [1, 1.5, 1],
              opacity: [1, 0.5, 1]
            } : {}}
            transition={{ duration: 1, repeat: Infinity, delay: index * 0.2 }}
          />
          <span className="text-xs font-mono">
            {status === 'active' ? 'Fetching' : 'Connected'}: {api}
          </span>
        </motion.div>
      ))}
      {status === 'complete' && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="mt-2 text-xs"
          style={{ color: 'var(--color-terminal-green)' }}
        >
          All APIs responded successfully
        </motion.div>
      )}
    </div>
  );
};

const BuildingStageDetail = ({ data, status }: { data?: StageData['building']; status: string }) => {
  if (!data) return null;

  return (
    <div className="space-y-3">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="grid grid-cols-2 gap-3"
      >
        <div className="text-center p-3 rounded"
          style={{
            backgroundColor: 'rgba(220, 20, 60, 0.05)',
            border: '1px solid rgba(220, 20, 60, 0.2)'
          }}
        >
          <motion.div
            className="text-2xl font-bold"
            style={{ color: 'var(--color-crimson)' }}
            animate={status === 'active' ? {
              scale: [1, 1.1, 1]
            } : {}}
            transition={{ duration: 0.5 }}
          >
            {data.cardCount}
          </motion.div>
          <div className="text-xs opacity-70 mt-1">content cards</div>
        </div>
        <div className="text-center p-3 rounded"
          style={{
            backgroundColor: 'rgba(0, 170, 46, 0.05)',
            border: '1px solid rgba(0, 170, 46, 0.2)'
          }}
        >
          <motion.div
            className="text-2xl font-bold"
            style={{ color: 'var(--color-terminal-green)' }}
            animate={status === 'active' ? {
              scale: [1, 1.1, 1]
            } : {}}
            transition={{ duration: 0.5, delay: 0.1 }}
          >
            {data.widgetCount}
          </motion.div>
          <div className="text-xs opacity-70 mt-1">UI components</div>
        </div>
      </motion.div>

      {status === 'active' && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-xs text-center"
          style={{ color: 'var(--color-gray)' }}
        >
          <motion.span
            animate={{ opacity: [0.5, 1, 0.5] }}
            transition={{ duration: 1.5, repeat: Infinity }}
          >
            Assembling personalized layout...
          </motion.span>
        </motion.div>
      )}
    </div>
  );
};
