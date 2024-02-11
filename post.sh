curl -X POST http://localhost:8080/predict \
	-H "Content-Type: application/json" \
	-d '{"messages": [{"role": "user", "content": "Tell me about Lassie and Timmy in the well."}]}'

