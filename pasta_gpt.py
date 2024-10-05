import json
import re
import streamlit as st
import streamlit.components.v1 as components
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from openai import OpenAI
from openai import AzureOpenAI

from classes.threat_model_fl import ThreatModelCl
from classes.control_matrix_fl import ControlMatrixCl
from classes.attack_tree_fl import AttackTreeCl
from classes.mark_down_fl import MarkDownCl


# ------------------ Helper Functions ------------------ #

# Function to get user input for the application description and key details
def get_input():
    input_text = st.text_area(
        label="Describe the application to be modelled",
        placeholder="Enter your application details...",
        height=150,
        key="app_input",
        help="Please provide a detailed description of the application, including the purpose of the application, the technologies used, and any other relevant information.",
    )
    return input_text



# ------------------ Streamlit UI Configuration ------------------ #

openai_api_key = []
mistral_api_key = []


st.set_page_config(
    page_title="Threat Modelling GPT",
    page_icon=":pirate_flag:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Title font creation

st.markdown("""
<style>
.big-font {
    font-size:25px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">Welcome to Threat Modeling GPT, an AI-powered tool designed to help teams produce better threat models for given applications !!</p>', unsafe_allow_html=True)

# Adding some extra space
st.markdown(' ')
st.markdown(' ')

# Create three columns
col1, col2 = st.columns([2,1])


# Use middle coulmn to show the tool functionality
with col2:
    st.markdown(' ')
    st.markdown(
        "With this tool, one could generate"
    )
    st.markdown('- PASTA Threat Model')
    st.markdown('- Control Matrix')
    st.markdown('- MITRE Attack Tree')

# Use the first column to display the logo, which will be centered
with col1:
    st.image("logo.png", width=550)



# ------------------ Main App UI ------------------ #

# Get application description from the user
app_input = get_input()

# Create two columns layout for input fields
col1, col2 = st.columns(2)

# Create input fields for app_type, sensitive_data and pam
with col1:
    app_type = st.selectbox(
        label="Select the application type",
        options=[
            "Web application",
            "Mobile application",
            "Desktop application",
            "Cloud application",
            "IoT application",
            "Other",
        ],
        key="app_type",
    )

    sensitive_data = st.selectbox(
        label="What is the highest sensitivity level of the data processed by the application?",
        options=[
            "Top Secret",
            "Secret",
            "Confidential",
            "Restricted",
            "Unclassified",
            "None",
        ],
        key="sensitive_data",
    )

    pam = st.selectbox(
        label="Are privileged accounts stored in a Privileged Access Management (PAM) solution?",
        options=["Yes", "No"],
        key="pam",
    )

# Create input fields for internet_facing and authentication
with col2:
    internet_facing = st.selectbox(
        label="Is the application internet-facing?",
        options=["Yes", "No"],
        key="internet_facing",
    )

    authentication = st.multiselect(
        "What authentication methods are supported by the application?",
        ["SSO", "MFA", "OAUTH2", "Basic", "None"],
        key="authentication",
    )



# ------------------ Sidebar ------------------ #

# Add instructions on how to use the app to the sidebar
st.sidebar.header("How to use Threat Modeling GPT")

with st.sidebar:
    # Add model selection input field to the sidebar
    model_provider = st.selectbox(
        "Select your preferred model provider:",
        ["OpenAI API", "Mistral API"],
        key="model_provider",
        help="Select the model provider you would like to use. This will determine the models available for selection.",
    )

    if model_provider == "OpenAI API":
        st.markdown(
        """
    1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) and chosen model below 🔑
    2. Provide details of the application that you would like to threat model  📝
    3. Generate a threat list, attack tree and/or mitigating controls for your application 🚀
    """
    )
        # Add OpenAI API key input field to the sidebar
        openai_api_key = st.text_input(
            "Enter your OpenAI API key:",
            type="password",
            help="You can find your OpenAI API key on the [OpenAI dashboard](https://platform.openai.com/account/api-keys).",
        )

        # Add model selection input field to the sidebar
        selected_model = st.selectbox(
            "Select the model you would like to use:",
            ["gpt-4-turbo-preview", "gpt-4", "gpt-3.5-turbo"],
            key="selected_model",
            help="OpenAI have moved to continuous model upgrades so `gpt-3.5-turbo`, `gpt-4` and `gpt-4-turbo-preview` point to the latest available version of each model.",
        )

   

    if model_provider == "Mistral API":
        st.markdown(
        """
    1. Enter your [Mistral API key](https://console.mistral.ai/api-keys/) and chosen model below 🔑
    2. Provide details of the application that you would like to threat model  📝
    3. Generate a threat list, attack tree and/or mitigating controls for your application 🚀
    """
    )
        # Add OpenAI API key input field to the sidebar
        mistral_api_key = st.text_input(
            "Enter your Mistral API key:",
            type="password",
            help="You can generate a Mistral API key in the [Mistral console](https://console.mistral.ai/api-keys/).",
        )

        # Add model selection input field to the sidebar
        mistral_model = st.selectbox(
            "Select the model you would like to use:",
            ["mistral-large-latest", "mistral-small-latest"],
            key="selected_model",
        )

    st.markdown("""---""")

# Add "About" section to the sidebar
st.sidebar.header("About")

with st.sidebar:
    st.markdown(
        "Welcome to Threat Modeling GPT, an AI-powered tool designed to help teams produce better threat models for their applications."
    )
    st.markdown(
        "Threat modelling is a key activity in the software development lifecycle, but is often overlooked or poorly executed. PASTA (threat modelling) GPT aims to help teams produce more comprehensive threat models by leveraging the power of Large Language Models (LLMs) to generate threat agents, controls, and attack tree for an application based on the details provided."
    )
    st.markdown("Created by Satyanarayana Vuppala (some part source code has been leveraged from Github - /mrwadams/stride-gpt/).")
    
    st.markdown("""---""")


# Add "Example Application Description" section to the sidebar
st.sidebar.header("Example Application Description")

with st.sidebar:
    st.markdown(
        "Below is an example application description that you can use to test Threat Modeling GPT:"
    )
    st.markdown(
        "> A web application that allows users to create, store, and share personal notes. The application is built using the React frontend framework and a Node.js backend with a MongoDB database. Users can sign up for an account and log in using OAuth2 with Google or Facebook. The notes are encrypted at rest and are only accessible by the user who created them. The application also supports real-time collaboration on notes with other users."
    )
    st.markdown("""---""")

# Add "FAQs" section to the sidebar
st.sidebar.header("FAQs")

with st.sidebar:
    st.markdown(
        """
    ### **What is PASTA?**
    PASTA (Process for Attack Simulation and Threat Analysis) is a threat modeling methodology used to systematically identify potential threats and vulnerabilities in software applications. It provides a structured approach for analyzing security risks throughout the development lifecycle of an application. PASTA is designed to be comprehensive and adaptable to various types of applications and environments.
    """
    )
    st.markdown(
        """
    ### **How does Threat modeling GPT work?**
    When you enter an application description and other relevant details, the tool will use a GPT model to generate a threat model for your application. The model uses the application description and details to generate a list of potential threats and then categorises each threat according to the PASTA methodology.
    """
    )
    st.markdown(
        """
    ### **Do you store the application details provided?**
    No, Threat modeling GPT does not store your application description or other details. All entered data is deleted after you close the browser tab.
    """
    )
    st.markdown(
        """
    ### **Why does it take so long to generate a threat model?**
    If you are using a free OpenAI API key, it will take a while to generate a threat model. This is because the free API key has strict rate limits. To speed up the process, you can use a paid API key.
    """
    )
    st.markdown(
        """
    ### **Are the threat models 100% accurate?**
    No, the threat models are not 100% accurate. Threat Modeling GPT uses GPT Large Language Models (LLMs) to generate its output. The GPT models are powerful, but they sometimes makes mistakes and are prone to 'hallucinations' (generating irrelevant or inaccurate content). Please use the output only as a starting point for identifying and addressing potential security risks in your applications.
    """
    )
    st.markdown(
        """
    ### **How can I improve the accuracy of the threat models?**
    You can improve the accuracy of the threat models by providing a detailed description of the application and selecting the correct application type, authentication methods, and other relevant details. The more information you provide, the more accurate the threat models will be.
    """
    )

st.markdown("""---""")

# ------------------ Classess Initilization ------------------ #

threat_model_obj = ThreatModelCl()
control_matrix_obj = ControlMatrixCl()
attack_tree_obj = AttackTreeCl()
markdown_obj = MarkDownCl()

# ------------------ PASTA Threat Model Generation ------------------ #

# Create a collapsible section for Threat Modelling
with st.expander("Threat Model", expanded=False):
    # Create a submit button for Threat Modelling
    threat_model_submit_button = st.button(label="Generate Threat Model")


    # If the submit button is clicked and the user has not provided an application description
    if threat_model_submit_button and not app_input:
        st.error("Please enter your application details before submitting.")

    # If the submit button is clicked and the user has not provided API_key
    if threat_model_submit_button:
        if not openai_api_key and not mistral_api_key:
                st.error("Please enter at leat one API key before submitting.")

    # If the Generate Threat Model button is clicked and the user has provided an application description
    if threat_model_submit_button and app_input:
        # Generate the prompt using the create_prompt function
        threat_model_prompt = threat_model_obj.create_threat_model_prompt(app_type, authentication, internet_facing, sensitive_data, pam, app_input)

        # Show a spinner while generating the threat model
        with st.spinner("Analysing potential threats..."):
            try:
                # Call one of the get_threat_model functions with the generated prompt
                if model_provider == "OpenAI API":
                    model_output = threat_model_obj.get_threat_model(openai_api_key, selected_model, threat_model_prompt)
                elif model_provider == "Mistral API":
                    model_output = threat_model_obj.get_threat_model_mistral(mistral_api_key, mistral_model, threat_model_prompt)
                        
                # Access the threat model and improvement suggestions from the parsed content
                threat_model = model_output.get("threat_model", [])
                improvement_suggestions = model_output.get("improvement_suggestions", [])
                # print(threat_model)

                # Save the threat model to the session state for later use in mitigations
                st.session_state['threat_model'] = threat_model

                # Convert the threat model JSON to Markdown
                markdown_output = markdown_obj.json_to_markdown(threat_model, improvement_suggestions)

                # Display the threat model in Markdown
                st.markdown(markdown_output)

            except Exception as e:
                st.error(f"Error generating threat model: {e}")

            # Add a button to allow the user to download the output as a Markdown file
            st.download_button(
                label="Download Threat Model",
                data=markdown_output,  # Use the Markdown output
                file_name="pasta_gpt_threat_model.md",
                mime="text/markdown",
            )



# ------------------ CCM controls Generation ------------------ #

# Create a collapsible section for Secuyrity Controls
with st.expander("Security Controls", expanded=False):
    # Create a submit button for Controls Generation
    control_matrix_submit_button = st.button(label="Generate Control Matrix")


    # If the submit button is clicked and the user has not provided an application description
    if control_matrix_submit_button and not app_input:
        st.error("Please enter your application details before submitting.")

    # If the submit button is clicked and the user has not provided API_key
    if control_matrix_submit_button:
        if not openai_api_key and not mistral_api_key:
            st.error("Please enter at leat one API key before submitting.")

    # If the Generate TControl matrix button is clicked and the user has provided an application description
    if control_matrix_submit_button and app_input:
        # Generate the prompt using the create_prompt function
        control_matrix_prompt = control_matrix_obj.create_control_matrix_prompt(app_type, authentication, internet_facing, sensitive_data, pam, app_input)

        # Show a spinner while generating the threat model
        with st.spinner("Preparing security controls..."):
            try:
                # Call one of the get_threat_model functions with the generated prompt

                if model_provider == "OpenAI API":
                    model_output = control_matrix_obj.get_control_matrix(openai_api_key, selected_model, control_matrix_prompt)
                elif model_provider == "Mistral API":
                    model_output = control_matrix_obj.get_control_matrix_mistral(mistral_api_key, mistral_model, control_matrix_prompt)

                        
                # Access the threat model and improvement suggestions from the parsed content
                control_matrix = model_output.get("control_matrix", [])
                improvement_suggestions = model_output.get("improvement_suggestions", [])
                print(control_matrix )

                # Save the threat model to the session state for later use in mitigations
                st.session_state['control_matrix '] = control_matrix 

                # Convert the threat model JSON to Markdown
                markdown_output = markdown_obj.json_to_markdown_control(control_matrix , improvement_suggestions)

                # Display the threat model in Markdown
                st.markdown(markdown_output)

            except Exception as e:
                st.error(f"Error generating control matrix: {e}")

            # Add a button to allow the user to download the output as a Markdown file
            st.download_button(
                label="Download Threat Model",
                data=markdown_output,  # Use the Markdown output
                file_name="control_matrix_model.md",
                mime="text/markdown",
            )



    



# ------------------ MITRE ATTACK TREE Generation------------------ #

# Create a collapsible section for Attack Tree
with st.expander("MITRE Attack Tree", expanded=False):
    if model_provider == "Mistral API" and mistral_model == "mistral-small-latest":
        st.warning("⚠️ Mistral Small doesn't reliably generate syntactically correct Mermaid code. Please use the Mistral Large model for generating attack trees, or select a different model provider.")
    # Create a submit button for Attack Tree
    attack_tree_submit_button = st.button(label="Generate MITRE Attack Tree")

    # If the Generate Attack Tree button is clicked and the user has provided an application description
    if attack_tree_submit_button and app_input:
        # Generate the prompt using the create_attack_tree_prompt function
        attack_tree_prompt = attack_tree_obj.create_attack_tree_prompt(app_type, authentication, internet_facing, sensitive_data, pam, app_input)

        # Show a spinner while generating the attack tree
        with st.spinner("Generating attack tree..."):
            try:
                # Call to either of the get_attack_tree functions with the generated prompt
                
                if model_provider == "OpenAI API":
                    mermaid_code = attack_tree_obj.get_attack_tree(openai_api_key, selected_model, attack_tree_prompt)
                elif model_provider == "Mistral API":
                    mermaid_code = attack_tree_obj.get_attack_tree_mistral(mistral_api_key, mistral_model, attack_tree_prompt)

                # Display the generated attack tree code
                st.write("Attack Tree Code:")
                st.code(mermaid_code)

                # Visualise the attack tree using the Mermaid custom component
                st.write("Attack Tree Diagram Preview:")
                attack_tree_obj.mermaid(mermaid_code)
                
                col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
                
                with col1:              
                    # Add a button to allow the user to download the Mermaid code
                    st.download_button(
                        label="Download Diagram Code",
                        data=mermaid_code,
                        file_name="attack_tree.md",
                        mime="text/plain",
                        help="Download the Mermaid code for the attack tree diagram."
                    )

                with col2:
                    # Add a button to allow the user to open the Mermaid Live editor
                    mermaid_live_button = st.link_button("Open Mermaid Live", "https://mermaid.live")
                
                with col3:
                    # Blank placeholder
                    st.write("")
                
                with col4:
                    # Blank placeholder
                    st.write("")
                
                with col5:
                    # Blank placeholder
                    st.write("")

            except Exception as e:
                st.error(f"Error generating attack tree: {e}")



