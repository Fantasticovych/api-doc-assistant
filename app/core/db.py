import logging
from prisma import Prisma
from fastapi import FastAPI
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)

db = Prisma()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting database connection...")
    await db.connect()
    logger.info("Database connected successfully.")

    yield

    logger.info("Closing database connection...")
    await db.disconnect()
    logger.info("Database disconnected.")
