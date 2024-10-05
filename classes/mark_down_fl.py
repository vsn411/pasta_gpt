
import json
import re
import streamlit as st
import streamlit.components.v1 as components
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from openai import OpenAI
from openai import AzureOpenAI

class MarkDownCl:
        
    # Function to convert JSON to Markdown for display.    
    def json_to_markdown(self, threat_model, improvement_suggestions):
        markdown_output = "## Threat Model\n\n"
        
        # Start the markdown table with headers
        global_header = []
        for threat in threat_model:
            global_header = threat
    
        for key in global_header.keys():
            markdown_output += f"| " + key
        markdown_output += f"\n"
        markdown_output += "|-------------|----------|------------------|-----------------|\n"
        
        # Fill the table rows with the threat model data
        for threat in threat_model:
            for key in threat.keys():
                markdown_output += f"| {threat[key]} "
            markdown_output += f"\n"
            #markdown_output += f"| {threat['Threat Agent']} | {threat['Threats']} | {threat['Risk Rating (Likelihood, Impact, Risk Level)']} |{threat['Mitigations']} |\n"
        
        markdown_output += "\n\n## Improvement Suggestions\n\n"
        for suggestion in improvement_suggestions:
            markdown_output += f"- {suggestion}\n"
        
        return markdown_output



    # Function to convert JSON to Markdown (security controls) for display.    
    def json_to_markdown_control(self, control_matrix, improvement_suggestions):
        markdown_output = "## Security control\n\n"
        
        # Start the markdown table with headers    
        global_header = []
        for control in control_matrix:
            global_header = control

        for key in global_header.keys():
            markdown_output += f"| " + key
        markdown_output += f"\n"
        markdown_output += "|-------------|----------|------------------|-----------------|-----------------|\n"
        
        
        # Fill the table rows with the threat model data
        for control in control_matrix:
            for key in control.keys():
                markdown_output += f"| {control[key]} "
            markdown_output += f"\n"
            # markdown_output += f"| {control['CCM Control ID']} | {control['Control Description']} | {control['Questionarries']} |{control['ISO 27001 reference']} |{control['NIST 800-53 reference']}|\n"
        
        markdown_output += "\n\n## Improvement Suggestions\n\n"
        for suggestion in improvement_suggestions:
            markdown_output += f"- {suggestion}\n"
        
        return markdown_output
