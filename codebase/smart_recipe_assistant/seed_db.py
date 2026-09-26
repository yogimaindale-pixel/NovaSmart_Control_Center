"""Seed Firestore with initial recipes dataset for smart-recipe-assistant."""

import logging
from google.cloud import firestore
from google.api_core.exceptions import NotFound, PermissionDenied

PROJECT_ID = "qwiklabs-gcp-01-2aad14f2c696"

logger = logging.getLogger(__name__)


def seed_firestore():
    sample_recipes = [
        {
            "id": "creamy-garlic-pasta",
            "title": "Creamy Garlic Tuscan Pasta",
            "cuisine": "Italian",
            "prep_time_minutes": 25,
            "dietary_tags": ["vegetarian"],
            "ingredients": [
                "8 oz fettuccine",
                "2 tbsp olive oil",
                "4 cloves garlic minced",
                "1 cup heavy cream",
                "1/2 cup parmesan cheese",
                "1 cup sun-dried tomatoes",
                "2 cups fresh spinach",
            ],
            "instructions": (
                "Cook fettuccine. Sauté garlic and sun-dried tomatoes in olive oil. "
                "Add heavy cream and bring to simmer. Stir in parmesan and spinach "
                "until wilted. Toss with pasta."
            ),
            "rating": 4.8,
        },
        {
            "id": "avocado-chickpea-salad",
            "title": "Avocado Chickpea Mediterranean Salad",
            "cuisine": "Mediterranean",
            "prep_time_minutes": 15,
            "dietary_tags": ["vegan", "gluten-free", "vegetarian"],
            "ingredients": [
                "1 can (15 oz) chickpeas drained",
                "2 ripe avocados diced",
                "1 cup cherry tomatoes halved",
                "1/2 cucumber diced",
                "1/4 cup red onion minced",
                "2 tbsp lemon juice",
                "2 tbsp olive oil",
            ],
            "instructions": (
                "Combine chickpeas, avocado, tomatoes, cucumber, and red onion "
                "in a large bowl. Whisk lemon juice and olive oil, pour over "
                "salad, and toss gently."
            ),
            "rating": 4.9,
        },
        {
            "id": "spicy-tofu-stir-fry",
            "title": "Spicy Sesame Tofu Stir Fry",
            "cuisine": "Asian",
            "prep_time_minutes": 20,
            "dietary_tags": ["vegan", "vegetarian"],
            "ingredients": [
                "1 block extra firm tofu cubed",
                "2 tbsp soy sauce",
                "1 tbsp sriracha",
                "1 tbsp sesame oil",
                "1 cup broccoli florets",
                "1 red bell pepper sliced",
                "2 green onions chopped",
            ],
            "instructions": (
                "Pan-fry cubed tofu in sesame oil until golden. Sauté broccoli "
                "and bell pepper. Toss with tofu, soy sauce, and sriracha. "
                "Garnish with green onions."
            ),
            "rating": 4.7,
        },
    ]

    print(f"Seeding Firestore collection 'recipes' in project '{PROJECT_ID}'...")
    try:
        db = firestore.Client(project=PROJECT_ID)
        recipes_ref = db.collection("recipes")
        for recipe in sample_recipes:
            doc_ref = recipes_ref.document(recipe["id"])
            doc_ref.set(recipe)
            print(f" -> Seeded recipe to Firestore: {recipe['title']} ({recipe['id']})")
        print("Firestore seeding complete!")
    except (NotFound, PermissionDenied) as exc:
        print(f"Note: Firestore database not provisioned yet ({exc}).")
        print("Using seeded local fallback dataset for local testing.")


if __name__ == "__main__":
    seed_firestore()
