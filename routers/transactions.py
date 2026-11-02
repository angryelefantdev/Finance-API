from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from dependencies import get_db, get_current_user
from schemas.transactions import FetchTransaction,CreateTransaction,UpdateTransaction
from models.categories import Categories
from models.transactions import Transactions

router = APIRouter()

@router.post("/transactions",response_model=FetchTransaction)
def create_transaction(createtrans:CreateTransaction,user = Depends(get_current_user),db:Session = Depends(get_db)):
    category = db.query(Categories).filter(
    Categories.category_id == createtrans.category_id,
    Categories.user_id == user.id
).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    transaction = Transactions(
        amount = createtrans.amount,
        type = createtrans.type,
        description = createtrans.description,
        date = createtrans.date
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction

@router.get("/transactions",response_model=list[FetchTransaction])
def see_transaction_history(user = Depends(get_current_user),db:Session = Depends(get_db)):
    return db.query(Transactions).filter(
        Transactions.user_id == user.id
    ).all()

@router.get("/transaction{transaction_id}",response_model=FetchTransaction)
def get_specific_transaction(transaction_id:int,user = Depends(get_current_user),db:Session = Depends(get_db)):
    transac = db.query(Transactions).filter(
        Transactions.transaction_id == transaction_id,
        Transactions.user_id == user.id
    ).first()

    if transac is None:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return transac

@router.delete("/transaction{transaction_id}")
def delete_transaction(transaction_id:int,user = Depends(get_current_user),db:Session = Depends(get_db)):
    transac = db.query(Transactions).filter(
        Transactions.transaction_id == transaction_id,
        Transactions.user_id == user.id
    ).first()

    if transac is None:
        raise HTTPException(status_code=404, detail="Transaction not found")

    db.delete(transac)
    db.commit()
    return {"message":"Deleted transaction."}


@router.patch("/transactions/{transaction_id}", response_model=FetchTransaction)
def update_transaction(
    transaction_id: int,
    updates: UpdateTransaction,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    transac = db.query(Transactions).filter(
        Transactions.transaction_id == transaction_id,
        Transactions.user_id == user.id
    ).first()

    if transac is None:
        raise HTTPException(status_code=404, detail="Transaction not found")

    changes = updates.model_dump(exclude_unset=True)

    if not changes:
        raise HTTPException(status_code=400, detail="No fields provided")

    # If category_id is changing, verify that the category belongs to this user.
    if "category_id" in changes:
        category = db.query(Categories).filter(
            Categories.category_id == changes["category_id"],
            Categories.user_id == user.id
        ).first()

        if category is None:
            raise HTTPException(status_code=404, detail="Category not found")

    for field, value in changes.items():
        setattr(transac, field, value)

    db.commit()
    db.refresh(transac)

    return transac


