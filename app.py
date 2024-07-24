import streamlit as st
from openai import OpenAI

openai_api_key = st.secrets['OPENAI_API_KEY']

# Initialize variables
system_message = """
You are a customer service AI assistant. Your goal is to help users with their inquiries and detect if they need to be escalated to a human representative. Pay attention to signs of frustration, repeated requests for human assistance, or complex issues that may require human intervention.
"""

prompt_instructions = """
Analyze the user's message and previous interactions. If you detect any of the following, suggest escalation:
1. Explicit requests to speak with a human
2. Signs of frustration or dissatisfaction with AI responses
3. Complex issues that may be beyond AI capabilities
4. Repeated questions or clarifications indicating misunderstanding
5. Some symptoms of Mental Illness like:
  - Look for keywords or phrases indicating distress, such as "hopeless," "can't cope," or "want to hurt myself"
  - Detect patterns of negative or anxious language
  - Note sudden changes in communication style or tone
  - Recognize expressions of isolation or lack of support
  - Be alert for references to trauma, abuse, or major life stressors

If escalation is needed, respond with "ESCALATE: " followed by your reasoning. Otherwise, respond normally to the user's query.
"""

# Sidebar for API key input
with st.sidebar:
    "**OHL PoC**"
    "Identifying the need to escalate to a human agent."
    ""
    "You can try:"
    "1. explicitly ask for a human agent"
    "2. struggle with understanding the response"
    "3. mimic signs of mental health problems"
    ""
    "When identifying any of these scenarios, the chat should stop and trigger an ESCALATION."
    ""
    "Please hit the Reset Conversation button to restart after an ESCALATION."

    # Model selection dropdown
    model_option = st.selectbox(
        'Choose GPT model',
        ('gpt-4o', 'gpt-4o-mini', 'gpt-4-turbo', 'gpt-4')
    )

st.title("💬 Customer Service AI Assistant with Need to Escalate detection")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt_instructions},
        {"role": "assistant", "content": "Hello! How can I assist you today?"}
    ]

# Display chat messages
for message in st.session_state.messages[2:]:  # Skip system message and instructions
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What's your question?"):
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model=model_option,  # Use the selected model
        messages=st.session_state.messages
    )
    assistant_response = response.choices[0].message.content

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    
    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
    
    # Check for escalation
    if assistant_response.startswith("ESCALATE:"):
        st.warning("This conversation has been flagged for escalation to a human representative.")

# Reset button
if st.button("Reset Conversation"):
    st.session_state.messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt_instructions},
        {"role": "assistant", "content": "Hello! How can I assist you today?"}
    ]
    st.experimental_rerun()