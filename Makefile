dev:
	uvicorn app.main:app --reload

demo:	
	curl -X POST http://localhost:8000/generate \
	  -H "Content-Type: application/json" \
	  -d '{"description": "list all schemas"}'
