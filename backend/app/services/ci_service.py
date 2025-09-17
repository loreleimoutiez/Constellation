"""
CRUD operations for Configuration Items in Neo4j.
"""
import logging
from typing import List, Optional, Dict, Any
from uuid import uuid4

from ..database import get_neo4j_connection
from ..models.ci import CI, CIType
from ..models.base import CriticalityLevel, EnvironmentType, LifecycleState

logger = logging.getLogger(__name__)


class CIService:
    """Service for Configuration Item operations."""

    def __init__(self):
        self.connection = None

    async def _get_connection(self):
        """Get Neo4j connection."""
        if not self.connection:
            self.connection = await get_neo4j_connection()
        return self.connection

    async def create_ci(self, ci_data: Dict[str, Any]) -> CI:
        """Create a new Configuration Item."""
        connection = await self._get_connection()
        
        # Generate ID if not provided
        if 'id' not in ci_data:
            ci_data['id'] = str(uuid4())
        
        # Create CI object to validate data
        ci = CI(**ci_data)
        
        # Convert to dict for Neo4j - ensure all values are primitive types
        ci_dict = ci.model_dump()
        
        # Convert enum values to strings and handle special cases
        for key, value in ci_dict.items():
            if hasattr(value, 'value'):  # Enum
                ci_dict[key] = value.value if hasattr(value, 'value') else str(value)
            elif isinstance(value, dict):  # Dict - convert to JSON string if not empty
                if value:  # Non-empty dict
                    import json
                    ci_dict[key] = json.dumps(value)
                else:  # Empty dict - remove it
                    ci_dict[key] = None
            elif isinstance(value, list) and not value:  # Empty list
                ci_dict[key] = None
            elif value is None:
                ci_dict[key] = None
        
        # Remove None values to avoid Neo4j issues
        ci_dict = {k: v for k, v in ci_dict.items() if v is not None}
        
        query = """
        CREATE (ci:CI)
        SET ci = $properties
        RETURN ci
        """
        
        try:
            result = await connection.execute_write_query(query, {"properties": ci_dict})
            logger.info(f"Created CI: {ci.id}")
            return ci
        except Exception as e:
            logger.error(f"Failed to create CI: {e}")
            raise

    def _convert_neo4j_data(self, neo4j_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert Neo4j data types to Python types."""
        from neo4j.time import DateTime
        import json
        
        converted = {}
        for key, value in neo4j_data.items():
            if isinstance(value, DateTime):
                # Convert Neo4j DateTime to Python datetime
                converted[key] = value.to_native()
            elif isinstance(value, str) and key == 'custom_attributes':
                # Try to parse JSON string back to dict
                try:
                    converted[key] = json.loads(value) if value else {}
                except (json.JSONDecodeError, TypeError):
                    converted[key] = {}
            else:
                converted[key] = value
        return converted

    async def get_ci(self, ci_id: str) -> Optional[CI]:
        """Get a Configuration Item by ID."""
        connection = await self._get_connection()
        
        query = """
        MATCH (ci:CI {id: $ci_id})
        RETURN ci
        """
        
        try:
            result = await connection.execute_query(query, {"ci_id": ci_id})
            if result:
                ci_data = self._convert_neo4j_data(result[0]["ci"])
                return CI(**ci_data)
            return None
        except Exception as e:
            logger.error(f"Failed to get CI {ci_id}: {e}")
            raise

    async def get_all_cis(self, 
                         ci_type: Optional[CIType] = None,
                         environment: Optional[EnvironmentType] = None,
                         criticality: Optional[CriticalityLevel] = None,
                         limit: int = 100,
                         offset: int = 0) -> List[CI]:
        """Get all Configuration Items with optional filters."""
        connection = await self._get_connection()
        
        # Build dynamic query based on filters
        where_clauses = []
        parameters: Dict[str, Any] = {"limit": limit, "offset": offset}
        
        if ci_type:
            where_clauses.append("ci.ci_type = $ci_type")
            parameters["ci_type"] = ci_type.value
            
        if environment:
            where_clauses.append("ci.environment = $environment")
            parameters["environment"] = environment.value
            
        if criticality:
            where_clauses.append("ci.criticality = $criticality")
            parameters["criticality"] = criticality.value
        
        where_clause = " AND ".join(where_clauses) if where_clauses else "true"
        
        query = f"""
        MATCH (ci:CI)
        WHERE {where_clause}
        RETURN ci
        ORDER BY ci.name
        SKIP $offset
        LIMIT $limit
        """
        
        try:
            result = await connection.execute_query(query, parameters)
            cis = []
            for record in result:
                ci_data = self._convert_neo4j_data(record["ci"])
                cis.append(CI(**ci_data))
            
            logger.info(f"Retrieved {len(cis)} CIs")
            return cis
        except Exception as e:
            logger.error(f"Failed to get CIs: {e}")
            raise

    async def update_ci(self, ci_id: str, update_data: Dict[str, Any]) -> Optional[CI]:
        """Update a Configuration Item."""
        connection = await self._get_connection()
        
        # Remove id from update data if present
        update_data.pop('id', None)
        
        # Build SET clause dynamically
        set_clauses = []
        parameters: Dict[str, Any] = {"ci_id": ci_id}
        
        for key, value in update_data.items():
            set_clauses.append(f"ci.{key} = ${key}")
            parameters[key] = value
        
        if not set_clauses:
            # No updates to perform
            return await self.get_ci(ci_id)
        
        set_clause = ", ".join(set_clauses)
        
        query = f"""
        MATCH (ci:CI {{id: $ci_id}})
        SET {set_clause}
        RETURN ci
        """
        
        try:
            result = await connection.execute_write_query(query, parameters)
            if result:
                ci_data = self._convert_neo4j_data(result[0]["ci"])
                updated_ci = CI(**ci_data)
                logger.info(f"Updated CI: {ci_id}")
                return updated_ci
            return None
        except Exception as e:
            logger.error(f"Failed to update CI {ci_id}: {e}")
            raise

    async def delete_ci(self, ci_id: str) -> bool:
        """Delete a Configuration Item."""
        connection = await self._get_connection()
        
        query = """
        MATCH (ci:CI {id: $ci_id})
        DETACH DELETE ci
        RETURN count(ci) as deleted_count
        """
        
        try:
            result = await connection.execute_write_query(query, {"ci_id": ci_id})
            deleted_count = result[0]["deleted_count"] if result else 0
            
            if deleted_count > 0:
                logger.info(f"Deleted CI: {ci_id}")
                return True
            
            logger.warning(f"CI not found for deletion: {ci_id}")
            return False
        except Exception as e:
            logger.error(f"Failed to delete CI {ci_id}: {e}")
            raise

    async def search_cis(self, query_text: str, limit: int = 50) -> List[CI]:
        """Search Configuration Items by text."""
        connection = await self._get_connection()
        
        query = """
        MATCH (ci:CI)
        WHERE toLower(ci.name) CONTAINS toLower($query_text)
           OR toLower(ci.description) CONTAINS toLower($query_text)
           OR toLower(ci.hostname) CONTAINS toLower($query_text)
        RETURN ci
        ORDER BY ci.name
        LIMIT $limit
        """
        
        try:
            result = await connection.execute_query(query, {
                "query_text": query_text,
                "limit": limit
            })
            
            cis = []
            for record in result:
                ci_data = self._convert_neo4j_data(record["ci"])
                cis.append(CI(**ci_data))
            
            logger.info(f"Search found {len(cis)} CIs for query: {query_text}")
            return cis
        except Exception as e:
            logger.error(f"Failed to search CIs: {e}")
            raise

    async def get_ci_count(self) -> int:
        """Get total count of Configuration Items."""
        connection = await self._get_connection()
        
        query = """
        MATCH (ci:CI)
        RETURN count(ci) as total_count
        """
        
        try:
            result = await connection.execute_query(query)
            return result[0]["total_count"] if result else 0
        except Exception as e:
            logger.error(f"Failed to get CI count: {e}")
            raise


# Global service instance
ci_service = CIService()


async def get_ci_service() -> CIService:
    """Dependency injection for CI service."""
    return ci_service