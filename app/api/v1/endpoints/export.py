from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from typing import Optional
import xml.etree.ElementTree as ET

router = APIRouter(prefix="/export", tags=["export"])

class ExportRequest(BaseModel):
    xml_content: str
    format: str  #png, jpeg, pdf, svg

@router.post("/png")
async def export_to_png(request: ExportRequest):
    return Response(content="PNG data will be here", media_type="image/png", headers={"Content-Disposition": "attachment; filename=leaflet.png"})

@router.post("/pdf")
async def export_to_pdf(request: ExportRequest):
    return Response(content="PDF data will be here", media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=leaflet.pdf"})

@router.post("/svg")
async def export_to_svg(request: ExportRequest):
    return Response(content="SVG data will be here", media_type="image/svg+xml", headers={"Content-Disposition": "attachment; filename=leaflet.svg"})