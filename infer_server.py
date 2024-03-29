from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = Flask(__name__)

# Assume the device is CUDA; ensure the model and tokenizer are loaded globally
device = "cuda"

model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2", torch_dtype=torch.float16).to(device)
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Parse the JSON input
        data = request.json
        messages = data.get("messages", [])

        # Check if messages are provided
        if not messages:
            return jsonify({"error": "No messages provided"}), 400

        try:
            # Process the messages
            encodeds = tokenizer.apply_chat_template(messages, return_tensors="pt")

            model_inputs = encodeds.to(device)
            model.to(device)

            # Generate response from the model
            generated_ids = model.generate(model_inputs, max_new_tokens=1000, do_sample=True)
            decoded = tokenizer.batch_decode(generated_ids)

            # Return the model output
            return jsonify({"response": decoded[0]})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "infer service is ready"}), 200

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)
