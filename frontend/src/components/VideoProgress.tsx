import { useEffect, useRef } from 'react'
import { 
  Loader2, 
  CheckCircle2, 
  XCircle, 
  GitBranch, 
  Sparkles, 
  Video,
  X
} from 'lucide-react'
import { getVideoStatus } from '../api'
import { VideoStatus } from '../types'

interface VideoProgressProps {
  jobId: string
  status: VideoStatus
  onStatusUpdate: (status: VideoStatus) => void
  onCancel: () => void
}

const POLL_INTERVAL = 2000 // 2 seconds

export function VideoProgress({ jobId, status, onStatusUpdate, onCancel }: VideoProgressProps) {
  const intervalRef = useRef<number | null>(null)

  useEffect(() => {
    const pollStatus = async () => {
      try {
        const newStatus = await getVideoStatus(jobId)
        onStatusUpdate(newStatus)
        
        // Stop polling if completed or failed
        if (newStatus.status === 'completed' || newStatus.status === 'failed') {
          if (intervalRef.current) {
            clearInterval(intervalRef.current)
          }
        }
      } catch (error) {
        console.error('Error polling status:', error)
      }
    }

    // Start polling
    intervalRef.current = window.setInterval(pollStatus, POLL_INTERVAL)

    // Cleanup
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current)
      }
    }
  }, [jobId, onStatusUpdate])

  const getStatusIcon = () => {
    switch (status.status) {
      case 'pending':
        return <Loader2 className="w-16 h-16 text-primary-400 animate-spin" />
      case 'processing':
        return (
          <div className="relative">
            <div className="absolute inset-0 bg-primary-500/20 rounded-full pulse-ring" />
            <Sparkles className="w-16 h-16 text-primary-400 animate-pulse" />
          </div>
        )
      case 'completed':
        return <CheckCircle2 className="w-16 h-16 text-green-400" />
      case 'failed':
        return <XCircle className="w-16 h-16 text-red-400" />
      default:
        return <Video className="w-16 h-16 text-dark-400" />
    }
  }

  const getProgressSteps = () => {
    const steps = [
      { label: 'Analyzing Repository', icon: GitBranch, threshold: 10 },
      { label: 'Creating Script', icon: Sparkles, threshold: 40 },
      { label: 'Generating Video', icon: Video, threshold: 60 },
      { label: 'Finalizing', icon: CheckCircle2, threshold: 90 },
    ]

    return steps.map((step) => ({
      ...step,
      completed: status.progress >= step.threshold,
      active: status.progress >= step.threshold - 30 && status.progress < step.threshold + 10,
    }))
  }

  return (
    <div className="glass rounded-2xl p-8 glow fade-in">
      {/* Cancel button */}
      <button
        onClick={onCancel}
        className="absolute top-4 right-4 p-2 rounded-lg hover:bg-dark-700 transition-colors text-dark-400 hover:text-white"
      >
        <X className="w-5 h-5" />
      </button>

      <div className="text-center mb-8">
        <div className="flex justify-center mb-6">
          {getStatusIcon()}
        </div>
        <h2 className="text-2xl font-bold mb-2">
          {status.status === 'failed' ? 'Generation Failed' : 'Generating Your Video'}
        </h2>
        <p className="text-dark-400">{status.message}</p>
      </div>

      {/* Progress bar */}
      <div className="mb-8">
        <div className="flex justify-between text-sm mb-2">
          <span className="text-dark-400">Progress</span>
          <span className="font-medium text-primary-400">{status.progress}%</span>
        </div>
        <div className="h-3 bg-dark-700 rounded-full overflow-hidden">
          <div
            className="h-full progress-bar rounded-full transition-all duration-500 ease-out"
            style={{ width: `${status.progress}%` }}
          />
        </div>
      </div>

      {/* Steps */}
      <div className="space-y-4">
        {getProgressSteps().map((step, index) => (
          <div
            key={step.label}
            className={`flex items-center gap-4 p-4 rounded-xl transition-all ${
              step.active
                ? 'bg-primary-500/10 border border-primary-500/20'
                : step.completed
                ? 'bg-dark-800'
                : 'bg-dark-800/50 opacity-50'
            }`}
          >
            <div
              className={`p-2 rounded-lg ${
                step.completed ? 'bg-green-500/20' : step.active ? 'bg-primary-500/20' : 'bg-dark-700'
              }`}
            >
              <step.icon
                className={`w-5 h-5 ${
                  step.completed
                    ? 'text-green-400'
                    : step.active
                    ? 'text-primary-400 animate-pulse'
                    : 'text-dark-500'
                }`}
              />
            </div>
            <div className="flex-1">
              <div className="font-medium">{step.label}</div>
              <div className="text-sm text-dark-500">Step {index + 1} of 4</div>
            </div>
            {step.completed && (
              <CheckCircle2 className="w-5 h-5 text-green-400" />
            )}
            {step.active && !step.completed && (
              <Loader2 className="w-5 h-5 text-primary-400 animate-spin" />
            )}
          </div>
        ))}
      </div>

      {/* Job ID */}
      <div className="mt-8 pt-6 border-t border-dark-700 text-center">
        <p className="text-xs text-dark-500">
          Job ID: <code className="text-dark-400">{jobId}</code>
        </p>
      </div>
    </div>
  )
}
