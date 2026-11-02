import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database.connection import get_db
from ..database.models import Conversation, Message
from ..schemas.history import ConversationSummary, ConversationDetail, MessageItem

router = APIRouter(prefix="/history", tags=["Conversation History"])

@router.get("", response_model=List[ConversationSummary])
def get_conversations(db: Session = Depends(get_db)):
    """Retrieves list of past conversations with message counts and timestamps."""
    convs = db.query(Conversation).order_by(Conversation.updated_at.desc()).all()
    result = []
    for c in convs:
        result.append(ConversationSummary(
            id=c.id,
            title=c.title,
            language=c.language,
            message_count=len(c.messages),
            created_at=c.created_at,
            updated_at=c.updated_at
        ))
    return result

@router.get("/{conversation_id}", response_model=ConversationDetail)
def get_conversation_detail(conversation_id: str, db: Session = Depends(get_db)):
    """Retrieves a complete conversation including its messages and answers."""
    conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found.")
    
    messages = [
        MessageItem(
            id=m.id,
            sender=m.sender,
            text=m.text,
            audio_url=m.audio_url,
            intent=m.intent,
            sources_used=m.sources_used,
            created_at=m.created_at
        )
        for m in conv.messages
    ]

    return ConversationDetail(
        id=conv.id,
        title=conv.title,
        language=conv.language,
        messages=messages,
        created_at=conv.created_at,
        updated_at=conv.updated_at
    )

@router.delete("/{conversation_id}")
def delete_conversation(conversation_id: str, db: Session = Depends(get_db)):
    """Deletes a conversation and its messages."""
    conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found.")
    db.delete(conv)
    db.commit()
    return {"status": "success", "message": "Conversation deleted successfully."}

@router.delete("")
def clear_all_history(db: Session = Depends(get_db)):
    """Clears all conversation history."""
    db.query(Message).delete()
    db.query(Conversation).delete()
    db.commit()
    return {"status": "success", "message": "All conversations cleared."}

