import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.services.route_scorer import score_route
import polyline

# Setup DB connection
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/safepulse"
engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def test():
    # Lonavala coordinates: approx 18.7537, 73.4068
    # Let's create a dummy route near there
    points = [(18.7537, 73.4068), (18.7550, 73.4100)]
    encoded = polyline.encode(points)
    
    async with AsyncSessionLocal() as session:
        score = await score_route(encoded, session)
        print(f"Risk score: {score.route_risk_score}")
        print(f"Recommendation: {score.recommendation}")
        print(f"High risk segments: {score.high_risk_segments}")

if __name__ == "__main__":
    asyncio.run(test())
