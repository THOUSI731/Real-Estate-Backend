
## Features
- Fully Customized APIView
- Search Based on Many to Many field of Features Table (for Property & Property Units)
- Tenant and Admin Authentication
- Optimized ORM Queries
- Documented API by Swagger (drf-yasg)

##  Instructions to Run the Code


1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/THOUSI731/Real-Estate-Backend.git
   cd <project_directory>

2. Create a Virtual Environment:

   ```bash
    python -m venv venv
    #for windows
    venv\Scripts\activate

3. Install Dependencies:

    ```bash
    pip install -r requirements.txt

5. Create SuperUser and Runserver;

    ```bash
    python manage.py makemigrations
    python manage.py migrate    
    python manage.py createsuperuser
    python manage.py runserver
6. For Api Documentation
    ```bash
    http://localhost:8000/swagger/
