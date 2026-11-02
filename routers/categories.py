from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from dependencies import get_db, get_current_user
from schemas import categories
from models.categories import Categories

router = APIRouter()


@router.post("/create_category", response_model=categories.FetchCategory)
def create_category(
    new_cat: categories.CreateCategory,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    alr_category = db.query(Categories).filter(
        Categories.category_name == new_cat.category_name,
        Categories.user_id == user.id
    ).first()

    if alr_category:
        raise HTTPException(status_code=409, detail="Category already exists.")

    category = Categories(
        category_name=new_cat.category_name,
        user_id=user.id
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


@router.get("/categories", response_model=list[categories.FetchCategory])
def see_categories(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Categories).filter(
        Categories.user_id == user.id
    ).all()


@router.delete("/delete_category/{category_id}")
def delete_category(
    category_id: int,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    category = db.query(Categories).filter(
        Categories.category_id == category_id,
        Categories.user_id == user.id
    ).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found.")

    db.delete(category)
    db.commit()

    return {"detail": "Category deleted successfully."}