from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import os

# 1. Define the System instructions with strict architectural constraints
system_template = """You are the progressive reading engine for a gritty, hard-boiled detective mystery. 
Your objective is to seamlessly inject beginner-level vocabulary into English text to facilitate contextual language learning.

RULES:
1. DIALECT: You must use the {dialect} dialect of Spanish. Prioritize regional terms if applicable.
2. TRANSLATION LIMIT: Select EXACTLY THREE (3) basic, beginner-level nouns from the provided text.
3. INLINE REPLACEMENT: Translate those three nouns into the {dialect} dialect. Leave all other text in the original English.
4. TONE: Preserve the dark, serious, hard-boiled tone of the original narrative. Do not break character.
5. REQUIRED FORMAT: You MUST wrap the translated words in a custom XML tag using this exact structure: 
   <vocab en="original_english_word">translated_spanish_word</vocab>

Example Output format:
The detective walked into the <vocab en="room">habitación</vocab> and saw the <vocab en="blood">sangre</vocab>.
"""

system_message = SystemMessagePromptTemplate.from_template(system_template)

# 2. Define the Human input
human_template = "CONTEXT TO PROCESS:\n{context}"
human_message = HumanMessagePromptTemplate.from_template(human_template)

# 3. Compile the chat template
chat_template = ChatPromptTemplate.from_messages([system_message, human_message])

# 4. Format and print to tests your variables
# We will use a mock paragraph from our earlier tests
mock_context = "Rojas began his search systematically, tearing through the minimalist furniture. The bedroom closet held three bespoke suits, all empty."

messages = chat_template.format_messages(
    dialect="Costa Rican",
    context=mock_context
)

# Print the final formatted prompt that will be sent to the LLM
for msg in messages:
    print(f"--- {msg.type.upper()} MESSAGE ---")
    print(msg.content)
    print("\n")

# 5. Initialize the LLM
# We use gpt-4o-mini because it is incredibly cheap, fast, and excellent at strict formatting.
# Temperature is set low (0.2) because we want strict, predictable formatting, not creative poetry.
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

# 6. Build the Chain using LCEL
# This pipes the variables -> prompt template -> LLM -> String parser
translation_chain = chat_template | llm | StrOutputParser()

print("\n--- EXECUTING AI PROGRESSIVE TRANSLATION ---")

try:
    # 7. Invoke the chain!
    # This is the actual network call to OpenAI.
    result = translation_chain.invoke({
        "dialect": "Costa Rican",
        "context": mock_context
    })

    print("\nFINAL OUTPUT:")
    print(result)

except Exception as e:
    print(f"\nPipeline blocked. API Error: {e}")
    print("If this is a 429 Error, your OpenAI account balance is still $0.00.")