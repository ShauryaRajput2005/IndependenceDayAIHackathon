"""
api/product.py — Product create and retrieve endpoints.
"""
import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import Product
from schemas.product import ProductCreate, ProductCreateResponse, ProductResponse
from utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/product", tags=["Product"])


@router.post(
    "/create",
    response_model=ProductCreateResponse,
    summary="Create a new product profile",
    status_code=201,
)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    """
    Create a product with all the information needed for content generation.
    Returns the new product ID.
    """
    product = Product(
        name=payload.name,
        category=payload.category,
        description=payload.description,
        features=json.dumps(payload.features),
        problem_solved=payload.problem_solved,
        target_audience=payload.target_audience,
        price=payload.price,
        platform=payload.platform,
        tone=payload.tone,
        requirements=payload.requirements,
    )
    db.add(product)
    db.commit()
    db.refresh(product)

    logger.info("Product created: id=%d name='%s'", product.id, product.name)
    return ProductCreateResponse(id=product.id, message="Product created successfully")


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Get product by ID",
)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Return complete product information by ID."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")

    return ProductResponse(
        id=product.id,
        name=product.name,
        category=product.category,
        description=product.description,
        features=product.features_list,
        problem_solved=product.problem_solved,
        target_audience=product.target_audience,
        price=product.price,
        platform=product.platform,
        tone=product.tone,
        requirements=product.requirements,
        created_at=product.created_at,
    )
