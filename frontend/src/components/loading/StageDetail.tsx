import type { StageData } from './types';

interface StageDetailProps {
  type: string;
  data?: StageData[keyof StageData];
  status: 'pending' | 'active' | 'complete';
}

export const StageDetail = ({ type, data, status }: StageDetailProps) => {
  if (status === 'pending') {
    return <div className="text-gray-400 text-sm">Waiting...</div>;
  }

  if (!data) return null;

  switch (type) {
    case 'data':
      return <DataStageDetail data={data as StageData['data']} />;
    case 'patterns':
      return <PersonaStageDetail data={data as StageData['patterns']} />;
    case 'theme':
      return <ThemeStageDetail data={data as StageData['theme']} />;
    case 'widgets':
      return <WidgetsStageDetail data={data as StageData['widgets']} />;
    case 'enrichment':
      return <EnrichmentStageDetail data={data as StageData['enrichment']} />;
    case 'building':
      return <BuildingStageDetail data={data as StageData['building']} />;
    default:
      return null;
  }
};

// Sub-components for each stage type
const DataStageDetail = ({ data }: { data?: StageData['data'] }) => {
  if (!data) return null;
  return (
    <div className="text-sm space-y-1">
      <div>• {data.interactions} interactions loaded</div>
      <div>• Platforms: {data.platforms.join(', ')}</div>
    </div>
  );
};

const PersonaStageDetail = ({ data }: { data?: StageData['patterns'] }) => {
  if (!data?.persona) return null;
  const persona = data.persona;

  return (
    <div className="text-sm space-y-2">
      <p className="italic text-gray-300">
        {persona.professional_context || persona.writing_style}
      </p>
      <div className="space-y-1">
        {persona.interests.slice(0, 4).map((interest, idx) => (
          <div key={idx}>• {interest}</div>
        ))}
      </div>
    </div>
  );
};

const ThemeStageDetail = ({ data }: { data?: StageData['theme'] }) => {
  if (!data) return null;
  return (
    <div className="text-sm space-y-1">
      <div className="flex items-center gap-2">
        <div
          className="w-4 h-4 rounded border border-gray-600"
          style={{ backgroundColor: data.primary }}
        />
        <span>Primary: {data.primary}</span>
      </div>
      <div>• Mood: {data.mood}</div>
      {data.rationale && (
        <div className="text-xs text-gray-400 italic">
          {data.rationale.slice(0, 100)}...
        </div>
      )}
    </div>
  );
};

const WidgetsStageDetail = ({ data }: { data?: StageData['widgets'] }) => {
  if (!data?.widgets) return null;
  return (
    <div className="text-sm space-y-1">
      {data.widgets.map((widget, idx) => (
        <div key={idx}>• {widget}</div>
      ))}
    </div>
  );
};

const EnrichmentStageDetail = ({ data }: { data?: StageData['enrichment'] }) => {
  if (!data?.apis) return null;
  return (
    <div className="text-sm space-y-1">
      {data.apis.map((api, idx) => (
        <div key={idx}>• Calling {api}...</div>
      ))}
    </div>
  );
};

const BuildingStageDetail = ({ data }: { data?: StageData['building'] }) => {
  if (!data) return null;
  return (
    <div className="text-sm space-y-1">
      <div>• {data.cardCount} content cards</div>
      <div>• {data.widgetCount} widgets</div>
    </div>
  );
};
