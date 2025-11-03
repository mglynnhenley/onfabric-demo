import { motion } from 'framer-motion';
import { Check } from 'lucide-react';
import { StageDetail } from './StageDetail';
import type { StageStatus, StageData } from './types';

interface PipelineStageProps {
  id: string;
  title: string;
  icon: string;
  status: StageStatus;
  data?: StageData[keyof StageData];
  index: number;
}

export const PipelineStage = ({
  id,
  title,
  icon,
  status,
  data,
  index,
}: PipelineStageProps) => {
  const getStatusStyles = () => {
    switch (status) {
      case 'active':
        return 'border-blue-500 bg-blue-950/30 shadow-lg shadow-blue-500/20';
      case 'complete':
        return 'border-green-600 bg-gray-800';
      case 'pending':
      default:
        return 'border-gray-700 bg-gray-900 opacity-40';
    }
  };

  const getStatusIndicator = () => {
    switch (status) {
      case 'active':
        return (
          <motion.div
            className="w-3 h-3 bg-blue-500 rounded-full"
            animate={{ scale: [1, 1.2, 1] }}
            transition={{ repeat: Infinity, duration: 2 }}
          />
        );
      case 'complete':
        return (
          <motion.div
            initial={{ scale: 0.8 }}
            animate={{ scale: 1 }}
            className="text-green-500"
          >
            <Check size={16} />
          </motion.div>
        );
      case 'pending':
      default:
        return <div className="w-3 h-3 border-2 border-gray-600 rounded-full" />;
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1, duration: 0.4 }}
      className={`border-2 rounded-lg p-4 transition-all duration-300 ${getStatusStyles()}`}
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-3">
          <span className="text-2xl">{icon}</span>
          <h3 className="font-semibold text-white">{title}</h3>
        </div>
        <div className="flex items-center gap-2">
          {getStatusIndicator()}
        </div>
      </div>

      {/* Detail Content */}
      <div className="mt-3 text-gray-300">
        <StageDetail type={id} data={data} status={status} />
      </div>
    </motion.div>
  );
};
