import { Video, Github, Linkedin, Heart } from 'lucide-react'

export function Footer() {
  return (
    <footer className="border-t border-dark-800 py-12 px-4">
      <div className="max-w-6xl mx-auto">
        <div className="grid md:grid-cols-3 gap-8 mb-8">
          {/* Brand */}
          <div className="md:col-span-2">
            <div className="flex items-center gap-2 mb-4">
              <Video className="w-8 h-8 text-primary-500" />
              <span className="text-xl font-bold gradient-text">GitVideo</span>
            </div>
            <p className="text-dark-400 max-w-sm">
              Transform any GitHub repository into a stunning showcase video using the power of AI.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="font-semibold mb-4">Quick Links</h4>
            <ul className="space-y-2 text-dark-400">
              <li><a href="#generator" className="hover:text-white transition-colors">Generate Video</a></li>
              <li><a href="#features" className="hover:text-white transition-colors">Features</a></li>
              <li><a href="https://github.com/harshit-wadhwani/GitVideo" className="hover:text-white transition-colors">GitHub</a></li>
            </ul>
          </div>
        </div>

        {/* Bottom */}
        <div className="flex flex-col sm:flex-row items-center justify-between pt-8 border-t border-dark-800">
          <p className="text-dark-500 text-sm flex items-center gap-1">
            Made with <Heart className="w-4 h-4 text-red-500 fill-red-500" /> by{' '}
            <a 
              href="https://www.harshitwadhwani.dev" 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-primary-400 hover:text-primary-300 transition-colors"
            >
              Harshit Wadhwani
            </a>
          </p>
          <div className="flex items-center gap-4 mt-4 sm:mt-0">
            <a
              href="https://github.com/harshit-wadhwani"
              target="_blank"
              rel="noopener noreferrer"
              className="text-dark-400 hover:text-white transition-colors"
            >
              <Github className="w-5 h-5" />
            </a>
            <a
              href="https://www.linkedin.com/in/harshitwadhwani/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-dark-400 hover:text-white transition-colors"
            >
              <Linkedin className="w-5 h-5" />
            </a>
          </div>
        </div>
      </div>
    </footer>
  )
}
