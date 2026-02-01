"""
Video generation service using OpenAI Sora
"""

import httpx
import asyncio
import os
import logging
from typing import Optional, Callable
from openai import AsyncOpenAI

from app.models.schemas import RepoData, VideoStyle


# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Sora API base URL
SORA_API_BASE = "https://api.openai.com/v1/videos"


# Map duration to Sora's allowed values (4, 8, or 12 seconds)
def get_sora_duration(requested_duration: int) -> str:
    """Map requested duration to Sora's allowed values (returns string)"""
    if requested_duration <= 4:
        return "4"
    elif requested_duration <= 8:
        return "8"
    else:
        return "12"  # Max is 12 seconds


# Map to valid Sora sizes
def get_sora_size(landscape: bool = True) -> str:
    """Get valid Sora size. Allowed: 720x1280, 1280x720, 1024x1792, 1792x1024"""
    return "1280x720" if landscape else "720x1280"


class VideoService:
    """Service for generating videos using OpenAI Sora"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = AsyncOpenAI(api_key=api_key)
        self.output_dir = "generated_videos"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Headers for Sora API requests
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    async def generate_script(self, repo_data: RepoData) -> str:
        """
        Generate a video script based on repository data
        
        Args:
            repo_data: Repository information
            
        Returns:
            Video script/prompt for Sora
        """
        # Extract key information for product demo
        languages = ', '.join(repo_data.languages[:3]) if repo_data.languages else 'code'
        primary_lang = repo_data.language or (repo_data.languages[0] if repo_data.languages else 'code')
        
        # Determine product type and demo focus
        demo_scenarios = []
        if repo_data.description:
            desc_lower = repo_data.description.lower()
            
            # Web applications
            if any(word in desc_lower for word in ['web', 'website', 'frontend', 'react', 'vue', 'angular', 'dashboard']):
                demo_scenarios.append('web application interface with interactive elements, smooth page transitions, responsive design elements')
                
            # APIs and backend services  
            elif any(word in desc_lower for word in ['api', 'backend', 'server', 'microservice', 'rest', 'graphql']):
                demo_scenarios.append('API data flow visualization with requests and responses, database interactions, server processing')
                
            # Mobile apps
            elif any(word in desc_lower for word in ['mobile', 'android', 'ios', 'flutter', 'react native']):
                demo_scenarios.append('mobile app interface with touch interactions, screen transitions, feature demonstrations')
                
            # Developer tools and libraries
            elif any(word in desc_lower for word in ['library', 'framework', 'cli', 'tool', 'sdk', 'package']):
                demo_scenarios.append('developer tool workflow showing code integration, terminal commands, build processes')
                
            # Data/AI/ML projects
            elif any(word in desc_lower for word in ['machine learning', 'ai', 'data', 'analytics', 'model', 'neural']):
                demo_scenarios.append('data processing pipeline with flowing information, model training visualization, analytics dashboards')
                
            # Games and graphics
            elif any(word in desc_lower for word in ['game', 'graphics', 'engine', 'rendering', '3d', 'animation']):
                demo_scenarios.append('interactive game elements, 3D graphics rendering, animation sequences')
                
            # DevOps and infrastructure  
            elif any(word in desc_lower for word in ['docker', 'kubernetes', 'deployment', 'infrastructure', 'devops']):
                demo_scenarios.append('deployment pipeline visualization, container orchestration, infrastructure scaling')
        
        # Default scenario if no specific type detected
        if not demo_scenarios:
            demo_scenarios.append(f'{primary_lang} software demonstration with code execution, feature showcases, user interface interactions')
        
        demo_focus = demo_scenarios[0]
        
        # Build repository-specific demo context
        repo_context = f"""
Product: {repo_data.name}
Primary Technology: {primary_lang}
Description: {repo_data.description[:200] if repo_data.description else 'Software project'}
Key Features: {', '.join(repo_data.topics[:5]) if repo_data.topics else 'Core functionality'}
Popularity: {repo_data.stars} stars, {repo_data.forks} forks
Technologies: {languages}
"""

        prompt = f"""Create a video prompt for a product demo video showcasing this software project:

