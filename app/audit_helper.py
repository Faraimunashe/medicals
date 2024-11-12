# audit_helpers.py
from app.models import AuditLog, db
from flask_login import current_user

def log_create(model):
    log = AuditLog(
        model_name=model.__class__.__name__,
        model_id=model.id,
        action="create",
        previous_data=None,
        new_data=model.to_dict(),
        user_id=current_user.id if current_user.is_authenticated else None
    )
    db.session.add(log)
    db.session.commit()

def log_update(model, old_data):
    log = AuditLog(
        model_name=model.__class__.__name__,
        model_id=model.id,
        action="update",
        previous_data=old_data,
        new_data=model.to_dict(),
        user_id=current_user.id if current_user.is_authenticated else None
    )
    db.session.add(log)
    db.session.commit()

def log_delete(model):
    log = AuditLog(
        model_name=model.__class__.__name__,
        model_id=model.id,
        action="delete",
        previous_data=model.to_dict(),
        new_data=None,
        user_id=current_user.id if current_user.is_authenticated else None
    )
    db.session.add(log)
    db.session.commit()
