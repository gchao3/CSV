import streamlit as st
import pandas as pd
from openai import AzureOpenAI
import requests
import json


def main():
    st.set_page_config(page_title="Input your CSV")
    st.header("Input your CSV for Analysis")

    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        categorical_cols = data.select_dtypes(include=['object','category']).columns
        duplicate_category_columns = [col for col in categorical_cols if data[col].duplicated().any()]

        categorical_summary = {col: data[col].value_counts() for col in duplicate_category_columns}
       
        client = AzureOpenAI(
            azure_endpoint="https://tennisfinancecentral.openai.azure.com/",
            api_key="9df14b8a59b04a40b8fbf83216fde843",
            api_version="2024-02-01",
        )

        message_text = [
            {
                "role": "system",
                "content": f"The following is a explanation of each potential category that might appear in the dataframe. -Product Type (CFPB): Type of product related to the complaint, as categorized by the Consumer Financial Protection Bureau (CFPB) -Subproduct Type (CFPB): Subtype of the product related to the complaint. -Issue type: Type of issue as categorized by the CFPB. -Complaint Source: Source from which the complaint originated.-Legal Action: Indicates whether legal action was involved (Yes or No). -Resolution Status: Status of the complaint resolution.-Potential UDAAP Complaint: Assessment of potential Unfair, Deceptive, or Abusive Acts or Practices (Yes or No).-Potential CFPB Complaint: Indicates whether there is a potential complaint to the CFPB (Complaint or Inquiries). -Potential Bank Complaint: Indicates whether there is a potential complaint to the bank (Yes or No). -Reg Z: Indicates whether there is a potential reg Z issue -ECOA: Indicates if there are any potential equal credit opportunity act issues. Generate a detailed report using the data summary provide, highlighting promminent reoccuring or common issues and trends that merit further attention. For Example: We processed 30 complaints. There were 25 complaints indicated that [CLIENT] failed to provide the consumer with requested documentation such as account statements or tax documentation. You may want to look further into these accounts to determine if there is an operational process breakdown or manual error by call center employee(s). Breakdown the report into 3 categories that make the most sense. Data summary <{categorical_summary}> ",
            }
        ]

        completion = client.chat.completions.create(
            model="rally-gpt-4",  # model = "deployment_name"
            messages=message_text,
            temperature=0.7,
            max_tokens=1000,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
        )

        message_content = completion.choices[0].message.content
        st.subheader("Generated Analysis")
        st.write(message_content)

        st.header("Ask Anything About the CSV")
        user_question = st.text_input("Example: You can ask it to summarize the results in a specific format or ask how many instances of udaap issues you found.")
        if user_question: 
             message_text2 = [{
             "role":"system",
             "content":f"{user_question} Data summary <{categorical_summary}> "}]

             completion2 = client.chat.completions.create(
             model="rally-gpt-4", # model = "deployment_name"
             messages = message_text2,
             temperature=0.7,
             max_tokens=2000,
             top_p=0.95,
             frequency_penalty=0,
             presence_penalty=0,
             stop=None
             )

             message_content2 = completion2.choices[0].message.content
             st.subheader('Question Response')
             st.write(message_content2)

    print("Streamlit app is running...")


if __name__ == "__main__":
    main()
