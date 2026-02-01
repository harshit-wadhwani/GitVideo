export interface VideoStatus {
  job_id: string
  status: 'pending' | 'processing' | 'completed' | 'failed'
  message: string
  progress: number
  video_url?: string
  thumbnail_url?: string
}

export interface GenerationResponse {
  job_id: string
  message: string
  status_url: string
}

export type VideoStyle = 'cinematic' | 'tech' | 'minimal' | 'dynamic' | 'documentary'

export interface GenerationRequest {
  repo_url: string
  openai_api_key: string
  video_style: VideoStyle
  duration: number
}
