# Includes

## URLs

- **GET**: Takes the ID of a transaction in the path and returns the JSON of the transaction.
- **POST**: Takes JSON data as input and an ID in the path to create a transaction. (To attach a parent, include `parent_id` as one parameter.)
- **SUM**: Sums up all nodes and child node amounts. (How we are doing it will be explained later.)
- **TYPE**: Returns an array of transactions filtered by type from the path.

## View

Contains all the logic for the above requests.

## Test Class

Tests all the above logic with a few edge case checks.

## How to Run

1. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2. **Apply migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

3. **Run tests:**
    ```bash
    python manage.py test transaction_service
    ```

4. **Start the server:**
    ```bash
    python manage.py runserver
    ```

## Admin

Admin is available to add, delete, view, and manipulate data in the transaction table.

- To create an admin user:
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to enter:
    - Name
    - Email
    - Password
    - Confirm Password

## Note

### Logic for Sum of Transaction

**Assumption:** As the data is for transactions, it generally doesn’t get updated after creation and deletion. (However, this can be handled.)

- We have another field called `transaction_sum`.
- Whenever a transaction with a parent is added:
    - Post-save signals are triggered to add the amount to the parent.
    - It also recursively adds the amount to all ancestors.

**Benefits:**

- Whenever the sum API is called, it won’t take time to calculate the sum by traversing multiple transactions.
- Recursive calls can be made as async calls post-save, so they won’t affect the existing processing and will work with very low latency.

