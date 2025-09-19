"""
Configuration Item API endpoints.
"""
import logging
from typing import List, Optional, Dict, Any

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel

from ..models.ci import CI, CIType
from ..models.base import CriticalityLevel, EnvironmentType, LifecycleState
from ..models.relationships import RelationshipType
from ..services.ci_service import get_ci_service, CIService
from ..services.relationship_service import get_relationship_service, RelationshipService

logger = logging.getLogger(__name__)

# API Router
router = APIRouter(prefix="/cis", tags=["Configuration Items"])


# Pydantic models for requests/responses
class RelationshipRequest(BaseModel):
    """Request model for creating a relationship during CI creation."""
    target_ci_id: str
    relationship_type: RelationshipType
    description: Optional[str] = None


class CICreateRequest(BaseModel):
    """Request model for creating a CI."""
    name: str
    description: Optional[str] = None
    ci_type: CIType = CIType.GENERIC
    criticality: CriticalityLevel = CriticalityLevel.MEDIUM
    environment: EnvironmentType = EnvironmentType.PRODUCTION
    lifecycle_state: LifecycleState = LifecycleState.ACTIVE
    hostname: Optional[str] = None
    ip_address: Optional[str] = None
    fqdn: Optional[str] = None
    vendor: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    asset_tag: Optional[str] = None
    location: Optional[str] = None
    owner: Optional[str] = None
    custom_attributes: Dict[str, Any] = {}
    # Nouveau: support des relations
    relationships: List[RelationshipRequest] = []


class CIUpdateRequest(BaseModel):
    """Request model for updating a CI."""
    name: Optional[str] = None
    description: Optional[str] = None
    ci_type: Optional[CIType] = None
    criticality: Optional[CriticalityLevel] = None
    environment: Optional[EnvironmentType] = None
    lifecycle_state: Optional[LifecycleState] = None
    hostname: Optional[str] = None
    ip_address: Optional[str] = None
    fqdn: Optional[str] = None
    vendor: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    asset_tag: Optional[str] = None
    location: Optional[str] = None
    owner: Optional[str] = None
    custom_attributes: Optional[Dict[str, Any]] = None


class CIListResponse(BaseModel):
    """Response model for CI list."""
    cis: List[CI]
    total_count: int
    limit: int
    offset: int


@router.post("/", response_model=CI, status_code=201)
async def create_ci(
    ci_data: CICreateRequest,
    ci_service: CIService = Depends(get_ci_service),
    relationship_service: RelationshipService = Depends(get_relationship_service)
) -> CI:
    """Create a new Configuration Item with optional relationships."""
    try:
        # Séparer les relations des données du CI
        relationships = ci_data.relationships
        ci_dict = ci_data.model_dump(exclude_unset=True, exclude={"relationships"})
        
        # Créer le CI
        ci = await ci_service.create_ci(ci_dict)
        
        # Créer les relations si spécifiées
        if relationships:
            for rel_data in relationships:
                try:
                    await relationship_service.create_relationship(
                        from_ci_id=ci.id,
                        to_ci_id=rel_data.target_ci_id,
                        relationship_type=rel_data.relationship_type,
                        properties={"description": rel_data.description} if rel_data.description else None
                    )
                except Exception as rel_error:
                    logger.warning(f"Failed to create relationship from {ci.id} to {rel_data.target_ci_id}: {rel_error}")
                    # Continue creating other relationships even if one fails
        
        return ci
    except Exception as e:
        logger.error(f"Error creating CI: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create CI: {str(e)}")


