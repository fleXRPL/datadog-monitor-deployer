"""
Core monitor class for defining and managing Datadog monitors.
"""
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, field

@dataclass
class Monitor:
    """
    Base class for Datadog monitors.
    """
    name: str
    type: str
    query: str
    message: str
    tags: List[str] = field(default_factory=list)
    options: Dict[str, Union[str, bool, int, float, List[str]]] = field(default_factory=dict)
    priority: Optional[int] = None
    restricted_roles: Optional[List[str]] = None
    
    def to_dict(self) -> Dict:
        """Convert monitor to dictionary format for Datadog API."""
        monitor_dict = {
            "name": self.name,
            "type": self.type,
            "query": self.query,
            "message": self.message,
            "tags": self.tags,
            "options": self.options
        }
        
        if self.priority is not None:
            monitor_dict["priority"] = self.priority
            
        if self.restricted_roles:
            monitor_dict["restricted_roles"] = self.restricted_roles
            
        return monitor_dict
    
    @classmethod
    def from_dict(cls, data: Dict) -> "Monitor":
        """Create monitor instance from dictionary."""
        return cls(
            name=data["name"],
            type=data["type"],
            query=data["query"],
            message=data["message"],
            tags=data.get("tags", []),
            options=data.get("options", {}),
            priority=data.get("priority"),
            restricted_roles=data.get("restricted_roles")
        )
    
    def validate(self) -> bool:
        """
        Validate monitor configuration.
        Returns True if valid, raises ValueError if invalid.
        """
        if not self.name:
            raise ValueError("Monitor name is required")
            
        if not self.type:
            raise ValueError("Monitor type is required")
            
        if not self.query:
            raise ValueError("Monitor query is required")
            
        if not self.message:
            raise ValueError("Monitor message is required")
            
        # Add more validation as needed
        return True 