import { motion, AnimatePresence } from 'framer-motion';
import { PipelineStage } from './PipelineStage';
import type { LoadingState, PipelineStageConfig } from './types';

interface LoadingOverlayProps {
  show: boolean;
  progress: LoadingState;
}

const PIPELINE_STAGES: PipelineStageConfig[] = [
  {
    id: 'data',
    title: 'Data Fetch',
    icon: '📊',
    websocketStep: ['data', 'initializing'],
  },
  {
    id: 'patterns',
    title: 'Persona Detection',
    icon: '🧠',
    websocketStep: ['patterns', 'patterns_complete'],
  },
  {
    id: 'theme',
    title: 'Theme Generation',
    icon: '🎨',
    websocketStep: ['theme', 'theme_complete'],
  },
  {
    id: 'widgets',
    title: 'Component Selection',
    icon: '🧩',
    websocketStep: ['widgets', 'widgets_complete'],
  },
  {
    id: 'enrichment',
    title: 'API Enrichment',
    icon: '🔍',
    websocketStep: ['search', 'enriching', 'content'],
  },
  {
    id: 'building',
    title: 'Dashboard Assembly',
    icon: '🏗️',
    websocketStep: ['building'],
  },
];

export const LoadingOverlay = ({ show, progress }: LoadingOverlayProps) => {
  return (
    <AnimatePresence>
      {show && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black/95 z-50 overflow-y-auto"
        >
          <div className="min-h-screen flex flex-col items-center justify-start py-8 px-4">
            {/* Header */}
            <motion.div
              initial={{ y: -20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              className="text-center mb-8 w-full max-w-2xl"
            >
              <h1 className="text-3xl font-bold text-white mb-4">
                Generating Your Dashboard
              </h1>

              {/* Progress Bar */}
              <div className="w-full bg-gray-800 rounded-full h-3 overflow-hidden mb-2">
                <motion.div
                  className="h-full bg-blue-500"
                  initial={{ width: 0 }}
                  animate={{ width: `${progress.percent}%` }}
                  transition={{ duration: 0.3, ease: 'easeOut' }}
                />
              </div>

              {/* Current Step Message */}
              <p className="text-gray-400 text-sm">
                {progress.message || 'Starting...'}
              </p>
            </motion.div>

            {/* Pipeline Stages */}
            <div className="w-full max-w-2xl space-y-4">
              {PIPELINE_STAGES.map((stage, index) => (
                <>
                  <PipelineStage
                    key={stage.id}
                    id={stage.id}
                    title={stage.title}
                    icon={stage.icon}
                    status={progress.stageStatuses[stage.id as keyof typeof progress.stageStatuses]}
                    data={progress.stageData[stage.id as keyof typeof progress.stageData]}
                    index={index}
                  />

                  {/* Arrow connector (except after last stage) */}
                  {index < PIPELINE_STAGES.length - 1 && (
                    <div key={`arrow-${stage.id}`} className="flex justify-center">
                      <div className="w-0.5 h-6 bg-gray-700" />
                    </div>
                  )}
                </>
              ))}
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};
