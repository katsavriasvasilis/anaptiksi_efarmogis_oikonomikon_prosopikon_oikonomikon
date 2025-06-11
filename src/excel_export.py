import xlsxwriter
from db_manager import connect

def export_month_to_excel(year, month, filename="export.xlsx"):
    conn = connect()
    cursor = conn.cursor()

    query = """
    SELECT t.date, c.name, c.type, t.amount, t.description
    FROM transactions t
    JOIN categories c ON t.category_id = c.id
    WHERE strftime('%Y', t.date) = ? AND strftime('%m', t.date) = ?
    ORDER BY t.date ASC
    """
    cursor.execute(query, (str(year), f"{month:02d}"))
    records = cursor.fetchall()
    conn.close()

    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet("Συναλλαγές")

    headers = ["Ημερομηνία", "Κατηγορία", "Τύπος", "Ποσό", "Περιγραφή"]
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)

    for row, record in enumerate(records, start=1):
        for col, value in enumerate(record):
            worksheet.write(row, col, value)

    workbook.close()
