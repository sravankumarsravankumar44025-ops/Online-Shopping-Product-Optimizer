from flask import Flask, render_template, request

app = Flask(__name__)


# =========================================================
# PRODUCT DATA
# =========================================================

products = [
    {
        "id": 1,
        "name": "Laptop",
        "price": 60000,
        "value": 95,
        "rating": 4.7,
        "image": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=600&q=80"
    },
    {
        "id": 2,
        "name": "Smartphone",
        "price": 30000,
        "value": 90,
        "rating": 4.5,
        "image": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=600&q=80"
    },
    {
        "id": 3,
        "name": "Headphones",
        "price": 5000,
        "value": 70,
        "rating": 4.3,
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&q=80"
    },
    {
        "id": 4,
        "name": "Smart Watch",
        "price": 8000,
        "value": 75,
        "rating": 4.2,
        "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&q=80"
    },
    {
        "id": 5,
        "name": "Keyboard",
        "price": 2500,
        "value": 50,
        "rating": 4.1,
        "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=600&q=80"
    },
    {
        "id": 6,
        "name": "Mouse",
        "price": 1500,
        "value": 40,
        "rating": 4.0,
        "image": "https://images.unsplash.com/photo-1527814050087-3793815479db?w=600&q=80"
    },
    {
        "id": 7,
        "name": "Tablet",
        "price": 20000,
        "value": 85,
        "rating": 4.4,
        "image": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=600&q=80"
    },
    {
        "id": 8,
        "name": "Speaker",
        "price": 4000,
        "value": 60,
        "rating": 4.2,
        "image": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=600&q=80"
    }
]


# =========================================================
# 0/1 KNAPSACK
# =========================================================

def knapsack(items, budget):

    n = len(items)

    # Convert rupees into thousands
    capacity = budget // 1000

    # DP table
    dp = [[0] * (capacity + 1)
          for _ in range(n + 1)]

    comparisons = 0

    # Build DP table
    for i in range(1, n + 1):

        price = items[i - 1]["price"] // 1000
        value = items[i - 1]["value"]

        for b in range(capacity + 1):

            comparisons += 1

            if price <= b:

                dp[i][b] = max(
                    dp[i - 1][b],
                    value + dp[i - 1][b - price]
                )

            else:

                dp[i][b] = dp[i - 1][b]

    # Find selected products
    selected = []

    b = capacity

    for i in range(n, 0, -1):

        if dp[i][b] != dp[i - 1][b]:

            selected.append(items[i - 1])

            b -= items[i - 1]["price"] // 1000

    selected.reverse()

    total_price = sum(
        item["price"] for item in selected
    )

    total_value = sum(
        item["value"] for item in selected
    )

    return selected, total_price, total_value, comparisons


# =========================================================
# SORTING
# =========================================================

def sort_products(items, sort_by):

    if sort_by == "price":

        return sorted(
            items,
            key=lambda x: x["price"]
        )

    elif sort_by == "rating":

        return sorted(
            items,
            key=lambda x: x["rating"],
            reverse=True
        )

    elif sort_by == "value":

        return sorted(
            items,
            key=lambda x: x["value"],
            reverse=True
        )

    return items


# =========================================================
# BINARY SEARCH
# =========================================================

def binary_search(items, target):

    low = 0
    high = len(items) - 1

    comparisons = 0
    steps = []

    while low <= high:

        mid = (low + high) // 2

        comparisons += 1

        steps.append(
            f"Step {comparisons}: Checking {items[mid]['name']}"
        )

        current = items[mid]["name"].lower()
        target = target.lower()

        if current == target:

            return items[mid], comparisons, steps

        elif current < target:

            low = mid + 1

        else:

            high = mid - 1

    return None, comparisons, steps


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/", methods=["GET", "POST"])
def home():

    display_products = products.copy()

    selected_products = []

    total_price = 0
    total_value = 0
    knapsack_comparisons = 0

    search_result = None
    search_comparisons = 0
    search_steps = []

    message = ""

    if request.method == "POST":

        action = request.form.get("action")

        # -----------------------------------------
        # KNAPSACK
        # -----------------------------------------

        if action == "optimize":

            budget = int(
                request.form.get("budget", 0)
            )

            if budget > 0:

                (
                    selected_products,
                    total_price,
                    total_value,
                    knapsack_comparisons
                ) = knapsack(products, budget)

            else:

                message = "Please enter a valid budget."

        # -----------------------------------------
        # SORTING
        # -----------------------------------------

        elif action == "sort":

            sort_by = request.form.get(
                "sort_by",
                "value"
            )

            display_products = sort_products(
                products,
                sort_by
            )

        # -----------------------------------------
        # BINARY SEARCH
        # -----------------------------------------

        elif action == "search":

            search_name = request.form.get(
                "search",
                ""
            )

            sorted_products = sorted(
                products,
                key=lambda x: x["name"].lower()
            )

            (
                search_result,
                search_comparisons,
                search_steps
            ) = binary_search(
                sorted_products,
                search_name
            )

            if search_result is None:

                message = "Product not found."

    return render_template(
        "index.html",
        products=display_products,
        selected=selected_products,
        total_price=total_price,
        total_value=total_value,
        knapsack_comparisons=knapsack_comparisons,
        search_result=search_result,
        search_comparisons=search_comparisons,
        search_steps=search_steps,
        message=message
    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(debug=True)