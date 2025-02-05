import logging
from typing import Dict, List
from fastapi import Body, FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import firestore
import os
from dotenv import load_dotenv

from agent import MistralAgent

# Check if running locally (Cloud Run sets ENVIRONMENT to "production" by default)
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Load the correct .env file
if ENVIRONMENT == "development":
    print("🔧 Loading local environment variables from .env.local")
    load_dotenv(".env.local")
else:
    print("🚀 Running in production mode, loading .env")
    load_dotenv(".env")

# Now, environment variables are accessible
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "").split(",")


app = FastAPI()

# Apply CORS settings dynamically
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Setup logging
logger = logging.getLogger("server")

# Initialize Firestore Client
db = firestore.Client()


# Load AI agent
agent = MistralAgent()


class CreateRecipeRequest(BaseModel):
    prompt: str


class MessageRequest(BaseModel):
    author: str
    content: str


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

    @classmethod
    def from_firestore(cls, data: dict) -> "Recipe":
        """Converts Firestore raw data into a Recipe model."""
        if "ingredients" in data:
            data["ingredients"] = {
                key: Ingredient(**value) for key, value in data["ingredients"].items()
            }
        return cls(**data)


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
def get_recipe(id: str):
    """Retrieves a recipe from Firestore by ID and returns it as a `Recipe` model."""
    logger.info(f"Fetching recipe with ID: {id}")

    try:
        doc_ref = db.collection("recipe").document(id)
        doc = doc_ref.get()

        if not doc.exists:
            raise HTTPException(status_code=404, detail="Recipe not found")

        return Recipe.from_firestore(doc.to_dict())

    except Exception as e:
        logger.error(f"Error fetching recipe {id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/recipe/create", response_model=dict)
async def create_recipe_from_prompt(request: CreateRecipeRequest):
    """Creates a recipe from user input and stores it in Firestore."""
    logger.info(f"Generating recipe for prompt: {request.prompt}")

    try:
        # Generate recipe using the AI agent
        generated_recipe = await agent.create_recipe(request.prompt)

        # Ensure recipe follows the correct schema
        recipe_data = Recipe(**generated_recipe).model_dump()

        # Store in Firestore
        doc_ref = db.collection("recipe").add(recipe_data)
        recipe_id = doc_ref[1].id

        logger.info(f"Recipe created successfully with ID: {recipe_id}")

        return {"message": "Recipe created successfully", "recipe_id": recipe_id}

    except Exception as e:
        logger.error(f"Error creating recipe from prompt: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/recipe", response_model=dict)
def create_recipe(recipe: Recipe = Body(...)):
    """Creates a new recipe and stores it in Firestore."""
    logger.info(f"Creating a new recipe: {recipe.name}")

    try:
        doc_ref = db.collection("recipe").add(recipe.model_dump())
        recipe_id = doc_ref[1].id

        return {"message": "Recipe created successfully", "id": recipe_id}

    except Exception as e:
        logger.error(f"Error creating recipe: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/recipes", response_model=List[Dict[str, str]])
def list_recipes():
    """Retrieves a list of all recipes with their ID, name, and summary from Firestore."""
    logger.info("Fetching all recipes with ID, name, and summary")

    try:
        # Query Firestore for all documents in the 'recipe' collection
        recipes = db.collection("recipe").stream()

        # Extract the required fields
        recipe_list = [
            {
                "id": doc.id,
                "name": doc.to_dict().get("name", "Unnamed Recipe"),
                "summary": doc.to_dict().get("summary", "No summary available"),
                "difficulty": doc.to_dict().get("difficulty", "Unknown"),
                "prep_time": str(doc.to_dict().get("prep_time", 0)),
                "cook_time": str(doc.to_dict().get("cook_time", 0)),
            }
            for doc in recipes
        ]

        return recipe_list

    except Exception as e:
        logger.error(f"Error fetching recipes: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
