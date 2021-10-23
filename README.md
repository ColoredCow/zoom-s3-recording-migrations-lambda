# zoom-recording-manager

This project contains source code and supporting files for a serverless application that you can deploy with the SAM CLI. It includes the following files and folders.

- zoom_recording_manager - Code for the application's Lambda function.
- events - Invocation events that you can use to invoke the function. (Currently not in use)
- template.yaml - A template that defines the application's AWS resources.

The application uses several AWS resources, including Lambda functions and an API Gateway API. These resources are defined in the `template.yaml` file in this project. You can update the template to add AWS resources through the same deployment process that updates your application code.


## Install the application

1. Clone the project and inside the project folder run:
    ```sh
    cd project_folder
    python3 -m venv venv
    source ./venv/bin/activate
    ```
2. Install aws sam client
    ```sh
    pip install aws-sam-cli
    ```


## Deploy the application on Lambda (Manually)
1. Build the application using sam in your local using the below command
   ```sh
   sam build
   ```
2. A `.aws-sam` folder will be created. And inside the build folder you will find your project resources.
3. Open your project folder and Zip all the folders and files. 
4. Upload the zip to the lambda function.