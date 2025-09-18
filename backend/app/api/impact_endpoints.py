"""
Relationship and Impact Analysis API endpoints.
"""
import logging
from typing import List, Optional, Dict, Any

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel

from ..models.relationships import RelationshipType, Relationship
from ..services.relationship_service import get_relationship_service, RelationshipService

logger = logging.getLogger(__name__)

# API Router
router = APIRouter(tags=["Relationships & Impact Analysis"])


# Pydantic models for requests/responses
class RelationshipCreateRequest(BaseModel):
    """Request model for creating a relationship."""
    from_ci_id: str
    to_ci_id: str
    relationship_type: RelationshipType
    description: Optional[str] = None


class ImpactAnalysisResponse(BaseModel):
    """Response model for impact analysis."""
    source_ci: str
    total_impacted: int
    impacted_cis: List[Dict[str, Any]]
    criticality_breakdown: Dict[str, int]
    risk_score: float
    max_depth_analyzed: int


class DependencyAnalysisResponse(BaseModel):
    """Response model for dependency analysis."""
    source_ci: str
    total_dependencies: int
    dependencies: List[Dict[str, Any]]
    max_depth_analyzed: int


class BusFactorResponse(BaseModel):
    """Response model for bus factor analysis."""
    high_risk_cis: List[Dict[str, Any]]
    total_analyzed: int
    analysis_date: str


# Relationship management endpoints
@router.get("/relationships", response_model=List[Dict[str, Any]])
async def get_all_relationships(
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of relationships to return"),
    offset: int = Query(0, ge=0, description="Number of relationships to skip"),
    relationship_service: RelationshipService = Depends(get_relationship_service)
):
    """Get all relationships in the system."""
    try:
        connection = await relationship_service._get_connection()
        
        query = """
        MATCH (from_ci:CI)-[r:RELATED]->(to_ci:CI)
        RETURN r.id as rel_id, r.type as rel_type, r.created_at as rel_created_at,
               from_ci.id as from_ci_id, from_ci.name as from_ci_name,
               to_ci.id as to_ci_id, to_ci.name as to_ci_name
        ORDER BY r.created_at DESC
        SKIP $offset LIMIT $limit
        """
        
        result = await connection.execute_query(query, {"offset": offset, "limit": limit})
        relationships = []
        
        for record in result:
            relationships.append({
                "id": record.get("rel_id"),
                "type": record.get("rel_type"),
                "from_ci": {
                    "id": record.get("from_ci_id"),
                    "name": record.get("from_ci_name")
                },
                "to_ci": {
                    "id": record.get("to_ci_id"),
                    "name": record.get("to_ci_name")
                },
                "created_at": str(record.get("rel_created_at")) if record.get("rel_created_at") else None
            })
        
        logger.info(f"Retrieved {len(relationships)} relationships")
        return relationships
        
    except Exception as e:
        logger.error(f"Error getting all relationships: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get relationships: {str(e)}")


@router.post("/relationships", response_model=Dict[str, str], status_code=201)
async def create_relationship(
    relationship_data: RelationshipCreateRequest,
    relationship_service: RelationshipService = Depends(get_relationship_service)
):
    """Create a new relationship between two CIs."""
    try:
        relationship = await relationship_service.create_relationship(
            from_ci_id=relationship_data.from_ci_id,
            to_ci_id=relationship_data.to_ci_id,
            relationship_type=relationship_data.relationship_type
        )
        
        return {
            "message": "Relationship created successfully",
            "from_ci": relationship_data.from_ci_id,
            "to_ci": relationship_data.to_ci_id,
            "type": relationship_data.relationship_type.value
        }
    except Exception as e:
        logger.error(f"Error creating relationship: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create relationship: {str(e)}")


@router.get("/cis/{ci_id}/relationships", response_model=List[Dict[str, Any]])
async def get_ci_relationships(
    ci_id: str,
    direction: str = Query("both", regex="^(incoming|outgoing|both)$"),
    relationship_service: RelationshipService = Depends(get_relationship_service)
):
    """Get all relationships for a specific CI."""
    try:
        relationships = await relationship_service.get_ci_relationships(ci_id, direction)
        return relationships
    except Exception as e:
        logger.error(f"Error getting relationships for CI {ci_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get relationships: {str(e)}")


