from db_manager import update_category_type

if __name__ == "__main__":
    update_category_type("Ενοίκιο", "expense")
    print("✅ Η κατηγορία 'Ενοίκιο' ενημερώθηκε σε 'expense'.")