const API_BASE = '/api'

export async function generateVideo(data: {
  repo_url: string
  openai_api_key: string
  video_style: string
  duration: number
}) {
  const response = await fetch(`${API_BASE}/generate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })
  
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'Failed to start video generation')
  }
  
  return response.json()
}

export async function getVideoStatus(jobId: string) {
  const response = await fetch(`${API_BASE}/status/${jobId}`)
  
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'Failed to get status')
  }
  
  return response.json()
}

export async function getVideo(jobId: string) {
  const response = await fetch(`${API_BASE}/video/${jobId}`)
  
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'Failed to get video')
  }
  
  return response.json()
}
