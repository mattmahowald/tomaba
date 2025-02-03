import logging
from typing import Dict, List
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


from tomaba.agent import MistralAgent

# Setup logging
logger = logging.getLogger("server")

# Initialize FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


# Load AI agent
agent = MistralAgent()


class MessageRequest(BaseModel):
    author: str
    content: str


# Define Recipe Schema
class Ingredient(BaseModel):
    quantity: str
    unit: str


class Recipe(BaseModel):
    name: str
    ingredients: Dict[str, Ingredient]
    steps: List[str]
    prep_time: int
    cook_time: int
    servings: int
    cuisine: str
    summary: str
    difficulty: str


# Static Recipe Data
recipe_data = Recipe(
    name="Spaghetti Carbonara",
    ingredients={
        "spaghetti": {"quantity": "200", "unit": "g"},
        "eggs": {"quantity": "2", "unit": "pcs"},
        "parmesan cheese": {"quantity": "50", "unit": "g"},
        "pancetta": {"quantity": "100", "unit": "g"},
        "black pepper": {"quantity": "1", "unit": "tsp"},
    },
    steps=[
        "Boil spaghetti until al dente.",
        "Fry pancetta until crispy.",
        "Mix eggs and cheese together.",
        "Combine spaghetti with pancetta and egg mixture.",
        "Season with black pepper and serve.",
    ],
    prep_time=10,
    cook_time=15,
    servings=2,
    cuisine="Italian",
    summary="Classic Italian pasta dish with creamy egg-based sauce.",
    difficulty="Medium",
)


@app.get("/")
def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "Tomaba Discord bot server is running!"}


@app.get("/healthz")
def healthz():
    """Health check endpoint."""
    return {"status": "ok", "message": "Tomaba Discord bot server is running!"}


@app.post("/chat")
async def chat(request: MessageRequest):
    """Processes incoming messages from the bot and returns a response."""
    logging.info(f"Server processing message: {request}")

    # TODO: This is where we will do handling to determine what kind of message
    # is being sent and then call the appropriate agent function

    response = await agent.create_recipe(request.content)

    logger.info(f"Response: {response}")

    # TODO: Eventually, the response will be a recipe with a lot of information
    # in JSON structure. We'll need to parse the message for what to send back
    # to the Discord channel, as well as what to store in the database.

    return {"response": response}


@app.get("/recipe/{id}", response_model=Recipe)
def get_recipe(id: int):
    """Retrieves a recipe by ID, but excludes the ID in the response."""
    logger.info(f"Fetching recipe with ID: {id}")

    return recipe_data


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
