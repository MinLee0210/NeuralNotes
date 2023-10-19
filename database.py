from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

class MongoDB:
    @classmethod
    async def init(cls, host, database_name):
        client = AsyncIOMotorClient(host)
        await init_beanie(
            database=AsyncIOMotorDatabase(client, database_name),
            document_models=["models.user.UserInfo",
                             "models.feedback.Comment",
                             "models.feedback.Rating"],
        )