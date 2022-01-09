# Blockchain tutorial
Following this tutorial:
https://hackernoon.com/learn-blockchains-by-building-one-117428612f46

Some changes:
- Using fastapi instead of flask
- Using pydantic models instead of dict for Block and Transaction

# Usage

```shell
uvicorn main:app --port 5000
```
Open your browser to http://127.0.0.1:5000/docs to try the API.