{repo_context}

Demo Requirements:
- Show the product in action demonstrating its core functionality
- Focus on: {demo_focus}
- Create a product showcase that highlights key features and capabilities
- Use screen-like interfaces, code editors, terminal windows, or app interfaces (NO real people or faces)
- Show workflow, interactions, and results
- Demonstrate value proposition visually
- NO human hands, faces, or people - only software interfaces and digital elements
- NO brand logos or company names
- Keep it focused on showing "what the product does"
- 4-12 second demo showcase
- Use smooth camera movements and professional presentation

Example demo concepts:
- Web app: "Clean dashboard interface with data visualizations updating in real-time, smooth navigation between different sections"
- API: "Terminal showing API requests with JSON responses, data flowing between services, status indicators"  
- Mobile app: "Mobile interface with feature demonstrations, screen transitions, interactive elements responding"
- Library/Tool: "Code editor showing integration examples, terminal commands executing, build processes completing"

Create a specific product demo video prompt for {repo_data.name}:"""

        response = await self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": f"Create product demo video prompts that showcase software functionality. Focus on demonstrating what the product does through interface interactions, workflows, and results. Use digital interfaces, screens, and software elements only. NO people, faces, hands, or human figures. Show the product value through visual demonstration. For {repo_data.name}, emphasize {demo_focus}."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    async def generate_video_with_progress(
        self,
        script: str,
        style: VideoStyle = VideoStyle.TECH,
        duration: int = 30,
        progress_callback: Optional[Callable[[int, str], None]] = None,
        image_urls: Optional[list[str]] = None
    ) -> str:
        """
        Generate video using OpenAI Sora API with progress updates
        
        Args:
            script: Video prompt/script
            style: Visual style for the video
            duration: Duration in seconds (will be mapped to 5, 10, 15, or 20)
            progress_callback: Optional callback for progress updates (progress%, message)
            image_urls: Optional list of image URLs to use as visual reference
            
        Returns:
            Path to the generated video
        """
        # Style modifiers for the prompt (kept simple to avoid moderation issues)
        style_modifiers = {
            VideoStyle.CINEMATIC: "Slow camera movement, dramatic lighting, depth of field",
            VideoStyle.TECH: "Neon blue and purple colors, dark background, glowing elements",
            VideoStyle.MINIMAL: "Clean white background, subtle animations, simple shapes",
            VideoStyle.DYNAMIC: "Fast motion, vibrant colors, energetic particle effects",
            VideoStyle.DOCUMENTARY: "Steady camera, neutral lighting, smooth transitions"
        }
        
        style_modifier = style_modifiers.get(style, style_modifiers[VideoStyle.TECH])
        
        # Build enhanced prompt with style (keep it concise)
        enhanced_prompt = f"{script} Style: {style_modifier}."

        # Get Sora-compatible duration (4, 8, or 12 seconds as string)
        sora_duration = get_sora_duration(duration)
        # Get valid size (1280x720 for landscape HD)
        sora_size = get_sora_size(landscape=True)
        
        try:
            # Create video using OpenAI Sora Videos API via direct HTTP
            # Reference: https://platform.openai.com/docs/api-reference/videos/create
            if progress_callback:
                progress_callback(0, "Submitting video to Sora...")
            
            # Use form data as per API docs (curl uses -F flags)
            form_data = {
                "model": "sora-2-pro",
                "prompt": enhanced_prompt,
                "size": sora_size,
                "seconds": sora_duration
            }
            
            # Log the request details
            logger.info("=" * 60)
            logger.info("SORA API REQUEST")
            logger.info("=" * 60)
            logger.info(f"URL: {SORA_API_BASE}")
            logger.info(f"Model: {form_data['model']}")
            logger.info(f"Size: {form_data['size']}")
            logger.info(f"Seconds: {form_data['seconds']}")
            logger.info(f"Prompt length: {len(form_data['prompt'])} chars")
            if image_urls:
                logger.info(f"Image URLs available (not used - requires multipart): {len(image_urls)}")
                for i, url in enumerate(image_urls[:5]):
                    logger.info(f"  Image {i+1}: {url}")
            logger.info("=" * 60)
            logger.info("FULL PROMPT BEING SENT TO SORA:")
            logger.info("=" * 60)
            logger.info(form_data['prompt'])
            logger.info("=" * 60)
            
            async with httpx.AsyncClient(timeout=60) as client:
                # Step 1: Create video job using JSON
                create_response = await client.post(
                    SORA_API_BASE,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json=form_data  # Use json= for application/json content type
                )
                
                # Log response details
                logger.info(f"Response Status: {create_response.status_code}")
                logger.info(f"Response Headers: {dict(create_response.headers)}")
                logger.info(f"Response Body: {create_response.text}")
                
                if create_response.status_code != 200:
                    error_detail = create_response.text
                    logger.error(f"Sora API Error: {error_detail}")
                    raise Exception(f"Sora API returned {create_response.status_code}: {error_detail}")
                
                create_response.raise_for_status()
                video_data = create_response.json()
            
            video_id = video_data["id"]
            video_status = video_data.get("status", "queued")
            
            if progress_callback:
                progress_callback(5, "Video queued, waiting for processing...")
            
            # Step 2: Poll for completion with progress updates
            async with httpx.AsyncClient(timeout=30) as client:
                while video_status in ["queued", "in_progress"]:
                    await asyncio.sleep(10)  # Wait 10 seconds between polls
                    
                    status_response = await client.get(
                        f"{SORA_API_BASE}/{video_id}",
                        headers=self.headers
                    )
                    status_response.raise_for_status()
                    video_data = status_response.json()
                    
                    video_status = video_data.get("status", "in_progress")
                    sora_progress = video_data.get("progress", 0) or 0
                    
                    status_msg = "Queued..." if video_status == "queued" else f"Generating video... {sora_progress}%"
                    
                    if progress_callback:
                        progress_callback(sora_progress, status_msg)
            
            if video_status == "failed":
                error_msg = video_data.get("error", "Unknown error")
                raise Exception(f"Video generation failed in Sora: {error_msg}")
            
            if progress_callback:
                progress_callback(95, "Downloading video...")
            
            # Download the video content
            video_path = await self._download_video_from_sora(video_id)
            
            if progress_callback:
                progress_callback(100, "Video ready!")
            
            return video_path
            
        except Exception as e:
            raise Exception(f"Video generation failed: {str(e)}")
    
    async def _download_video_from_sora(self, video_id: str) -> str:
        """Download video from Sora API and save locally"""
        try:
            # Use httpx to download the video content directly
            # The OpenAI Python SDK may not have async download_content
            async with httpx.AsyncClient(timeout=300) as client:
                response = await client.get(
                    f"https://api.openai.com/v1/videos/{video_id}/content",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    follow_redirects=True
                )
                response.raise_for_status()
                
                video_path = os.path.join(self.output_dir, f"{video_id}.mp4")
                
                with open(video_path, "wb") as f:
                    f.write(response.content)
                
                return video_path
            
        except Exception as e:
            raise Exception(f"Failed to download video: {str(e)}")
    
    async def _download_video(self, video_url: str, job_id: str) -> str:
        """Download video from URL and save locally"""
        async with httpx.AsyncClient() as client:
            response = await client.get(video_url)
            response.raise_for_status()
            
            video_path = os.path.join(self.output_dir, f"{job_id}.mp4")
            with open(video_path, "wb") as f:
                f.write(response.content)
            
            return video_path
    
    async def generate_thumbnail(self, video_id: str) -> Optional[str]:
        """Download thumbnail from Sora API"""
        try:
            # Sora provides thumbnails via the content endpoint with variant=thumbnail
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"https://api.openai.com/v1/videos/{video_id}/content?variant=thumbnail",
                    headers={"Authorization": f"Bearer {self.api_key}"}
                )
                response.raise_for_status()
                
                thumbnail_path = os.path.join(self.output_dir, f"{video_id}_thumb.webp")
                with open(thumbnail_path, "wb") as f:
                    f.write(response.content)
                
                return thumbnail_path
        except Exception:
            return None
