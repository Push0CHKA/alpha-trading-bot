from datetime import datetime

from sqlalchemy import Column, DateTime, func


class CreatedDateMixin:
    """Время создания"""

    created_date = Column(
        DateTime, default=datetime.now, server_default=func.now()
    )
