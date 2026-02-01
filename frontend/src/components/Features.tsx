import { 
  Zap, 
  Palette, 
  Shield, 
  GitBranch, 
  Sparkles, 
  Clock 
} from 'lucide-react'

const FEATURES = [
  {
    icon: Zap,
    title: 'AI-Powered Generation',
    description: 'Leverages OpenAI Sora to create stunning, professional-quality videos from your code.',
    gradient: 'from-yellow-400 to-orange-500',
  },
  {
    icon: GitBranch,
    title: 'Repository Analysis',
    description: 'Automatically analyzes your repo structure, README, and codebase to understand your project.',
    gradient: 'from-green-400 to-emerald-500',
  },
  {
    icon: Palette,
    title: 'Multiple Styles',
    description: 'Choose from 5 unique visual styles including Tech, Cinematic, Minimal, Dynamic, and Documentary.',
    gradient: 'from-purple-400 to-pink-500',
  },
  {
    icon: Shield,
    title: 'Secure & Private',
    description: 'Your API key is never stored. All processing happens in real-time and data is immediately discarded.',
    gradient: 'from-blue-400 to-cyan-500',
  },
  {
    icon: Sparkles,
    title: 'Smart Script Writing',
    description: 'GPT-4o creates a tailored video script based on your project\'s unique features and purpose.',
    gradient: 'from-pink-400 to-rose-500',
  },
  {
    icon: Clock,
    title: 'Fast Processing',
    description: 'Get your video in minutes, not hours. Background processing keeps you informed of progress.',
    gradient: 'from-indigo-400 to-violet-500',
  },
]

export function Features() {
  return (
    <section id="features" className="py-20 px-4 bg-dark-950/50">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            Why <span className="gradient-text">GitVideo</span>?
          </h2>
          <p className="text-xl text-dark-400 max-w-2xl mx-auto">
            Transform your repositories into captivating visual stories with cutting-edge AI technology.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {FEATURES.map((feature, index) => (
            <div
              key={feature.title}
              className="group p-6 rounded-2xl glass hover:bg-dark-800/50 transition-all duration-300 fade-in"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div
                className={`inline-flex p-3 rounded-xl bg-gradient-to-br ${feature.gradient} mb-4 group-hover:scale-110 transition-transform`}
              >
                <feature.icon className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
              <p className="text-dark-400 leading-relaxed">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
