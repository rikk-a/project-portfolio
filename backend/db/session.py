from contextlib import contextmanager

from db.base import db


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    try:
        yield db.session
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise