import json, services


def lambda_handler(event, context):
    jsonData = event
    recording_handler = services.RecordingHandler(jsonData)
    recording_handler.handle_recording()

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": "Recording Uploaded Successfully",
    }
