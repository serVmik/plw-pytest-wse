# plw-pytest-wse

## Testing "Web Self Educate" application with Playwright and Pytest

### Install
```commandline
poetry install --no-root
source .venv/bin/activate
playwright install --with-deps
playwright install
```

### Populate .env
- add host  
- add user name  
- add user password  


### Save the signed-in state
```commandline
make state
```

### Run tests
```commandline
make test
```