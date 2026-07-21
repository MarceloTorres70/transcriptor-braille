import os
from inference_sdk import InferenceHTTPClient

def process_roboflow_predictions(predictions):
    if not predictions:
        return "", []
    
    # Sort predictions geometrically
    # First, calculate average height to use as tolerance for line grouping
    avg_height = sum(p.get('height', 20) for p in predictions) / len(predictions)
    y_tolerance = avg_height * 0.5  # Half a character height
    
    # Sort by Y-coordinate
    sorted_by_y = sorted(predictions, key=lambda p: p.get('y', 0))
    
    lines = []
    current_line = []
    
    if sorted_by_y:
        current_y = sorted_by_y[0].get('y', 0)
        
        for pred in sorted_by_y:
            if abs(pred.get('y', 0) - current_y) <= y_tolerance:
                current_line.append(pred)
            else:
                lines.append(current_line)
                current_line = [pred]
                current_y = pred.get('y', 0)
        if current_line:
            lines.append(current_line)
            
    # Sort horizontally for each line and concatenate
    raw_braille = ""
    for line in lines:
        line_sorted_by_x = sorted(line, key=lambda p: p.get('x', 0))
        for pred in line_sorted_by_x:
            raw_braille += pred.get('class', '')
        raw_braille += "\n"
        
    return raw_braille.strip(), predictions

def detect_braille(image_path):
    CLIENT = InferenceHTTPClient(
        api_url="https://serverless.roboflow.com",
        api_key=("V5Ps7qCSZgJHmJmwt7lQ")
    )
    MODEL_ID = "braille-detection-f0rb5/10"
    
    result = CLIENT.infer(image_path, model_id=MODEL_ID)
    predictions = result.get("predictions", [])
    
    raw_braille, ordered_predictions = process_roboflow_predictions(predictions)
    return raw_braille, ordered_predictions
