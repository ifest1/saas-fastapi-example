import ormar
import uuid


class Tenant(ormar.Model):
    id: uuid.UUID = ormar.UUID(default=uuid.uuid4, primary_key=True)
    name: str = ormar.String(max_length=50)
