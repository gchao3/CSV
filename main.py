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
        initial_overview = {
            "Number of Cases": data.shape[0],
            "Number of Columns": data.shape[1],
            "Columns": data.columns.tolist(),
        }

        categorical_cols = [
            "Product Type (CFPB)",
            "Subproduct Type (CFPB)",
            "Issue type (CFPB)",
            "Complaint Source",
            "Legal Action",
            "Resolution Status",
            "Potential UDAAP Complaint",
            "Potential CFPB Complaint",
            "Potential Bank Complaint",
        ]

        categorical_summary = {
            col: data[col].value_counts() for col in categorical_cols
        }

        explanation_cols = [
            "UDAAP Explanation",
            "CFPB Complaint Explanation",
            "Bank Complaint Explanation",
        ]

        client = AzureOpenAI(
            azure_endpoint="https://tennisfinancecentral.openai.azure.com/",
            api_key="9df14b8a59b04a40b8fbf83216fde843",
            api_version="2024-02-15-preview",
        )

        message_text = [
            {
                "role": "system",
                "content": f"The following is a explaination of each category. -Product Type (CFPB): Type of product related to the complaint, as categorized by the Consumer Financial Protection Bureau (CFPB) -Subproduct Type (CFPB): Subtype of the product related to the complaint. -Issue type (CFPB): Type of issue as categorized by the CFPB. -Complaint Source: Source from which the complaint originated.-Legal Action: Indicates whether legal action was involved (Yes or No). -Resolution Status: Status of the complaint resolution.-Potential UDAAP Complaint: Assessment of potential Unfair, Deceptive, or Abusive Acts or Practices (Yes or No).-Potential CFPB Complaint: Indicates whether there is a potential complaint to the CFPB (Complaint or Inquiries). -Potential Bank Complaint: Indicates whether there is a potential complaint to the bank (Yes or No). Generate a detailed summary of the data summary, highlighting insights, trends, and issues that merit further attention. For Example: We processed 30 complaints. There were 25 complaints indicated that [CLIENT] failed to provide the consumer with requested documentation such as account statements or tax documentation. You may want to look further into these accounts to determine if there is an operational process breakdown or manual error by call center employee(s). Breakdown the summary by the following categories: -Product, Subproduct Types, and Issue Types -Sources,  Legal Actions, and Resolution Status -Complaint Issues. Data summary {categorical_summary} ",
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

    print("Streamlit app is running...")


if __name__ == "__main__":
    main()
