from Codes.base_code import BaseCodes
from Codes.task_code import TaskCodes

def test_task_operations(driver):
    base = BaseCodes(driver)
    task_page = TaskCodes(driver)

    base.open("https://todomvc.com/examples/react/dist/")

    # Add 3 tasks
    tasks = ["Search Product", "Add to Cart", "Checkout"]
    for task in tasks:
        task_page.add_task(task)
    assert task_page.get_task_texts() == tasks

    # Mark the second task (index 1) as complete
    task_page.complete_task(1)
    assert task_page.is_task_completed(1)

    # Delete the first task (index 0)
    task_page.delete_task(0)
    updated_tasks = ["Add to Cart", "Checkout"]
    assert task_page.get_task_texts() == updated_tasks

    # Validate task completion state
    assert task_page.is_task_completed(0)  # "Add to Cart"
    assert not task_page.is_task_completed(1)  # "Checkout"
