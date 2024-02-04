### Credit Approval System 

```markdown
## API Endpoints

### Register User
- **URL:** `/register/`
- **Method:** POST
- **Description:** Register a new user.
- **Request Body:**
  ```json
  {
    "first_name": "John",
    "last_name": "Doe",
    "age": 30,
    "phone_number": "1234567890",
    "monthly_income": 5000
  }
  ```
- **Response:**
  ```json
  {
    "customer_id": 2131312,
    "name": "John Doe",
    "age": 30,
    "phone_number": "1234567890",
    "monthly_income": 5000,
    "approved_limit": 900000,
  }
  ```

### Check Eligibility
- **URL:** `/check-eligibility/`
- **Method:** POST
- **Description:** Checks if a customer is eligible for a loan.
- **Request Body:**
  ```json
  {
    "customer_id": 1,
    "loan_amount": 10000,
    "interest_rate": 8,
    "tenure": 12
  }
  ```
- **Response:**
  ```json
  {
    "customer_id": 1,
    "eligible": true,
    "interest_rate": 8,
    "corrected_interest_rate": 8,
    "tenure": 12,
    "monthly_installment": 950
  }
  ```

### Create Loan
- **URL:** `/create-loan/`
- **Method:** POST
- **Description:** Create a new loan for a customer.
- **Request Body:**
  ```json
  {
    "customer_id": 1,
    "loan_amount": 10000,
    "interest_rate": 8,
    "tenure": 12
  }
  ```
- **Response:**
  ```json
    {
    "loan_id": 10007,
    "customer_id": 299,
    "loan_approved": true,
    "message": "Loan approved by authority",
    "monthly_installment": 833.
    }
  ```

### View Loan
- **URL:** `/view-loan/<int:loan_id>/`
- **Method:** GET
- **Description:** Check the information of a specific loan.
- **Response:**
  ```json
  {
    "loan_id": 10007,
    "customer": {
        "first_name": "Argelia",
        "last_name": "Saavedra",
        "phone_number": "9614182220",
        "age": 30
    },
    "loan_amount": 5000.0,
    "interest_rate": 2.0,
    "tenure": 50,
    "monthly_installment": 833
    }
  ```

### View Loans
- **URL:** `/view-loans/<int:customer_id>/`
- **Method:** GET
- **Description:** See the loans of a specific customer.
- **Response:**
  ```json
  {
    "loan_id": 10007,
    "customer": {
        "first_name": "Argelia",
        "last_name": "Saavedra",
        "phone_number": "9614182220",
        "age": 30
    },
    "loan_amount": 5000.0,
    "interest_rate": 2.0,
    "tenure": 50,
    "monthly_installment": 833.70
    }
  ```

Author: Hossain Chisty(Backend Developer)
<br>
Contact: hossain.chisty11@gmail.com
<br>
Github: https://github.com/hossainchisty
