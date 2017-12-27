from cookiecutter.main import cookiecutter

cookiecutter('cookiecutter-nim-cli',
             no_input=True,
             extra_context={
    "full_name": "Tester",
    "email": "testerexample.com",
    "github_username": "tester",
    "project_name": "TestProject",
    "project_slug": "testproject",
    "project_short_description": "A TEST description.",
    "release_date": "2000-01-01",
    "version": "0.1.0",
    "_extensions": ["jinja2_time.TimeExtension"]
})
