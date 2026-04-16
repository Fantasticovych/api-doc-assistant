from prisma import Prisma
from fastapi import FastAPI
from contextlib import asynccontextmanager

db = Prisma()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting database connection...")
    await db.connect()
    print("Database connected successfully.")

    yield

    print("Closing database connection...")
    await db.disconnect()
    print("Database disconnected.")
