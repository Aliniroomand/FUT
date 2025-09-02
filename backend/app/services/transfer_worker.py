# app/services/transfer_worker.py
import asyncio
import logging
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.transfer_task import TransferTask, TransferStatus
from time import sleep

logger = logging.getLogger("transfer_worker")

STOP_EVENT = asyncio.Event()

async def process_task(task_id: int):
    # placeholder: logic to interact with EA/FUT to buy the card
    # IMPORTANT: do not implement real credential-using code here without safeguards
    logger.info(f"Processing task {task_id}")
    # simulate attempt
    await asyncio.sleep(2)
    return {"success": False, "error": "placeholder-not-implemented"}

async def worker_loop(poll_interval: float = 5.0):
    logger.info("Worker loop started")
    while not STOP_EVENT.is_set():
        try:
            db: Session = SessionLocal()
            pending = db.query(TransferTask).filter(TransferTask.status == TransferStatus.pending).limit(5).all()
            for t in pending:
                t.status = TransferStatus.attempting
                db.commit()
                db.refresh(t)
                res = await process_task(t.id)
                if res.get("success"):
                    t.status = TransferStatus.success
                else:
                    t.attempts += 1
                    t.last_error = res.get("error")
                    t.status = TransferStatus.failed if t.attempts >= 3 else TransferStatus.pending
                db.commit()
            db.close()
        except Exception as e:
            logger.exception("Worker loop error")
        await asyncio.sleep(poll_interval)
    logger.info("Worker loop stopped")

async def start_worker(app):
    app.state.worker_task = asyncio.create_task(worker_loop())

async def stop_worker(app):
    STOP_EVENT.set()
    if hasattr(app.state, "worker_task"):
        app.state.worker_task.cancel()
        try:
            await app.state.worker_task
        except asyncio.CancelledError:
            pass
