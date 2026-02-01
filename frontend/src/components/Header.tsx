import { Video, Github } from 'lucide-react'

export function Header() {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 glass">
      <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
        <a href="/" className="flex items-center gap-2 group">
          <div className="relative">
            <Video className="w-8 h-8 text-primary-500 group-hover:text-primary-400 transition-colors" />
            <div className="absolute -inset-1 bg-primary-500/20 rounded-full blur-md opacity-0 group-hover:opacity-100 transition-opacity" />
          </div>
          <span className="text-xl font-bold gradient-text">GitVideo</span>
        </a>
        
        <nav className="flex items-center gap-6">
          <a 
            href="#generator" 
            className="text-dark-300 hover:text-white transition-colors font-medium"
          >
            Generate
          </a>
          <a 
            href="#features" 
            className="text-dark-300 hover:text-white transition-colors font-medium"
          >
            Features
          </a>
          <a
            href="https://github.com/harshit-wadhwani/GitVideo"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-dark-700 hover:bg-dark-600 transition-colors"
          >
            <Github className="w-5 h-5" />
            <span className="hidden sm:inline">GitHub</span>
          </a>
        </nav>
      </div>
    </header>
  )
}
