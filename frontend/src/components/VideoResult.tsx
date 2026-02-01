import { 
  Download, 
  Share2, 
  RefreshCw, 
  CheckCircle2,
  Play,
  Twitter,
  Linkedin
} from 'lucide-react'

interface VideoResultProps {
  videoUrl: string
  onGenerateAnother: () => void
}

export function VideoResult({ videoUrl, onGenerateAnother }: VideoResultProps) {
  const handleDownload = () => {
    const link = document.createElement('a')
    link.href = videoUrl
    link.download = 'gitvideo-output.mp4'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  const handleShare = (platform: 'twitter' | 'linkedin') => {
    const text = "Check out this video I generated for my GitHub repository using GitVideo! 🎬"
    const url = encodeURIComponent(window.location.href)
    
    const shareUrls = {
      twitter: `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${url}`,
      linkedin: `https://www.linkedin.com/sharing/share-offsite/?url=${url}`,
    }
    
    window.open(shareUrls[platform], '_blank', 'width=600,height=400')
  }

  return (
    <div className="glass rounded-2xl p-8 glow fade-in">
      {/* Success header */}
      <div className="text-center mb-8">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-green-500/20 mb-4">
          <CheckCircle2 className="w-8 h-8 text-green-400" />
        </div>
        <h2 className="text-3xl font-bold mb-2">Video Generated!</h2>
        <p className="text-dark-400">Your repository video is ready</p>
      </div>

      {/* Video player */}
      <div className="relative rounded-xl overflow-hidden bg-dark-800 mb-8 group">
        <video
          src={videoUrl}
          controls
          className="w-full aspect-video"
          poster="/video-poster.png"
        >
          Your browser does not support the video tag.
        </video>
        
        {/* Play overlay */}
        <div className="absolute inset-0 flex items-center justify-center bg-black/30 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none">
          <div className="p-4 rounded-full bg-white/20 backdrop-blur-sm">
            <Play className="w-8 h-8 text-white fill-white" />
          </div>
        </div>
      </div>

      {/* Actions */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        <button
          onClick={handleDownload}
          className="flex items-center justify-center gap-2 py-3 px-6 rounded-xl bg-primary-500 hover:bg-primary-600 transition-colors font-medium"
        >
          <Download className="w-5 h-5" />
          Download Video
        </button>
        <button
          onClick={onGenerateAnother}
          className="flex items-center justify-center gap-2 py-3 px-6 rounded-xl bg-dark-700 hover:bg-dark-600 transition-colors font-medium"
        >
          <RefreshCw className="w-5 h-5" />
          Generate Another
        </button>
      </div>

      {/* Share */}
      <div className="border-t border-dark-700 pt-6">
        <p className="text-center text-dark-400 mb-4">
          <Share2 className="inline w-4 h-4 mr-2" />
          Share your video
        </p>
        <div className="flex justify-center gap-4">
          <button
            onClick={() => handleShare('twitter')}
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-[#1DA1F2]/20 text-[#1DA1F2] hover:bg-[#1DA1F2]/30 transition-colors"
          >
            <Twitter className="w-5 h-5" />
            Twitter
          </button>
          <button
            onClick={() => handleShare('linkedin')}
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-[#0A66C2]/20 text-[#0A66C2] hover:bg-[#0A66C2]/30 transition-colors"
          >
            <Linkedin className="w-5 h-5" />
            LinkedIn
          </button>
        </div>
      </div>
    </div>
  )
}
