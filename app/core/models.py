import uuid
from datetime import datetime

import ormar


class AppBaseModel(object):
    id: uuid.UUID = ormar.UUID(default=uuid.uuid4, primary_key=True)
    created_at = ormar.DateTime(default=datetime.now)
    updated_at = ormar.DateTime(nullable=True)
