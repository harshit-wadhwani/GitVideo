import { Play, Sparkles, GitBranch } from 'lucide-react'

export function Hero() {
  return (
    <section className="relative pt-32 pb-20 px-4 overflow-hidden">
      {/* Background effects */}
      <div className="absolute inset-0 bg-gradient-radial from-primary-500/10 via-transparent to-transparent" />
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary-500/20 rounded-full blur-3xl" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl" />
      
      <div className="relative max-w-5xl mx-auto text-center">
        {/* Badge */}
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass mb-8 fade-in">
          <Sparkles className="w-4 h-4 text-yellow-400" />
          <span className="text-sm font-medium">Powered by OpenAI Sora</span>
        </div>
        
        {/* Main headline */}
        <h1 className="text-5xl md:text-7xl font-extrabold mb-6 fade-in" style={{ animationDelay: '0.1s' }}>
          Turn Any{' '}
          <span className="gradient-text">GitHub Repo</span>
          <br />
          Into a{' '}
          <span className="relative inline-block">
            <span className="gradient-text">Stunning Video</span>
            <Play className="absolute -right-8 -top-4 w-8 h-8 text-primary-400 animate-float" />
          </span>
        </h1>
        
        {/* Subtitle */}
        <p className="text-xl md:text-2xl text-dark-300 max-w-3xl mx-auto mb-12 fade-in" style={{ animationDelay: '0.2s' }}>
          Generate beautiful, AI-powered showcase videos for your open source projects.
          Just paste a repository URL and let the magic happen.
        </p>
        
        {/* CTA */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 fade-in" style={{ animationDelay: '0.3s' }}>
          <a
            href="#generator"
            className="group flex items-center gap-2 px-8 py-4 rounded-xl gradient-bg font-semibold text-lg btn-glow transition-all hover:scale-105"
          >
            <GitBranch className="w-5 h-5" />
            Generate Video
            <span className="group-hover:translate-x-1 transition-transform">→</span>
          </a>
          <a
            href="#features"
            className="flex items-center gap-2 px-8 py-4 rounded-xl glass font-semibold text-lg hover:bg-dark-700/50 transition-colors"
          >
            Learn More
          </a>
        </div>
        
        {/* Stats */}
        <div className="grid grid-cols-2 gap-8 max-w-lg mx-auto mt-20 fade-in" style={{ animationDelay: '0.4s' }}>
          <div className="text-center">
            <div className="text-3xl font-bold gradient-text">AI-Powered</div>
            <div className="text-dark-400 mt-1">Video Generation</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold gradient-text">5 Styles</div>
            <div className="text-dark-400 mt-1">Visual Options</div>
          </div>
        </div>
      </div>
    </section>
  )
}
