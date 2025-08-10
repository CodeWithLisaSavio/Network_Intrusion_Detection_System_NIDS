import requests
import json

# -----------------------------
# IBM Watsonx.ai API Credentials
# -----------------------------
API_KEY = "your_ibm_cloud_api_key"
DEPLOYMENT_URL = "https://your-deployment-url.ibm.com/ml/v4/deployments/your-deployment-id/predictions"
MODEL_INPUT_FIELDS = ["duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes", ...]  # Add all required fields

# -----------------------------
# Get IAM Token from IBM Cloud
# -----------------------------
def get_iam_token(api_key):
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = f"apikey={api_key}&grant_type=urn:ibm:params:oauth:grant-type:apikey"
    response = requests.post(url, headers=headers, data=data)
    return response.json()["access_token"]

# -----------------------------
# Send Input Data to AutoAI Model
# -----------------------------
def send_to_autoai_model(input_values, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "input_data": [{
            "fields": MODEL_INPUT_FIELDS,
            "values": [input_values]
        }]
    }

    response = requests.post(DEPLOYMENT_URL, headers=headers, json=payload)
    return response.json()

# -----------------------------
# Display Prediction Results
# -----------------------------
def display_results(result_json):
    try:
        predictions = result_json["predictions"][0]["values"][0]
        print("\n🔍 Prediction Result:")
        for i, value in enumerate(predictions):
            print(f"  Output {i+1}: {value}")
    except Exception as e:
        print("Error parsing results:", e)

# -----------------------------
# Example Usage
# -----------------------------
if __name__ == "__main__":
    print("🔗 Connecting to IBM Watsonx.ai AutoAI Model...")

    token = get_iam_token(API_KEY)

    # Example input values — replace with real network data
    input_values = [1, 0, 0, 0, 1234, 5678, ...]  # Fill in all required features

    result = send_to_autoai_model(input_values, token)
    display_results(result)
