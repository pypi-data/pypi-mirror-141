
from notecron.center.app import db


class JobLog(db.Model):
    __tablename__ = 'job_log'
    id = db.Column(db.Integer, primary_key=True)
    log_id = db.Column(db.String(65), nullable=False, index=True,
                       server_default='', default='log id 用uuid生成唯一id,用来用户更新')
    cron_info_id = db.Column(db.Integer, nullable=False, default=0, index=True)
    content = db.Column(db.TEXT, nullable=False, default='', doc='返回的内容')
    create_time = db.Column(db.String(25), nullable=False, default='')
    take_time = db.Column(db.String(25), default='', doc='耗时时间')

    def to_json(self):
        return {
            'id': self.id,
            'job_id': self.job_id,
            'remark': self.remark,
            'content': self.content,
            'traces': self.traces,
            'status': self.status,
            'create_time': self.create_time
        }
