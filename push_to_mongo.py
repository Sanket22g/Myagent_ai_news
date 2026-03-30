from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pymongo import AsyncMongoClient
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import asyncio
import os

from src.crew import MyagentUdate

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(title="AI Research Digest API", version="1.0.0")

# Enable CORS (important for Android / frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
client = AsyncMongoClient(os.getenv("MONGODB_URI"))
db = client[os.getenv("MONGODB_DB")]
collection = db[os.getenv("MONGODB_COLLECTION")]

# Root API
@app.get("/")
async def root():
    return {"message": "API is working!"}


# 🔥 Run CrewAI in thread (NON-BLOCKING)
async def run_crew_async(inputs):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None,
        lambda: MyagentUdate().crew().kickoff(inputs=inputs)
    )
    return result


# 🔥 Background Task (FULLY ASYNC SAFE)
async def run_crew_and_save(inputs: dict):
    try:
        print("🚀 Starting CrewAI task...")

        # Run heavy task in background thread
        result = await run_crew_async(inputs)

        # Convert result to dict
        report_dict = result.pydantic.model_dump()

        # Add metadata
        report_dict["topic_searched"] = inputs["topic"]
        report_dict["created_at"] = datetime.now(timezone.utc)

        # Save to MongoDB
        await collection.insert_one(report_dict)

        print("✅ Data saved successfully!")

    except Exception as e:
        print(f"❌ Error in background task: {e}")


# 🔥 API to start processing
@app.post("/start_crew_save")
async def save_data(background_tasks: BackgroundTasks):
    inputs = {
        "topic": "LLM, Agentic AI, AI Updates, AI Tools, Machine Learning",
        "current_year": str(datetime.now().year),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "two_days_ago": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
    }

    # Run background task safely
    background_tasks.add_task(run_crew_and_save, inputs)

    return JSONResponse(content={
        "message": "Processing started in background 🚀",
        "status": "processing"
    })


# 🔥 Get latest reports
@app.get("/get")
async def get_data():
    try:
        cursor = collection.find().sort("_id", -1).limit(10)
        reports = await cursor.to_list(length=10)

        for report in reports:
            report["_id"] = str(report["_id"])

        return reports

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