@router.delete("/relationships/{relationship_id}", status_code=204)
async def delete_relationship(
    relationship_id: str,
    relationship_service: RelationshipService = Depends(get_relationship_service)
):
    """Delete a relationship."""
    try:
        deleted = await relationship_service.delete_relationship(relationship_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Relationship not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting relationship {relationship_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete relationship: {str(e)}")


# Impact analysis endpoints
@router.get("/impact/{ci_id}", response_model=ImpactAnalysisResponse)
async def analyze_impact(
    ci_id: str,
    max_depth: int = Query(3, ge=1, le=5, description="Maximum relationship depth to analyze"),
    relationship_service: RelationshipService = Depends(get_relationship_service)
):
    """
    Analyze the impact of a CI failure.
    
    This endpoint analyzes what other CIs would be affected if the specified CI fails.
    It follows dependency chains to understand the blast radius of potential outages.
    """
    try:
        analysis = await relationship_service.get_impact_analysis(ci_id, max_depth)
        return ImpactAnalysisResponse(**analysis)
    except Exception as e:
        logger.error(f"Error performing impact analysis for CI {ci_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Impact analysis failed: {str(e)}")


@router.get("/dependencies/{ci_id}", response_model=DependencyAnalysisResponse)
async def analyze_dependencies(
    ci_id: str,
    max_depth: int = Query(3, ge=1, le=5, description="Maximum relationship depth to analyze"),
    relationship_service: RelationshipService = Depends(get_relationship_service)
):
    """
    Analyze dependencies of a CI.
    
    This endpoint shows what other CIs this CI depends on to function properly.
    Useful for understanding potential single points of failure.
    """
    try:
        analysis = await relationship_service.get_dependencies(ci_id, max_depth)
        return DependencyAnalysisResponse(**analysis)
    except Exception as e:
        logger.error(f"Error performing dependency analysis for CI {ci_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Dependency analysis failed: {str(e)}")


@router.get("/busfactor", response_model=BusFactorResponse)
async def analyze_busfactor(
    relationship_service: RelationshipService = Depends(get_relationship_service)
):
    """
    Analyze bus factor risk across all CIs.
    
    Identifies CIs that have the most dependencies on them, representing potential
    single points of failure. Higher dependency counts indicate higher risk.
    """
    try:
        analysis = await relationship_service.get_busfactor_analysis()
        return BusFactorResponse(**analysis)
    except Exception as e:
        logger.error(f"Error performing bus factor analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Bus factor analysis failed: {str(e)}")


@router.get("/graph/stats", response_model=Dict[str, Any])
async def get_graph_statistics(
    relationship_service: RelationshipService = Depends(get_relationship_service)
):
    """Get overall graph statistics."""
    try:
        connection = await relationship_service._get_connection()
        
        # Get basic counts
        stats_query = """
        MATCH (ci:CI)
        OPTIONAL MATCH (ci)-[r:RELATED]-()
        RETURN 
            count(DISTINCT ci) as total_cis,
            count(r) as total_relationships,
            count(DISTINCT r.type) as relationship_types
        """
        
        result = await connection.execute_query(stats_query)
        stats = result[0] if result else {}
        
        # Get relationship type breakdown
        type_query = """
        MATCH ()-[r:RELATED]-()
        RETURN r.type as relationship_type, count(r) as count
        ORDER BY count DESC
        """
        
        type_result = await connection.execute_query(type_query)
        relationship_breakdown = {record["relationship_type"]: record["count"] for record in type_result}
        
        return {
            "total_cis": stats.get("total_cis", 0),
            "total_relationships": stats.get("total_relationships", 0),
            "unique_relationship_types": stats.get("relationship_types", 0),
            "relationship_type_breakdown": relationship_breakdown
        }
        
    except Exception as e:
        logger.error(f"Error getting graph statistics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get statistics: {str(e)}")