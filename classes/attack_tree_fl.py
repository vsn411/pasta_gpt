import json
import re
import streamlit as st
import streamlit.components.v1 as components
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from openai import OpenAI
from openai import AzureOpenAI

class AttackTreeCl:
        
    # Function to create a prompt to generate an attack tree
    def create_attack_tree_prompt(self, app_type, authentication, internet_facing, sensitive_data, pam, app_input):
        prompt = f"""
    APPLICATION TYPE: {app_type}
    AUTHENTICATION METHODS: {authentication}
    INTERNET FACING: {internet_facing}
    SENSITIVE DATA: {sensitive_data}
    PRIVILEGED ACCESS MANAGEMENT: {pam}
    APPLICATION DESCRIPTION: {app_input}
    """
        return prompt


    # Function to get attack tree from the GPT response.
    def get_attack_tree(self, api_key, model_name, prompt):
        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": """
    As a cybersecurity expert with over 20 years of experience in threat modeling using the PASTA methodology, your task is to develop a comprehensive threat model.  Your goal is to create a MITRE ATT&CK matrix reflecting potential threat agents and threats based on the provided application details.

    You MUST only respond with the Mermaid code block. See below for a simple example of the required format and syntax for your output.

    ```mermaid
    graph TD
        A[Enter Chart Definition] --> B(Preview)
        B --> C{{decide}}
        C --> D["Keep"]
        C --> E["Edit Definition (Edit)"]
        E --> B
        D --> F["Save Image and Code"]
        F --> B
    ```

    IMPORTANT: Round brackets are special characters in Mermaid syntax. If you want to use round brackets inside a node label you MUST wrap the label in double quotes. For example, ["Example Node Label (ENL)"].
    """},
                {"role": "user", "content": prompt}
            ]
        )

        # Access the 'content' attribute of the 'message' object directly
        attack_tree_code = response.choices[0].message.content
        
        # Remove Markdown code block delimiters using regular expression
        attack_tree_code = re.sub(r'^```mermaid\s*|\s*```$', '', attack_tree_code, flags=re.MULTILINE)

        return attack_tree_code



    # Function to get attack tree from the Mistral model's response.
    def get_attack_tree_mistral(self, api_key, model_name, prompt):
        client = MistralClient(api_key=mistral_api_key)

        response = client.chat(
            model=mistral_model,
            messages=[
                {"role": "system", "content": """
    As a cybersecurity expert with over 20 years of experience in threat modeling using the PASTA methodology, your task is to develop a comprehensive threat model.  Your goal is to create a MITRE ATT&CK matrix reflecting potential threat agents and threats based on the provided application details.

    You MUST only respond with the Mermaid code block. See below for a simple example of the required format and syntax for your output.

    ```mermaid
    graph TD
        A[Enter Chart Definition] --> B(Preview)
        B --> C{{decide}}
        C --> D["Keep"]
        C --> E["Edit Definition (Edit)"]
        E --> B
        D --> F["Save Image and Code"]
        F --> B
    ```

    IMPORTANT: Round brackets are special characters in Mermaid syntax. If you want to use round brackets inside a node label you MUST wrap the label in double quotes. For example, ["Example Node Label (ENL)"].
    """},
                {"role": "user", "content": prompt}
            ]
        )

        # Access the 'content' attribute of the 'message' object directly
        attack_tree_code = response.choices[0].message.content
        
        # Remove Markdown code block delimiters using regular expression
        attack_tree_code = re.sub(r'^```mermaid\s*|\s*```$', '', attack_tree_code, flags=re.MULTILINE)

        return attack_tree_code

    # Function to render Mermaid diagram
    def mermaid(self, code: str, height: int = 500) -> None:
        components.html(
            f"""
            <pre class="mermaid" style="height: {height}px;">
                {code}
            </pre>

            <script type="module">
                import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
                mermaid.initialize({{ startOnLoad: true }});
            </script>
            """,
            height=height,
        )
