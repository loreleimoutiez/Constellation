"""
API package for Constellation CMDB.
"""

from .ci_endpoints import router as ci_router

__all__ = [
    "ci_router",
]
