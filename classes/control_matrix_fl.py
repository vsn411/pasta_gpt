import json
import re
import streamlit as st
import streamlit.components.v1 as components
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from openai import OpenAI
from openai import AzureOpenAI

class ControlMatrixCl:

    # Function to create a prompt for generating a control matrix
    def create_control_matrix_prompt(self, app_type, authentication, internet_facing, sensitive_data, pam, app_input):
        prompt = f"""
    Act as a cyber security expert with more than 20 years experience of using ISO 27001, NIST 800:53 and Cloud Security Alliance CCM matrix for security applications.  Provide me list of security controls as per CCM matrix aligning with ISO 27001, NIST 800-53. For each control, list set of questionaries that are needed to be addressed. Provide in a table format. Columns in table should be 'CCM Control ID', 'Control Description', 'Questionarries', 'ISO 27001 reference' and 'NIST 800-53 reference’. It is very important that your responses are tailored to reflect the details you are given.

    APPLICATION TYPE: {app_type}
    AUTHENTICATION METHODS: {authentication}
    INTERNET FACING: {internet_facing}
    SENSITIVE DATA: {sensitive_data}
    PRIVILEGED ACCESS MANAGEMENT: {pam}
    APPLICATION DESCRIPTION: {app_input}

    When providing the control matrix use a JSON formatted response with the keys “control_matrix” and "improvement_suggestions". Under “control_matrix”, include an array of objects with the keys “CCM Control ID”, “Control Description”, “Questionarries”, “ISO 27001 reference”, and “NIST 800-53 reference”. 
    """
        return prompt


    # Function to get control matrix from the GPT response.
    def get_control_matrix(self, api_key, model_name, prompt):
        #client = OpenAI(organization='org-tn1PRlanO2IDw3NJYDZIUgNr')
        client = OpenAI(api_key=api_key)


        response = client.chat.completions.create(
            model=model_name,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4000,
        )

        # Convert the JSON string in the 'content' field to a Python dictionary
        response_content = json.loads(response.choices[0].message.content, strict=False)

        return response_content


    # Function to get control matrix from Mistral response.
    def get_control_matrix_mistral(self, api_key, model_name, prompt):
        client = MistralClient(api_key=mistral_api_key)

        response = client.chat(
            model = mistral_model,
            response_format={"type": "json_object"},
            messages=[
                ChatMessage(role="user", content=prompt)
            ]
        )

        # Convert the JSON string in the 'content' field to a Python dictionary
        response_content = json.loads(response.choices[0].message.content)

        return response_content
