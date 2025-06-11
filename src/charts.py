import matplotlib.pyplot as plt
from db_manager import connect

def plot_expenses_by_category(year, month):
    conn = connect()
    cursor = conn.cursor()

    query = """
    SELECT c.name, SUM(t.amount)
    FROM transactions t
    JOIN categories c ON t.category_id = c.id
    WHERE strftime('%Y', date) = ? AND strftime('%m', date) = ? AND c.type = 'expense'
    GROUP BY c.name
    """

    cursor.execute(query, (str(year), f"{month:02d}"))
    results = cursor.fetchall()
    conn.close()

    if not results:
        print("Καμία εγγραφή για εμφάνιση.")
        return

    categories = [row[0] for row in results]
    totals = [row[1] for row in results]

    plt.figure(figsize=(10, 5))
    plt.bar(categories, totals)
    plt.xlabel("Κατηγορία Εξόδων")
    plt.ylabel("Συνολικό Ποσό (€)")
    plt.title(f"Έξοδα ανά κατηγορία - {month:02d}/{year}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
