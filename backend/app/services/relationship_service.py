"""
Relationship service for managing CI relationships and impact analysis.
"""
import logging
from typing import List, Optional, Dict, Any
from uuid import uuid4

from ..database import get_neo4j_connection
from ..models.relationships import RelationshipType, Relationship

logger = logging.getLogger(__name__)


class RelationshipService:
    """Service for managing relationships between Configuration Items."""

    def __init__(self):
        self.connection = None

    async def _get_connection(self):
        """Get Neo4j connection."""
        if not self.connection:
            self.connection = await get_neo4j_connection()
        return self.connection

    async def create_relationship(self, 
                                from_ci_id: str, 
                                to_ci_id: str, 
                                relationship_type: RelationshipType,
                                properties: Optional[Dict[str, Any]] = None) -> Relationship:
        """Create a relationship between two CIs."""
        connection = await self._get_connection()
        
        # Generate relationship ID
        rel_id = str(uuid4())
        rel_properties = properties or {}
        rel_properties.update({
            "id": rel_id,
            "type": relationship_type.value,
            "created_at": "datetime()"
        })
        
        query = """
        MATCH (from_ci:CI {id: $from_ci_id})
        MATCH (to_ci:CI {id: $to_ci_id})
        CREATE (from_ci)-[r:RELATED {id: $rel_id, type: $rel_type, created_at: datetime()}]->(to_ci)
        RETURN r, from_ci.name as from_name, to_ci.name as to_name
        """
        
        try:
            result = await connection.execute_write_query(query, {
                "from_ci_id": from_ci_id,
                "to_ci_id": to_ci_id,
                "rel_id": rel_id,
                "rel_type": relationship_type.value
            })
            
            if result:
                relationship = Relationship(
                    source_id=from_ci_id,
                    target_id=to_ci_id,
                    relationship_type=relationship_type,
                    weight=1.0,
                    description=f"Auto-created {relationship_type.value} relationship",
                    active=True,
                    verified=False,
                    auto_discovered=True,
                    conditions=None,
                    port=None,
                    protocol=None,
                    discovered_by="system",
                    discovered_at=None,
                    last_verified=None
                )
                logger.info(f"Created relationship: {from_ci_id} -{relationship_type.value}-> {to_ci_id}")
                return relationship
            else:
                raise RuntimeError("Failed to create relationship - CIs not found")
                
        except Exception as e:
            logger.error(f"Failed to create relationship: {e}")
            raise

    async def get_ci_relationships(self, ci_id: str, direction: str = "both") -> List[Dict[str, Any]]:
        """Get all relationships for a CI."""
        connection = await self._get_connection()
        
        if direction == "outgoing":
            query = """
            MATCH (ci:CI {id: $ci_id})-[r:RELATED]->(related:CI)
            RETURN r.id as rel_id, r.type as rel_type, r.created_at as rel_created_at,
                   related.id as related_id, related.name as related_name, 'outgoing' as direction
            """
        elif direction == "incoming":
            query = """
            MATCH (ci:CI {id: $ci_id})<-[r:RELATED]-(related:CI)
            RETURN r.id as rel_id, r.type as rel_type, r.created_at as rel_created_at,
                   related.id as related_id, related.name as related_name, 'incoming' as direction
            """
        else:  # both
            query = """
            MATCH (ci:CI {id: $ci_id})-[r:RELATED]-(related:CI)
            RETURN r.id as rel_id, r.type as rel_type, r.created_at as rel_created_at,
                   related.id as related_id, related.name as related_name,
                   CASE WHEN startNode(r).id = $ci_id THEN 'outgoing' ELSE 'incoming' END as direction
            """
        
        try:
            result = await connection.execute_query(query, {"ci_id": ci_id})
            relationships = []
            
            for record in result:
                relationships.append({
                    "id": record.get("rel_id"),
                    "type": record.get("rel_type"),
                    "direction": record.get("direction"),
                    "related_ci": {
                        "id": record.get("related_id"),
                        "name": record.get("related_name")
                    },
                    "created_at": str(record.get("rel_created_at")) if record.get("rel_created_at") else None
                })
            
            logger.info(f"Found {len(relationships)} relationships for CI {ci_id}")
            return relationships
            
        except Exception as e:
            logger.error(f"Failed to get relationships for CI {ci_id}: {e}")
            raise

    async def delete_relationship(self, relationship_id: str) -> bool:
        """Delete a relationship by ID."""
        connection = await self._get_connection()
        
        query = """
        MATCH ()-[r:RELATED {id: $relationship_id}]-()
        DELETE r
        RETURN count(r) as deleted_count
        """
        
        try:
            result = await connection.execute_write_query(query, {"relationship_id": relationship_id})
            deleted_count = result[0]["deleted_count"] if result else 0
            
            if deleted_count > 0:
                logger.info(f"Deleted relationship: {relationship_id}")
                return True
            
            logger.warning(f"Relationship not found for deletion: {relationship_id}")
            return False
            
        except Exception as e:
            logger.error(f"Failed to delete relationship {relationship_id}: {e}")
            raise

    async def get_impact_analysis(self, ci_id: str, max_depth: int = 3) -> Dict[str, Any]:
        """Analyze the impact of a CI failure."""
        connection = await self._get_connection()
        
        # Get all CIs that would be impacted if this CI fails (reverse dependencies)
        # If CI A depends on CI B, then A is impacted when B fails
        query = f"""
        MATCH path = (impacted:CI)-[:RELATED*1..{max_depth}]->(ci:CI {{id: $ci_id}})
        WHERE ALL(r IN relationships(path) WHERE r.type IN ['DEPENDS_ON', 'HOSTED_ON', 'USES'])
        RETURN impacted.id as ci_id, impacted.name as ci_name, impacted.criticality as criticality,
               length(path) as distance, 
               [r in relationships(path) | r.type] as relationship_chain
        ORDER BY distance, criticality DESC
        """
        
        try:
            result = await connection.execute_query(query, {"ci_id": ci_id})
            
            impacted_cis = []
            criticality_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
            
            for record in result:
                ci_data = {
                    "ci_id": record["ci_id"],
                    "ci_name": record["ci_name"],
                    "criticality": record["criticality"],
                    "distance": record["distance"],
                    "relationship_chain": record["relationship_chain"]
                }
                impacted_cis.append(ci_data)
                
                # Count criticality levels
                criticality = record["criticality"] or "MEDIUM"
                if criticality in criticality_counts:
                    criticality_counts[criticality] += 1
            
            # Calculate risk score
            risk_score = (
                criticality_counts["CRITICAL"] * 10 +
                criticality_counts["HIGH"] * 5 +
                criticality_counts["MEDIUM"] * 2 +
                criticality_counts["LOW"] * 1
            )
            
            analysis = {
                "source_ci": ci_id,
                "total_impacted": len(impacted_cis),
                "impacted_cis": impacted_cis,
                "criticality_breakdown": criticality_counts,
                "risk_score": risk_score,
                "max_depth_analyzed": max_depth
            }
            
            logger.info(f"Impact analysis for {ci_id}: {len(impacted_cis)} CIs impacted, risk score: {risk_score}")
            return analysis
            
        except Exception as e:
            logger.error(f"Failed to perform impact analysis for CI {ci_id}: {e}")
            raise

    async def get_dependencies(self, ci_id: str, max_depth: int = 3) -> Dict[str, Any]:
        """Get all dependencies of a CI."""
        connection = await self._get_connection()
        
        query = f"""
        MATCH path = (ci:CI {{id: $ci_id}})-[:RELATED*1..{max_depth}]->(dependency:CI)
        WHERE ALL(r IN relationships(path) WHERE r.type IN ['DEPENDS_ON', 'HOSTED_ON', 'USES'])
        RETURN dependency.id as ci_id, dependency.name as ci_name, dependency.criticality as criticality,
               length(path) as distance,
               [r in relationships(path) | r.type] as relationship_chain
        ORDER BY distance, criticality DESC
        """
        
        try:
            result = await connection.execute_query(query, {"ci_id": ci_id})
            
            dependencies = []
            for record in result:
                dependencies.append({
                    "ci_id": record["ci_id"],
                    "ci_name": record["ci_name"],
                    "criticality": record["criticality"],
                    "distance": record["distance"],
                    "relationship_chain": record["relationship_chain"]
                })
            
            return {
                "source_ci": ci_id,
                "total_dependencies": len(dependencies),
                "dependencies": dependencies,
                "max_depth_analyzed": max_depth
            }
            
        except Exception as e:
            logger.error(f"Failed to get dependencies for CI {ci_id}: {e}")
            raise

    async def get_busfactor_analysis(self) -> Dict[str, Any]:
        """Analyze bus factor - CIs with the most dependencies."""
        connection = await self._get_connection()
        
        query = """
        MATCH (ci:CI)<-[:RELATED]-(dependent:CI)
        WHERE ANY(r IN [(ci)<-[rel:RELATED]-(dependent) | rel] WHERE r.type IN ['DEPENDS_ON', 'HOSTED_ON', 'USES'])
        WITH ci, count(dependent) as dependency_count
        WHERE dependency_count > 0
        RETURN ci.id as ci_id, ci.name as ci_name, ci.criticality as criticality, 
               ci.ci_type as ci_type, dependency_count
        ORDER BY dependency_count DESC, criticality DESC
        LIMIT 20
        """
        
        try:
            result = await connection.execute_query(query)
            
            high_risk_cis = []
            for record in result:
                risk_multiplier = {"CRITICAL": 3, "HIGH": 2, "MEDIUM": 1.5, "LOW": 1}.get(record["criticality"], 1)
                risk_score = record["dependency_count"] * risk_multiplier
                
                high_risk_cis.append({
                    "ci_id": record["ci_id"],
                    "ci_name": record["ci_name"],
                    "ci_type": record["ci_type"],
                    "criticality": record["criticality"],
                    "dependency_count": record["dependency_count"],
                    "risk_score": round(risk_score, 2)
                })
            
            return {
                "high_risk_cis": high_risk_cis,
                "total_analyzed": len(high_risk_cis),
                "analysis_date": "datetime()"
            }
            
        except Exception as e:
            logger.error(f"Failed to perform bus factor analysis: {e}")
            raise


# Global service instance
relationship_service = RelationshipService()


async def get_relationship_service() -> RelationshipService:
    """Dependency injection for relationship service."""
    return relationship_service