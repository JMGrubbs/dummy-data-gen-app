async def process_data_gen_task_async(task_id: int) -> None:
    # 1. Load DataGenTask from Postgres.
    # 2. Mark it as in progress.
    # 3. Call your provider with await.
    # 4. Save generated data and completion/failure state.
    print(f"Processing data generation task {task_id}")
