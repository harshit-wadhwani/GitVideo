import { useState } from 'react'
import { 
  Github, 
  Key, 
  Palette, 
  Clock, 
  Loader2, 
  AlertCircle,
  Eye,
  EyeOff
} from 'lucide-react'
import { generateVideo } from '../api'
import { VideoStyle } from '../types'

interface VideoFormProps {
  onGenerationStart: (jobId: string) => void
}

const VIDEO_STYLES: { value: VideoStyle; label: string; description: string }[] = [
  { value: 'tech', label: 'Tech', description: 'Futuristic, neon accents, holographic displays' },
  { value: 'cinematic', label: 'Cinematic', description: 'Wide shots, dramatic lighting, film grain' },
  { value: 'minimal', label: 'Minimal', description: 'Clean, white space, subtle animations' },
  { value: 'dynamic', label: 'Dynamic', description: 'Fast-paced, energetic, vibrant colors' },
  { value: 'documentary', label: 'Documentary', description: 'Authentic, informative, professional' },
]

export function VideoForm({ onGenerationStart }: VideoFormProps) {
  const [repoUrl, setRepoUrl] = useState('')
  const [apiKey, setApiKey] = useState('')
  const [showApiKey, setShowApiKey] = useState(false)
  const [style, setStyle] = useState<VideoStyle>('tech')
  const [duration, setDuration] = useState(8)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setIsLoading(true)

    try {
      // Validate GitHub URL
      if (!repoUrl.includes('github.com')) {
        throw new Error('Please enter a valid GitHub repository URL')
      }

      // Validate API key format
      if (!apiKey.startsWith('sk-')) {
        throw new Error('Please enter a valid OpenAI API key')
      }

      const response = await generateVideo({
        repo_url: repoUrl,
        openai_api_key: apiKey,
        video_style: style,
        duration
      })

      onGenerationStart(response.job_id)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="glass rounded-2xl p-8 glow fade-in">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold mb-2">Generate Your Video</h2>
        <p className="text-dark-400">Enter your repository and API key to get started</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Repository URL */}
        <div>
          <label className="block text-sm font-medium mb-2 text-dark-200">
            GitHub Repository URL
          </label>
          <div className="relative">
            <Github className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-dark-400" />
            <input
              type="url"
              value={repoUrl}
              onChange={(e) => setRepoUrl(e.target.value)}
              placeholder="https://github.com/username/repository"
              required
              className="w-full pl-12 pr-4 py-3 rounded-xl bg-dark-800 border border-dark-600 text-white placeholder-dark-400 focus:border-primary-500 transition-colors"
            />
          </div>
        </div>

        {/* API Key */}
        <div>
          <label className="block text-sm font-medium mb-2 text-dark-200">
            OpenAI API Key
          </label>
          <div className="relative">
            <Key className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-dark-400" />
            <input
              type={showApiKey ? 'text' : 'password'}
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="sk-..."
              required
              className="w-full pl-12 pr-12 py-3 rounded-xl bg-dark-800 border border-dark-600 text-white placeholder-dark-400 focus:border-primary-500 transition-colors"
            />
            <button
              type="button"
              onClick={() => setShowApiKey(!showApiKey)}
              className="absolute right-4 top-1/2 -translate-y-1/2 text-dark-400 hover:text-dark-200 transition-colors"
            >
              {showApiKey ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
            </button>
          </div>
          <p className="text-xs text-dark-500 mt-2">
            Your API key is never stored and is only used for this generation request.
          </p>
        </div>

        {/* Video Style */}
        <div>
          <label className="block text-sm font-medium mb-2 text-dark-200">
            <Palette className="inline w-4 h-4 mr-1" />
            Video Style
          </label>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3">
            {VIDEO_STYLES.map((s) => (
              <button
                key={s.value}
                type="button"
                onClick={() => setStyle(s.value)}
                className={`p-3 rounded-xl border text-center transition-all ${
                  style === s.value
                    ? 'border-primary-500 bg-primary-500/20 text-primary-400'
                    : 'border-dark-600 bg-dark-800 hover:border-dark-500'
                }`}
              >
                <div className="font-medium">{s.label}</div>
                <div className="text-xs text-dark-400 mt-1 hidden sm:block">{s.description.split(',')[0]}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Duration */}
        <div>
          <label className="block text-sm font-medium mb-2 text-dark-200">
            <Clock className="inline w-4 h-4 mr-1" />
            Duration: {duration} seconds
          </label>
          <div className="grid grid-cols-3 gap-3">
            {[4, 8, 12].map((d) => (
              <button
                key={d}
                type="button"
                onClick={() => setDuration(d)}
                className={`py-3 rounded-xl border text-center transition-all ${
                  duration === d
                    ? 'border-primary-500 bg-primary-500/20 text-primary-400'
                    : 'border-dark-600 bg-dark-800 hover:border-dark-500'
                }`}
              >
                {d} sec
              </button>
            ))}
          </div>
          <p className="text-xs text-dark-500 mt-2">
            Sora supports video clips of 4, 8, or 12 seconds.
          </p>
        </div>

        {/* Error */}
        {error && (
          <div className="flex items-center gap-2 p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400">
            <AlertCircle className="w-5 h-5 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {/* Submit */}
        <button
          type="submit"
          disabled={isLoading}
          className="w-full py-4 rounded-xl gradient-bg font-semibold text-lg btn-glow transition-all hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 flex items-center justify-center gap-2"
        >
          {isLoading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Starting Generation...
            </>
          ) : (
            <>
              Generate Video
              <span>→</span>
            </>
          )}
        </button>
      </form>
    </div>
  )
}
