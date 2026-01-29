import requests
from typing import Dict, Optional
from config import Config
from datetime import datetime

class GitHubAPI:
    def __init__(self):
        self.owner = Config.GITHUB_REPO_OWNER
        self.repo = Config.GITHUB_REPO_NAME
        self.token = Config.GITHUB_TOKEN
        self.base_url = f"https://api.github.com/repos/{self.owner}/{self.repo}"
        
    def _get_headers(self) -> Dict[str, str]:
        headers = {'Accept': 'application/vnd.github.v3+json'}
        if self.token:
            headers['Authorization'] = f'token {self.token}'
        return headers
    
    def get_latest_commit(self) -> Optional[Dict]:
        try:
            url = f"{self.base_url}/commits"
            response = requests.get(url, headers=self._get_headers(), timeout = 10)
            response.raise_for_status()
            
            commits = response.json()
            if not commits:
                return None
            
            latest = commits[0]
            return self._format_commit_data(latest)
        except Exception as e:
            print(f"Error fetching latest commit: {e}")
            return None
        
    def _format_commit_data(self, commit_data: Dict) -> Dict:
        commit = commit_data.get('commit', {})
        
        timestamp_str = commit.get('author', {}).get('date', '')
        try:
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ")
            formatted_time = timestamp.strftime('%B %d, %Y at %I:%M %p UTC')
        except:
            formatted_time = timestamp_str
            
        message = commit.get('message', 'No commit message')
        message_lines = message.split('\n', 1)
        title = message_lines[0]
        description = message_lines[1].strip() if len(message_lines) > 1 else ''
        
        return {
            'sha': commit_data.get('sha', '')[:7],
            'title': title,
            'description': description,
            'author': commit.get('author', {}).get('name', 'Unknown'),
            'timestamp': formatted_time,
            'url': commit_data.get('html_url', ''),
            'branch': 'main'  # Will be overridden by webhook data if available 
        }
        
    def parse_webhook_payload(self, payload: Dict) -> Optional[Dict]:
        try:
            if 'commits' not in payload or not payload['commits']:
                return None
            
            latest_commit = payload['commits'][-1]
            
            ref = payload.get('ref', 'refs/heads/main')
            branch = ref.replace('refs/heads/', '')
            
            timestamp_str = latest_commit.get('timestamp', '')
            try: 
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S%z')
                formatted_time = timestamp.strftime('%B %d, %Y at %I:%M %p UTC')
            except:
                formatted_time = timestamp_str
            
            message = latest_commit.get('message', 'No commit message')
            message_lines = message.split('\n', 1)
            title = message_lines[0]
            description = message_lines[1].strip() if len(message_lines) > 1 else ''
            
            return {
                'sha': latest_commit.get('id', '')[:7],
                'title': title,
                'description': description,
                'author': latest_commit.get('author', {}).get('name', 'Unknown'),
                'timestamp': formatted_time,
                'url': latest_commit.get('url', ''),
                'branch': branch
            }
            
        except Exception as e:
            print(f"Error parsing webhook payload: {e}")
            return None

github_api = GitHubAPI()