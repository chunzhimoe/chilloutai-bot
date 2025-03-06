import logging
from enum import Enum, auto
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class UserState(Enum):
    IDLE = auto()
    WAITING_FOR_IMAGE = auto()
    WAITING_FOR_CONTROLNET_TYPE = auto()
    WAITING_FOR_CONTROLNET_PROMPT = auto()
    WAITING_FOR_IPADAPTER_PROMPT = auto()

class UserSession:
    def __init__(self):
        self.state = UserState.IDLE
        self.image_url = None
        self.image_path = None
        self.controlnet_type = None
        self.last_activity = datetime.now()
        self.additional_params = {}

class UserStateManager:
    def __init__(self):
        self.user_sessions = {}
        self.session_timeout = timedelta(minutes=30)
    
    def get_user_session(self, user_id):
        """Get or create a user session"""
        # Clean up expired sessions
        self._cleanup_expired_sessions()
        
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = UserSession()
        
        # Update last activity
        self.user_sessions[user_id].last_activity = datetime.now()
        return self.user_sessions[user_id]
    
    def set_user_state(self, user_id, state, **kwargs):
        """Set the state for a user session"""
        session = self.get_user_session(user_id)
        session.state = state
        
        # Update any additional attributes
        for key, value in kwargs.items():
            setattr(session, key, value)
        
        logger.info(f"User {user_id} state changed to {state}")
        return session
    
    def reset_user_state(self, user_id):
        """Reset user state to IDLE"""
        session = self.get_user_session(user_id)
        old_state = session.state
        
        session.state = UserState.IDLE
        session.image_url = None
        session.image_path = None
        session.controlnet_type = None
        session.additional_params = {}
        
        logger.info(f"User {user_id} state reset from {old_state} to IDLE")
        return session
    
    def _cleanup_expired_sessions(self):
        """Remove expired user sessions"""
        now = datetime.now()
        expired_users = [
            user_id for user_id, session in self.user_sessions.items()
            if now - session.last_activity > self.session_timeout
        ]
        
        for user_id in expired_users:
            del self.user_sessions[user_id]
            logger.info(f"Removed expired session for user {user_id}")

# Create a global instance
state_manager = UserStateManager()
