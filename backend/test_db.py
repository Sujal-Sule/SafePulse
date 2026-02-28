import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, func, text
from app.models import RiskZone
from app.config.settings import get_settings

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/safepulse"
engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def test():
    settings = get_settings()
    async with AsyncSessionLocal() as session:
        # 1. Fetch all risk zones
        print("--- Active Risk Zones ---")
        stmt = select(RiskZone).where(RiskZone.active == True)
        res = await session.execute(stmt)
        zones = res.scalars().all()
        for z in zones:
            print(f"Zone: {z.id}, score: {z.risk_score}")

        # 2. Test intersection with a known polyline 
        # (This is a short line segment through roughly 73.40, 18.75)
        coords = [(18.7537, 73.4068), (18.7580, 73.4150)]
        line_wkt = "LINESTRING(" + ", ".join([f"{c[1]} {c[0]}" for c in coords]) + ")"
        
        stmt2 = select(RiskZone).where(
            RiskZone.active == True,
            func.ST_DWithin(
                RiskZone.centroid,
                func.ST_GeogFromText(line_wkt),
                settings.RISK_CLUSTER_RADIUS_M
            )
        )
        res2 = await session.execute(stmt2)
        intersecting = res2.scalars().all()
        
        print(f"\n--- Intersecting Zones (Radius: {settings.RISK_CLUSTER_RADIUS_M}m) ---")
        for z in intersecting:
            print(f"Intersecting: {z.id} ({z.risk_level})")
            
        if not intersecting:
            print("No intersections found for test route.")

if __name__ == "__main__":
    asyncio.run(test())
