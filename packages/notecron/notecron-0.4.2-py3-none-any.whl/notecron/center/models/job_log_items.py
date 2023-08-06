from notecron.center.app import db
from sqlalchemy import Column


class JobLogItems(db.Model):
    __tablename__ = 'job_log_items'
    id: Column = db.Column(db.Integer, primary_key=True)
    log_id: Column = db.Column(db.String(65), index=True, nullable=False)
    content: Column = db.Column(db.TEXT, nullable=False, default='')
