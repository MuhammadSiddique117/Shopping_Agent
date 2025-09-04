from agents import Agent, Runner, function_tool
import requests
from connection import config, model
import rich

# ---------------------------
# Function Tool: Get Products
# ---------------------------
@function_tool
def get_products(max_price: float = None, sort_by: str = None):
    """
    Fetches a list of products from the API with optional filtering & sorting.

    Args:
        max_price (float, optional): Maximum price to filter products.
        sort_by (str, optional): Sort criteria. Options: "newest", "discount".
    """
    url = "https://template6-six.vercel.app/api/products"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        products = data.get("products", data) if isinstance(data, dict) else data

        # Filter by price
        if max_price is not None:
            products = [p for p in products if p.get("price", 0) <= max_price]

        # Sorting
        if sort_by == "newest":
            products = sorted(products, key=lambda p: p.get("isNew", False), reverse=True)
        elif sort_by == "discount":
            products = sorted(products, key=lambda p: p.get("discountPercentage", 0), reverse=True)

        return [
            {
                "title": p.get("title"),
                "price": p.get("price"),
                "discount": p.get("discountPercentage"),
                "category": ", ".join(p.get("tags", [])),
                "isNew": p.get("isNew"),
                "description": p.get("description")
            }
            for p in products
        ]
    except requests.RequestException as e:
        return {"error": f"Failed to fetch products: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

# ---------------------------
# Define Shopping Agent
# ---------------------------
agent = Agent(
    name="Shopping Agent",
    instructions="""
    You are a helpful shopping assistant.
    Use the product list from the API to recommend products based on the user's query.
    You can filter by price or sort by newest/discount.
    """,
    tools=[get_products],
    model=model
)

# ---------------------------
# Interactive Chatbot Mode
# ---------------------------
def run_chatbot():
    rich.print("[bold green]🛒 Welcome to the Smart Shopping Assistant![/bold green]")
    rich.print("Type your shopping query (or 'exit' to quit)\n")

    while True:
        query = input("🧑 You: ")
        if query.lower() in ["exit", "quit"]:
            rich.print("[red]👋 Goodbye![/red]")
            break

        result = Runner.run_sync(agent, input=query, run_config=config)
        rich.print(f"[yellow]🤖 Agent:[/yellow] {result.final_output}")

# Run chatbot
if __name__ == "__main__":
    run_chatbot()
