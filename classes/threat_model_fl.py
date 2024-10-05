import json
import re
import streamlit as st
import streamlit.components.v1 as components
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from openai import OpenAI
from openai import AzureOpenAI


class ThreatModelCl:

    # Function to create a prompt for generating a threat model
    def create_threat_model_prompt(self, app_type, authentication, internet_facing, sensitive_data, pam, app_input):
        prompt = f"""
    Act as a cyber security expert with more than 20 years experience of using the PASTA threat modelling methodology to produce comprehensive threat models for a wide range of applications. Your task is to use the application description and additional provided to you to produce a list of specific threat agents, modelling threats, and providing recommendations for the application. 

    in the context of the application type and application description, for each threat agent in PASTA modelling, list multiple threats (10 or 12). You should list minimum of 4 threat agents. It is important to prioritise those threats with risk ratings (likelihood, impact, risk level). Also, provide mitigations for each identified threat under a selected threat agent. All answers should be laid out in a single table format. It is very important that your responses are tailored to reflect the details you are given.

    APPLICATION TYPE: {app_type}
    AUTHENTICATION METHODS: {authentication}
    INTERNET FACING: {internet_facing}
    SENSITIVE DATA: {sensitive_data}
    PRIVILEGED ACCESS MANAGEMENT: {pam}
    APPLICATION DESCRIPTION: {app_input}

    When providing the threat model, use a JSON formatted response with the keys "threat_model" and "improvement_suggestions". Under "threat_model", include an array of objects with the keys "Threat Agent”, “Threats”, “Risk Rating (Likelihood, Impact, Risk Level)”, and “Mitigations”. 

    Under "improvement_suggestions", include an array of strings with suggestions on how the threat modeller can improve their application description in order to allow the tool to produce a more comprehensive threat model.

    """
        return prompt


    # Function to get threat model from the GPT response.
    def get_threat_model(self, api_key, model_name, prompt):
        
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
        response_content = json.loads(response.choices[0].message.content,strict=False)
        

        return response_content
    
        # Function to get threat model from Mistral response.
    def get_threat_model_mistral(self, api_key, model_name, prompt):
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
