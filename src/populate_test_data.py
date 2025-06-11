from db_manager import add_category, get_categories, add_transaction
from datetime import datetime, timedelta
import random

# Δημιουργία βασικών κατηγοριών
categories = [
    ("Μισθός", "income"),
    ("Ενοίκιο", "expense"),  # Αλλαγή από income σε expense
    ("Φαγητό", "expense"),
    ("Διασκέδαση", "expense"),
    ("ΔΕΗ", "expense"),
    ("Καύσιμα", "expense"),
]

# Εισαγωγή κατηγοριών
existing = [c[1] for c in get_categories()]
for name, type_ in categories:
    if name not in existing:
        add_category(name, type_)

# Πάρε τα IDs
cat_dict = {name: cid for cid, name, type_ in get_categories()}

# Δημιουργία συναλλαγών
def random_date():
    base = datetime(2025, 5, 1)
    return base + timedelta(days=random.randint(0, 27))

for _ in range(5):  # Έσοδα
    add_transaction(
        amount=random.randint(800, 1500),
        date=random_date().strftime("%Y-%m-%d"),
        category_id=cat_dict.get("Μισθός"),
        description="Μισθοδοσία",
        is_recurring=1
    )

for _ in range(10):  # Έξοδα
    category = random.choice(["Φαγητό", "Διασκέδαση", "ΔΕΗ", "Καύσιμα"])
    add_transaction(
        amount=random.randint(10, 120),
        date=random_date().strftime("%Y-%m-%d"),
        category_id=cat_dict.get(category),
        description=f"Πληρωμή για {category}",
        is_recurring=0
    )

print("✅ Έγινε εισαγωγή δεδομένων!")
