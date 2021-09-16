## Django-Starter Project

Django Starter Project to quickly get you starter your new django project.

## Prerequisites

1. Use [python >= 3.7.6](https://www.python.org/downloads/release/python-376/)
2. (Optional) Recommended to use [Anaconda](https://www.anaconda.com/products/individual) as a python distribution and as a python environment manager (see [here](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#activating-an-environment) to create conda environments)

## Getting Started

1. Clone the repo
2. Install requirements using pip

```console
python -m pip install -r requirements.txt
```

3. Replace `YOUR_PROJECT` and `your_project` folder with your own project name accordingly (you will have to replace all instance of `your_project` with your own project's name)

4. Done. Start developing your project

## Response Structure

All the views in this project are supposed to use create_response method in [/common/response](./common/response.py) module. It's recommended to use this because it helps in simplifying the response structure across the project (see [here](your_project/users/views/user_change_password.py) for an example usage).

```python
{
    "data": "payload data", # payload data, this will contain what the individual views intent to return
    "errors": [], # list of possible errors that were encountered during the processing of the request, eg- Authentication Error, Permission Denied etc.
    "statusCode": 201, # or 401, 404, etc.
}
```

## Endpoints

1. For quickly get you started, this project comes with a default implementation of Users and Authentication views. For Authentication I have used [djangorestframework-simplejwt](https://pypi.org/project/djangorestframework-simplejwt/). Visit [/your_project/playground](http://localhost:8000/your_project/playground) to explore all the endpoints (this is a [swagger](https://swagger.io/) endpoint descibing all project related endpoints).

2. Also, Visit [/your_project/](http://localhost:8000/your_project/docs) to explore all the endpoints in [ReDoc](https://github.com/Redocly/redoc) style

## References

Would like to mention [HackSoft Stylguide](https://github.com/HackSoftware/Styleguide-Example), almost all of the code here, are copied from there :grin:. Would recommend watching their tutorial [HackSoft](https://github.com/HackSoftware)

## Copyrights & License

© [Sinha, Ujjawal](https://github.com/Sinha-Ujjawal)

Licensed under [MIT](./LICENSE)
