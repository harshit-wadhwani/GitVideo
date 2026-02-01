"""
Repository ingestion service - analyzes GitHub repositories
"""

import httpx
import asyncio
import logging
from typing import Optional
from urllib.parse import urlparse

from app.models.schemas import RepoData

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class RepoService:
    """Service for ingesting and analyzing GitHub repositories"""
    
    def __init__(self):
        self.github_api_base = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitVideo/1.0"
        }
    
    def _parse_github_url(self, url: str) -> tuple[str, str]:
        """Extract owner and repo name from GitHub URL"""
        parsed = urlparse(url)
        path_parts = parsed.path.strip("/").split("/")
        
        if len(path_parts) < 2:
            raise ValueError("Invalid GitHub URL format")
        
        owner = path_parts[0]
        repo = path_parts[1].replace(".git", "")
        
        return owner, repo
    
    async def ingest_repository(self, repo_url: str) -> RepoData:
        """
        Ingest a GitHub repository and extract relevant information
        
        Args:
            repo_url: GitHub repository URL
            
        Returns:
            RepoData containing repository information
        """
        owner, repo = self._parse_github_url(repo_url)
        
        async with httpx.AsyncClient() as client:
            # Fetch repository info, languages, and README in parallel
            repo_info_task = self._fetch_repo_info(client, owner, repo)
            languages_task = self._fetch_languages(client, owner, repo)
            readme_task = self._fetch_readme(client, owner, repo)
            tree_task = self._fetch_file_tree(client, owner, repo)
            topics_task = self._fetch_topics(client, owner, repo)
            
            results = await asyncio.gather(
                repo_info_task,
                languages_task,
                readme_task,
                tree_task,
                topics_task,
                return_exceptions=True
            )
            
            repo_info = results[0] if not isinstance(results[0], Exception) else {}
            languages = results[1] if not isinstance(results[1], Exception) else []
            readme = results[2] if not isinstance(results[2], Exception) else None
            file_tree = results[3] if not isinstance(results[3], Exception) else ""
            topics = results[4] if not isinstance(results[4], Exception) else []
        
        # Build summary
        summary = self._build_summary(repo_info, languages, readme)
        
        # Identify key files
        key_files = self._identify_key_files(file_tree)
        
        # Extract image URLs from file tree
        image_urls = self._extract_image_urls(file_tree, owner, repo)
        
        # Log found images
        logger.info("=" * 60)
        logger.info("REPOSITORY ANALYSIS COMPLETE")
        logger.info("=" * 60)
        logger.info(f"Repo: {owner}/{repo}")
        logger.info(f"Languages: {languages}")
        logger.info(f"Topics: {topics}")
        logger.info(f"Key files: {key_files}")
        logger.info(f"Images found: {len(image_urls)}")
        for i, url in enumerate(image_urls):
            logger.info(f"  Image {i+1}: {url}")
        logger.info("=" * 60)
        
        return RepoData(
            name=repo_info.get("name", repo),
            description=repo_info.get("description"),
            language=repo_info.get("language"),
            languages=languages,
            topics=topics,
            stars=repo_info.get("stargazers_count", 0),
            forks=repo_info.get("forks_count", 0),
            file_tree=file_tree,
            summary=summary,
            key_files=key_files,
            readme_content=readme,
            image_urls=image_urls
        )
    
    async def _fetch_repo_info(self, client: httpx.AsyncClient, owner: str, repo: str) -> dict:
        """Fetch basic repository information"""
        url = f"{self.github_api_base}/repos/{owner}/{repo}"
        response = await client.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    async def _fetch_languages(self, client: httpx.AsyncClient, owner: str, repo: str) -> list[str]:
        """Fetch repository languages"""
        url = f"{self.github_api_base}/repos/{owner}/{repo}/languages"
        response = await client.get(url, headers=self.headers)
        response.raise_for_status()
        languages_data = response.json()
        return list(languages_data.keys())
    
    async def _fetch_readme(self, client: httpx.AsyncClient, owner: str, repo: str) -> Optional[str]:
        """Fetch repository README content"""
        url = f"{self.github_api_base}/repos/{owner}/{repo}/readme"
        headers = {**self.headers, "Accept": "application/vnd.github.v3.raw"}
        
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.text[:5000]  # Limit README content
        except httpx.HTTPStatusError:
            return None
    
    async def _fetch_file_tree(self, client: httpx.AsyncClient, owner: str, repo: str) -> str:
        """Fetch repository file tree"""
        url = f"{self.github_api_base}/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"
        
        try:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            # Build tree structure
            tree_lines = []
            for item in data.get("tree", [])[:100]:  # Limit to 100 files
                path = item["path"]
                item_type = "📁" if item["type"] == "tree" else "📄"
                tree_lines.append(f"{item_type} {path}")
            
            return "\n".join(tree_lines)
        except httpx.HTTPStatusError:
            return ""
    
    async def _fetch_topics(self, client: httpx.AsyncClient, owner: str, repo: str) -> list[str]:
        """Fetch repository topics/tags"""
        url = f"{self.github_api_base}/repos/{owner}/{repo}/topics"
        headers = {**self.headers, "Accept": "application/vnd.github.mercy-preview+json"}
        
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data.get("names", [])
        except httpx.HTTPStatusError:
            return []
    
    def _build_summary(self, repo_info: dict, languages: list[str], readme: Optional[str]) -> str:
        """Build a comprehensive summary of the repository"""
        parts = []
        
        name = repo_info.get("name", "Unknown")
        parts.append(f"Repository: {name}")
        
        if repo_info.get("description"):
            parts.append(f"Description: {repo_info['description']}")
        
        if languages:
            parts.append(f"Languages: {', '.join(languages[:5])}")
        
        if repo_info.get("stargazers_count"):
            parts.append(f"Stars: {repo_info['stargazers_count']:,}")
        
        if readme:
            # Extract first paragraph of README
            readme_preview = readme.split("\n\n")[0][:500]
            parts.append(f"README Preview: {readme_preview}")
        
        return "\n".join(parts)
    
    def _identify_key_files(self, file_tree: str) -> list[str]:
        """Identify key files in the repository"""
        key_patterns = [
            "README", "LICENSE", "CONTRIBUTING",
            "package.json", "requirements.txt", "Cargo.toml",
            "setup.py", "pyproject.toml", "go.mod",
            "Dockerfile", "docker-compose", ".github/workflows"
        ]
        
        key_files = []
        for line in file_tree.split("\n"):
            for pattern in key_patterns:
                if pattern.lower() in line.lower():
                    # Extract filename
                    filename = line.replace("📁 ", "").replace("📄 ", "")
                    key_files.append(filename)
                    break
        
        return key_files[:10]  # Limit to 10 key files
    
    def _extract_image_urls(self, file_tree: str, owner: str, repo: str) -> list[str]:
        """Extract image URLs from repository file tree"""
        image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg']
        image_urls = []
        
        # Parse file tree to find image files
        lines = file_tree.split("\n")
        current_path = []
        
        for line in lines:
            if not line.strip():
                continue
            
            # Count indentation (spaces or tree characters)
            stripped = line.lstrip("│ ├└─ ")
            indent_level = (len(line) - len(stripped)) // 4
            
            # Clean filename
            filename = stripped.replace("📁 ", "").replace("📄 ", "").strip()
            if not filename:
                continue
            
            # Check if it's an image file
            lower_filename = filename.lower()
            is_image = any(lower_filename.endswith(ext) for ext in image_extensions)
            
            if is_image:
                # Construct raw GitHub URL
                # Format: https://raw.githubusercontent.com/{owner}/{repo}/main/{path}
                raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/{filename}"
                image_urls.append(raw_url)
                
                # Also try common subdirectories
                for subdir in ['assets', 'images', 'img', 'docs', 'static', 'public']:
                    if subdir in file_tree.lower():
                        alt_url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/{subdir}/{filename}"
                        if alt_url not in image_urls:
                            image_urls.append(alt_url)
        
        # Limit to 5 images to avoid too many API calls
        return image_urls[:5]
