import requests
from typing import Dict, List, Optional
from config import Config
from datetime import datetime, timezone

class ClickUpAPI:
    def __init__(self):
        self.token = Config.CLICKUP_API_TOKEN
        self.team_id = Config.CLICKUP_TEAM_ID
        self.space_id = Config.CLICKUP_SPACE_ID
        self.base_url = "https://api.clickup.com/api/v2"

    def is_configured(self) -> bool:
        return bool(self.token and self.team_id and self.space_id)

    def _get_headers(self) -> Dict[str, str]:
        # Personal API tokens are sent as-is, without a "Bearer" prefix
        return {'Authorization': self.token or ''}

    def get_latest_task(self) -> Optional[Dict]:
        try:
            url = f"{self.base_url}/team/{self.team_id}/task"
            params = {
                'space_ids[]': self.space_id,
                'order_by': 'updated',  # newest first; reverse=true would flip to oldest first
                'page': 0
            }
            response = requests.get(url, headers=self._get_headers(), params=params, timeout=10)
            response.raise_for_status()

            tasks = response.json().get('tasks', [])
            if not tasks:
                return None

            return self._format_task_data(tasks[0])
        except Exception as e:
            print(f"Error fetching latest task: {e}")
            return None

    def get_all_tasks(self, max_pages: int = 10) -> Optional[List[Dict]]:
        """Fetch every open task in the Space, most recently updated first"""
        try:
            url = f"{self.base_url}/team/{self.team_id}/task"
            tasks: List[Dict] = []
            for page in range(max_pages):
                params = {
                    'space_ids[]': self.space_id,
                    'order_by': 'updated',
                    'page': page
                }
                response = requests.get(url, headers=self._get_headers(), params=params, timeout=10)
                response.raise_for_status()

                data = response.json()
                tasks.extend(data.get('tasks', []))
                if data.get('last_page', True):
                    break

            return [self._format_task_data(t) for t in tasks]
        except Exception as e:
            print(f"Error fetching all tasks: {e}")
            return None

    def get_task(self, task_id: str) -> Optional[Dict]:
        try:
            url = f"{self.base_url}/task/{task_id}"
            response = requests.get(url, headers=self._get_headers(), timeout=10)
            response.raise_for_status()
            return self._format_task_data(response.json())
        except Exception as e:
            print(f"Error fetching task {task_id}: {e}")
            return None

    def _format_task_data(self, task: Dict) -> Dict:
        status = task.get('status') or {}

        assignees = [a.get('username') or a.get('email') or 'Unknown' for a in task.get('assignees', [])]

        due_date = task.get('due_date')
        try:
            due = datetime.fromtimestamp(int(due_date) / 1000, tz=timezone.utc)
            formatted_due = due.strftime('%B %d, %Y at %I:%M %p UTC')
        except (TypeError, ValueError):
            formatted_due = 'No deadline'

        return {
            'title': task.get('name', 'Untitled task'),
            'status': status.get('status', 'Unknown'),
            'status_color': status.get('color'),
            'assignees': assignees or ['Unassigned'],
            'priority': ((task.get('priority') or {}).get('priority') or '').lower() or None,
            'due_date': formatted_due,
            'url': task.get('url', '')
        }

clickup_api = ClickUpAPI()
