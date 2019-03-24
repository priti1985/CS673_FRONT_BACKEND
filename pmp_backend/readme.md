# Back end for CS673Proj
- The Back end is mainly a Flask Rest API
- The api_module will handle all the call from the client side
- The file structure is represented as follows :
```
│   ├── api_module
│   │   ├── __init__.py
│   │   ├── chat_controller.py
│   │   ├── company_controller.py
│   │   ├── employee_controller.py
│   │   ├── helpers.py
│   │   ├── issue_controller.py
│   │   ├── models.py
│   │   ├── project_controller.py
│   │   ├── role_controller.py
│   │   ├── sprint_controller.py
│   │   ├── task_controller.py
│   │   ├── team_controller.py
│   │   └── user_controllers.py
│   └── templates
│       ├── 404.html
│       └── docstring.html
├── config.py
├── local
│   └── db
│       └── app.db
├── readme.md
├── run.py
├── static
└── tests
    ├── payload.txt
    └── pmp_backend.postman_collection.json

```

- Run a development server using the run.py
    - GET : http://0.0.0.0:5005/api/ 

# Requirements : 
- Python 3.6
    - flask
    - SQLAlchemy
    - jwt
    - flask_sqlalchemy
    - flask_cors
    - flask_socketio
    
# Run : 
- python run.py