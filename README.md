# AWS API Gateway with Cognito Authentication

Design and implement an AWS API Gateway that uses Cognito for authentication and connects to two Lambda functions. Each Lambda function will call an external service of the candidate's choice. The candidate must use CloudFormation scripts to provide the necessary infrastructure and clear documentation.

## Description

* API Gateway and Cognito Setup:

  Create an API Gateway with at least two endpoints.
  Implement Cognito as the authentication mechanism for these endpoints. Use an Amazon Cognito User Pool and configure it for secure access to the API.

* Lambda Functions:

  Develop two AWS Lambda functions. Each function should:
  Call an external service of your choice. The services can be any publicly accessible APIs.
  At least one of the external services must require authentication (e.g., an API key). A free-tier API such as OpenWeatherMap is acceptable.Process the response from the external service and return a meaningful output to the API Gateway.


## Getting Started

* Set an IAM User
  If you are using VSCode you can install "AWS toolkit" extension. You can generate an Access key with the IAM user and connect to your AWS from VSCode.

  ![IAM User Setup](https://github.com/dnaval/AWS-API-Cognito/blob/main/assets/IAM_User_Config.png)

* Install AWS CLI
  To use the aws command you need install the AWS CLI on your computer. Instructions for all the common operating system are available here: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

* Create a User Pool (Amazon Cognito)
  Amazon Cognito user pool is a user directory for web and mobile app authentication and authorization.

  User Pool setup:

  ![User Pool](https://github.com/dnaval/AWS-API-Cognito/blob/main/assets/AWS_Cognito_User_Pools.png)

  App client setup:

  ![App Client](https://github.com/dnaval/AWS-API-Cognito/blob/main/assets/UserPool_AppClient.png)

* Create a bucket (Amazon S3)
  You can create a bucket in the S3 service in AWS. This bucket will be used to upload the Lambda function code.

  ![S3 Bucket](https://github.com/dnaval/AWS-API-Cognito/blob/main/assets/S3_Bucket.png)

* Upload Lambdas function file (zip)
  In VSCode:

  ![Lambdas Zip Files](https://github.com/dnaval/AWS-API-Cognito/blob/main/assets/lambdas_zip_files.png)

  In AWS:

  ![Bucket Lambdas Files](https://github.com/dnaval/AWS-API-Cognito/blob/main/assets/Bucket_Lambda_AWS.png)

* Update the parameters in main.yaml
  ```
  Parameters:
    StageName:
      Type: String
      Default: dev

    UserPoolId:
      Type: String
      Default: USER_POOL_ID

    CognitoClientId:
      Type: String
      Default: APP_CLIENT_ID

    OpenWeatherApiKey:
      Type: String
      NoEcho: true
      Default: OPENWEATHER_API_KEY
  ```

* Deploy Stack
  To create the stack (remeber to add the OPENWEATHER_API_KEY) :
  ```bash
    aws cloudformation create-stack \
    --stack-name dnavaldev-assessment-stack \
    --template-body file://cloudformation/main.yaml \
    --parameters ParameterKey=OpenWeatherApiKey,ParameterValue=OPENWEATHER_API_KEY \
    --capabilities CAPABILITY_IAM \
    --region us-east-1
    ```

  To update the stack (Optional - remeber to add the OPENWEATHER_API_KEY):
  ```bash
    aws cloudformation deploy \
    --stack-name dnavaldev-assessment-stack \
    --template-file cloudformation/main.yaml \
    --parameter-overrides OpenWeatherApiKey=OPENWEATHER_API_KEY \
    --capabilities CAPABILITY_IAM \
    --region us-east-1
  ```

  You should see this in your AWS:
  ![Docker Installation](https://github.com/dnaval/AWS-API-Cognito/blob/main/assets/Stack_function_API.gif)

## API endpoint testing

* Enable Password Grant in Cognito
  - Go to AWS Management Console → Cognito → User Pools → Your User Pool
  - Click App clients
  - Click Show details on your App Client
  - Under “Authentication flows” (or “Enabled Identity Providers” for some versions), check:
    ALLOW_USER_PASSWORD_AUTH
    ALLOW_REFRESH_TOKEN_AUTH
  - Save changes
  ![Password Grant Setup](https://github.com/dnaval/AWS-API-Cognito/blob/main/assets/Setting_to_Get_Token_URL.gif)


* Get a JWT Token from Cognito
  You must authenticate against your Cognito User Pool to get an ID Token or Access Token.

  - Modify this URL and open in your browser:
   [AUTHORIZATION_URL](https://us-east-1yizyglfdu.auth.us-east-1.amazoncognito.com/oauth2/authorize?response_type=code&client_id=pdrck2rmiq4oilgkq5rghipo1&redirect_uri=https://dnavaldev.com/&scope=openid)

    What happens, Cognito shows the login page. You log in. Cognito redirects to your callback: https://dnavaldev.com/?code=AUTHORIZATION_CODE
    Example: https://dnavaldev.com/?code=0b7c9f9c-xxxxxx
    Copy the code value.

  - Exchange Authorization Code for JWT Token
    Now use curl to get the tokens.
    ```bash
    curl -X POST https://us-east-1yizyglfdu.auth.us-east-1.amazoncognito.com/oauth2/token \
    -u CLIENT_ID:CLIENT_SECRET \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "grant_type=authorization_code&code=AUTHORIZATION_CODE&redirect_uri=CALLBACK_URL/"
    ```
    Replace CLIENT_ID, CLIENT_SECRET, AUTHORIZATION_CODE and CALLBACK_URL with your values.
    
    For test purposes:
    ```bash
    curl -X POST https://us-east-1yizyglfdu.auth.us-east-1.amazoncognito.com/oauth2/token \
    -u pdrck2rmiq4oilgkq5rghipo1:rfuim92u4gfqe4d43u2m094e2k147k0gl2912u8301at3o1dj2t \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "grant_type=authorization_code&code=AUTHORIZATION_CODE&redirect_uri=https://dnavaldev.com/"
    ```

    Example response:
    ```bash
    {
    "id_token": "eyJraWQiOiJ...",
    "access_token": "eyJraWQiOiJ...",
    "...." : "...."
    "expires_in": 3600,
    "token_type": "Bearer"
    }
    ```

* Test API with CURL
  Use the "id_token" as "Bearer Token" in postman or the CURL command below.

  Call your Amazon API Gateway for Lambda1 function endpoint:
  ```bash
  curl https://ibs4o9nz2f.execute-api.us-east-1.amazonaws.com/dev/age \
  -H "Authorization: Bearer eyJraWQiOiJ..."
  ```

  Call your Amazon API Gateway Lambda2 function endpoint:
  ```bash
  curl https://ibs4o9nz2f.execute-api.us-east-1.amazonaws.com/dev/weather \
  -H "Authorization: Bearer eyJraWQiOiJ..."
  ```


### Authors

ScanSource Canada Assessment
Candidat: Daniel Naval
