import json
import os
import time
from pathlib import Path
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class UserData:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / 'data'
        self.users_file = self.data_dir / 'users.json'
        self.data: Dict = {}
        self._load_data()

    def _load_data(self):
        """Load user data from JSON file"""
        try:
            if self.users_file.exists():
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            else:
                self.data = {}
                self._save_data()  # Create the file if it doesn't exist
        except Exception as e:
            logger.error(f"Error loading user data: {e}")
            self.data = {}

    def _save_data(self):
        """Save user data to JSON file"""
        try:
            self.data_dir.mkdir(parents=True, exist_ok=True)
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving user data: {e}")

    def add_user(self, user_id: int, user_data: dict):
        """Add or update user information"""
        str_id = str(user_id)  # Convert to string for JSON compatibility
        if str_id not in self.data:
            self.data[str_id] = {
                "first_seen": int(time.time()),
                "last_seen": int(time.time()),
                "total_visits": 1,
                **user_data
            }
        else:
            self.data[str_id].update({
                "last_seen": int(time.time()),
                "total_visits": self.data[str_id].get("total_visits", 0) + 1,
                **user_data
            })
        self._save_data()

    def get_user(self, user_id: int) -> Optional[dict]:
        """Get user information"""
        return self.data.get(str(user_id))

    def get_all_users(self) -> Dict:
        """Get all users information"""
        return self.data

    def get_total_users(self) -> int:
        """Get total number of users"""
        return len(self.data)

# Create a singleton instance
user_db = UserData()
