/**
 * TaskCard Widget (TaskList)
 *
 * Displays a to-do list with checkable tasks.
 * Clean, minimalist design for task tracking.
 */

import { motion } from 'framer-motion';
import { CheckSquare, Square, ListTodo } from 'lucide-react';
import { useState } from 'react';
import { registerWidget } from './WidgetRegistry';
import type { WidgetProps } from './WidgetTypes';

interface TaskItem {
  text: string;
  completed: boolean;
  priority: 'low' | 'medium' | 'high';
}

interface TaskCardData {
  title: string;
  tasks: TaskItem[];
}

function TaskCard({ id, data, size }: WidgetProps) {
  const taskData = data as TaskCardData;
  const { title, tasks } = taskData;

  // Track completed state for each task, initialized from backend data
  const [completedTasks, setCompletedTasks] = useState<Set<number>>(
    new Set(tasks.map((task, idx) => task.completed ? idx : -1).filter(idx => idx !== -1))
  );

  const toggleTask = (index: number) => {
    setCompletedTasks((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(index)) {
        newSet.delete(index);
      } else {
        newSet.add(index);
      }
      return newSet;
    });
  };

  const completedCount = completedTasks.size;
  const totalCount = tasks.length;
  const progress = totalCount > 0 ? (completedCount / totalCount) * 100 : 0;

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
      className="h-full"
    >
      <div className="card-background rounded-lg p-6 h-full flex flex-col shadow-lg border border-border/50">
        {/* Header */}
        <div className="mb-4">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-lg font-bold text-foreground flex items-center gap-2">
              <ListTodo className="w-5 h-5 text-primary" />
              {title}
            </h3>
            <span className="text-xs text-muted px-2 py-1 rounded-full bg-primary/10">
              {completedCount}/{totalCount}
            </span>
          </div>

          {/* Progress Bar */}
          <div className="h-2 bg-muted/20 rounded-full overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              transition={{ duration: 0.5, ease: 'easeOut' }}
              className="h-full bg-gradient-to-r from-primary to-secondary"
            />
          </div>
        </div>

        {/* Task List */}
        <div className="flex-1 space-y-2">
          {tasks.map((task, index) => {
            const isCompleted = completedTasks.has(index);

            return (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.1 * (index + 1) }}
                whileHover={{ scale: 1.02 }}
                className="group"
              >
                <button
                  onClick={() => toggleTask(index)}
                  className="w-full flex items-start gap-3 p-3 rounded-lg hover:bg-muted/20 transition-colors text-left"
                >
                  {/* Checkbox */}
                  <div className="flex-shrink-0 mt-0.5">
                    {isCompleted ? (
                      <CheckSquare className="w-5 h-5 text-success" />
                    ) : (
                      <Square className="w-5 h-5 text-muted group-hover:text-primary transition-colors" />
                    )}
                  </div>

                  {/* Task Text */}
                  <span
                    className={`text-xs flex-1 transition-all line-clamp-2 ${
                      isCompleted
                        ? 'text-muted line-through opacity-60'
                        : 'text-foreground'
                    }`}
                  >
                    {task.text}
                  </span>
                </button>
              </motion.div>
            );
          })}

          {/* Empty State */}
          {tasks.length === 0 && (
            <div className="flex flex-col items-center justify-center py-8 text-center">
              <ListTodo className="w-12 h-12 text-muted mb-3 opacity-30" />
              <p className="text-sm text-muted">No tasks yet</p>
              <p className="text-xs text-muted-foreground mt-1">
                Add tasks to get started
              </p>
            </div>
          )}
        </div>

        {/* Footer Summary */}
        {tasks.length > 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
            className="mt-4 pt-4 border-t border-border/30"
          >
            {completedCount === totalCount ? (
              <p className="text-xs text-success flex items-center gap-1">
                <CheckSquare className="w-3 h-3" />
                All tasks completed! 🎉
              </p>
            ) : (
              <p className="text-xs text-muted">
                {totalCount - completedCount} {totalCount - completedCount === 1 ? 'task' : 'tasks'} remaining
              </p>
            )}
          </motion.div>
        )}
      </div>
    </motion.div>
  );
}

// Register this widget type as "task-card" (matches backend)
registerWidget('task-card', TaskCard);

export default TaskCard;