@router.post("/with-relationships", response_model=Dict[str, Any], status_code=201)
async def create_ci_with_relationships(
    ci_data: CICreateRequest,
    ci_service: CIService = Depends(get_ci_service),
    relationship_service: RelationshipService = Depends(get_relationship_service)
) -> Dict[str, Any]:
    """Create a new Configuration Item with relationships in a single transaction."""
    created_relationships = []
    failed_relationships = []
    
    try:
        # Séparer les relations des données du CI
        relationships = ci_data.relationships
        ci_dict = ci_data.model_dump(exclude_unset=True, exclude={"relationships"})
        
        # Créer le CI
        ci = await ci_service.create_ci(ci_dict)
        
        # Créer les relations si spécifiées
        if relationships:
            for rel_data in relationships:
                try:
                    relationship = await relationship_service.create_relationship(
                        from_ci_id=ci.id,
                        to_ci_id=rel_data.target_ci_id,
                        relationship_type=rel_data.relationship_type,
                        properties={"description": rel_data.description} if rel_data.description else None
                    )
                    created_relationships.append({
                        "target_ci_id": rel_data.target_ci_id,
                        "relationship_type": rel_data.relationship_type.value,
                        "description": rel_data.description
                    })
                except Exception as rel_error:
                    logger.warning(f"Failed to create relationship from {ci.id} to {rel_data.target_ci_id}: {rel_error}")
                    failed_relationships.append({
                        "target_ci_id": rel_data.target_ci_id,
                        "relationship_type": rel_data.relationship_type.value,
                        "error": str(rel_error)
                    })
        
        return {
            "ci": ci.model_dump(),
            "created_relationships": created_relationships,
            "failed_relationships": failed_relationships,
            "success": True
        }
    except Exception as e:
        logger.error(f"Error creating CI with relationships: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create CI: {str(e)}")


@router.get("/", response_model=CIListResponse)
async def get_cis(
    ci_type: Optional[CIType] = Query(None, description="Filter by CI type"),
    environment: Optional[EnvironmentType] = Query(None, description="Filter by environment"),
    criticality: Optional[CriticalityLevel] = Query(None, description="Filter by criticality"),
    limit: int = Query(100, ge=1, le=1000, description="Number of CIs to return"),
    offset: int = Query(0, ge=0, description="Number of CIs to skip"),
    ci_service: CIService = Depends(get_ci_service)
) -> CIListResponse:
    """Get all Configuration Items with optional filters."""
    try:
        cis = await ci_service.get_all_cis(
            ci_type=ci_type,
            environment=environment,
            criticality=criticality,
            limit=limit,
            offset=offset
        )
        
        total_count = await ci_service.get_ci_count()
        
        return CIListResponse(
            cis=cis,
            total_count=total_count,
            limit=limit,
            offset=offset
        )
    except Exception as e:
        logger.error(f"Error getting CIs: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve CIs: {str(e)}")


@router.get("/search", response_model=List[CI])
async def search_cis(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(50, ge=1, le=100, description="Number of results to return"),
    ci_service: CIService = Depends(get_ci_service)
) -> List[CI]:
    """Search Configuration Items by text."""
    try:
        cis = await ci_service.search_cis(q, limit)
        return cis
    except Exception as e:
        logger.error(f"Error searching CIs: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/count", response_model=Dict[str, int])
async def get_ci_count(
    ci_service: CIService = Depends(get_ci_service)
) -> Dict[str, int]:
    """Get total count of Configuration Items."""
    try:
        count = await ci_service.get_ci_count()
        return {"total_count": count}
    except Exception as e:
        logger.error(f"Error getting CI count: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get count: {str(e)}")


@router.get("/{ci_id}", response_model=CI)
async def get_ci(
    ci_id: str,
    ci_service: CIService = Depends(get_ci_service)
) -> CI:
    """Get a Configuration Item by ID."""
    try:
        ci = await ci_service.get_ci(ci_id)
        if not ci:
            raise HTTPException(status_code=404, detail=f"CI not found: {ci_id}")
        return ci
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting CI {ci_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve CI: {str(e)}")


@router.put("/{ci_id}", response_model=CI)
async def update_ci(
    ci_id: str,
    update_data: CIUpdateRequest,
    ci_service: CIService = Depends(get_ci_service)
) -> CI:
    """Update a Configuration Item."""
    try:
        update_dict = update_data.model_dump(exclude_unset=True, exclude_none=True)
        
        if not update_dict:
            raise HTTPException(status_code=400, detail="No fields provided for update")
        
        ci = await ci_service.update_ci(ci_id, update_dict)
        if not ci:
            raise HTTPException(status_code=404, detail=f"CI not found: {ci_id}")
        
        return ci
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating CI {ci_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update CI: {str(e)}")


@router.delete("/{ci_id}", status_code=204)
async def delete_ci(
    ci_id: str,
    ci_service: CIService = Depends(get_ci_service)
):
    """Delete a Configuration Item."""
    try:
        deleted = await ci_service.delete_ci(ci_id)
        if not deleted:
            raise HTTPException(status_code=404, detail=f"CI not found: {ci_id}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting CI {ci_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete CI: {str(e)}")