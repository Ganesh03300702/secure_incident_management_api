import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from app.database import get_connection
from app.models import IncidentCreate, IncidentUpdate, LoginRequest
from app.auth import require_token, DEMO_TOKEN

router = APIRouter(prefix="/api/v1", tags=["Incidents"])
logger = logging.getLogger("incident_api")

@router.post("/auth/login")
def login(payload: LoginRequest):
    if payload.username == "admin" and payload.password == "admin123":
        return {"access_token": DEMO_TOKEN, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/incidents", status_code=201, dependencies=[Depends(require_token)])
def create_incident(payload: IncidentCreate):
    with get_connection() as conn:
        cur = conn.execute(
            """INSERT INTO incidents(title, description, priority, status, reporter)
               VALUES (?, ?, ?, 'open', ?)""",
            (payload.title, payload.description, payload.priority, payload.reporter),
        )
        conn.commit()
        incident_id = cur.lastrowid
    logger.info("Created incident %s", incident_id)
    return {"id": incident_id, **payload.model_dump(), "status": "open"}

@router.get("/incidents", dependencies=[Depends(require_token)])
def list_incidents(
    priority: str | None = Query(default=None),
    status: str | None = Query(default=None),
):
    query = "SELECT * FROM incidents WHERE 1=1"
    params = []
    if priority:
        query += " AND priority = ?"
        params.append(priority)
    if status:
        query += " AND status = ?"
        params.append(status)
    query += " ORDER BY id DESC"
    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()
    return [dict(r) for r in rows]

@router.get("/incidents/{incident_id}", dependencies=[Depends(require_token)])
def get_incident(incident_id: int):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM incidents WHERE id = ?", (incident_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Incident not found")
    return dict(row)

@router.put("/incidents/{incident_id}", dependencies=[Depends(require_token)])
def update_incident(incident_id: int, payload: IncidentUpdate):
    changes = {k: v for k, v in payload.model_dump(exclude_none=True).items()}
    if not changes:
        raise HTTPException(status_code=400, detail="No fields supplied for update")
    with get_connection() as conn:
        existing = conn.execute("SELECT * FROM incidents WHERE id = ?", (incident_id,)).fetchone()
        if not existing:
            raise HTTPException(status_code=404, detail="Incident not found")
        set_clause = ", ".join(f"{k} = ?" for k in changes)
        values = list(changes.values()) + [incident_id]
        conn.execute(f"UPDATE incidents SET {set_clause} WHERE id = ?", values)
        conn.commit()
        row = conn.execute("SELECT * FROM incidents WHERE id = ?", (incident_id,)).fetchone()
    logger.info("Updated incident %s", incident_id)
    return dict(row)

@router.delete("/incidents/{incident_id}", status_code=204, dependencies=[Depends(require_token)])
def delete_incident(incident_id: int):
    with get_connection() as conn:
        cur = conn.execute("DELETE FROM incidents WHERE id = ?", (incident_id,))
        conn.commit()
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Incident not found")
    logger.info("Deleted incident %s", incident_id)
