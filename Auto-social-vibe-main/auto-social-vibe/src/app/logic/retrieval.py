def create_retriever(db, k: int = 2):
    return db.as_retriever(search_kwargs={"k": k})
