import { useState } from 'react'
import { Header } from './components/Header'
import { Hero } from './components/Hero'
import { VideoForm } from './components/VideoForm'
import { VideoProgress } from './components/VideoProgress'
import { VideoResult } from './components/VideoResult'
import { Features } from './components/Features'
import { Footer } from './components/Footer'
import { VideoStatus } from './types'

function App() {
  const [jobId, setJobId] = useState<string | null>(null)
  const [status, setStatus] = useState<VideoStatus | null>(null)
  const [videoUrl, setVideoUrl] = useState<string | null>(null)

  const handleGenerationStart = (id: string) => {
    setJobId(id)
    setStatus({
      job_id: id,
      status: 'pending',
      message: 'Starting video generation...',
      progress: 0
    })
    setVideoUrl(null)
  }

  const handleStatusUpdate = (newStatus: VideoStatus) => {
    setStatus(newStatus)
    if (newStatus.status === 'completed' && newStatus.video_url) {
      setVideoUrl(newStatus.video_url)
    }
  }

  const handleReset = () => {
    setJobId(null)
    setStatus(null)
    setVideoUrl(null)
  }

  return (
    <div className="min-h-screen bg-dark-900 text-dark-100">
      <Header />
      
      <main>
        <Hero />
        
        <section id="generator" className="py-20 px-4">
          <div className="max-w-4xl mx-auto">
            {!jobId && (
              <VideoForm onGenerationStart={handleGenerationStart} />
            )}
            
            {jobId && status && status.status !== 'completed' && (
              <VideoProgress 
                jobId={jobId}
                status={status}
                onStatusUpdate={handleStatusUpdate}
                onCancel={handleReset}
              />
            )}
            
            {videoUrl && status?.status === 'completed' && (
              <VideoResult 
                videoUrl={videoUrl}
                onGenerateAnother={handleReset}
              />
            )}
          </div>
        </section>
        
        <Features />
      </main>
      
      <Footer />
    </div>
  )
}

export default App
