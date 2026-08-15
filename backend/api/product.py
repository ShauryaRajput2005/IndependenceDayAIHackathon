from fastapi import APIRouter, HTTPException

from database.database import execute, fetch_one
from schemas.product import ProductCreate, ProductOut, ProductResponse


router = APIRouter(prefix="/api/product", tags=["product"])


@router.post("/create", response_model=ProductResponse)
def create_product(payload: ProductCreate):
    product_id = execute(
        """
        INSERT INTO products (
            name, category, description, features, problem, audience,
            price_range, competitors, platform, tone, requirements
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            payload.name,
            payload.category,
            payload.description,
            payload.features,
            payload.problem,
            payload.audience,
            payload.price_range,
            payload.competitors,
            payload.platform,
            payload.tone,
            payload.requirements,
        ),
    )
    return {"product_id": product_id, "message": "Product saved successfully"}


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int):
    row = fetch_one("SELECT * FROM products WHERE id = ?", (product_id,))
    if not row:
        raise HTTPException(status_code=404, detail="Product not found")
    return dict(row)
