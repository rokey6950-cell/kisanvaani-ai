import uuid
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.database.connection import Base
from backend.app.database.models import Conversation, Message

TEST_DB_URL = "sqlite:///:memory:"

@pytest.fixture
def db_session():
    engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()

def test_conversation_and_message_crud(db_session):
    # 1. Create conversation
    conv_id = str(uuid.uuid4())
    conv = Conversation(
        id=conv_id,
        title="गेहूं में रोग की जानकारी",
        language="hi"
    )
    db_session.add(conv)
    db_session.commit()

    # 2. Add farmer message
    msg1 = Message(
        id=str(uuid.uuid4()),
        conversation_id=conv_id,
        sender="farmer",
        text="गेहूं में पीला रतुआ कैसे पहचानें?",
        intent="disease_inquiry"
    )
    # 3. Add assistant response
    msg2 = Message(
        id=str(uuid.uuid4()),
        conversation_id=conv_id,
        sender="assistant",
        text="पत्तियों पर पीले रंग की पाउडरनुमा धारियां दिखना पीला रतुआ का मुख्य लक्षण है।",
        intent="disease_diagnosis",
        sources_used=[{"source_id": "src-hau-pop-001"}]
    )
    db_session.add_all([msg1, msg2])
    db_session.commit()

    # 4. Verify relations
    retrieved_conv = db_session.query(Conversation).filter(Conversation.id == conv_id).first()
    assert retrieved_conv is not None
    assert len(retrieved_conv.messages) == 2
    assert retrieved_conv.messages[0].sender == "farmer"
    assert retrieved_conv.messages[1].sender == "assistant"

    # 5. Verify Cascade Delete
    db_session.delete(retrieved_conv)
    db_session.commit()

    remaining_messages = db_session.query(Message).filter(Message.conversation_id == conv_id).all()
    assert len(remaining_messages) == 0

