import streamlit as st
import pandas as pd
import pickle
import io
import json
from pathlib import Path
from model_final import prepare_dataframe


@st.cache_resource
def load_model():
    model_path = Path(__file__).resolve().parent / 'model_3.pkl'
    with open(model_path, 'rb') as file:
        data = pickle.load(file)
    return data


def get_inr_rate():
    try:
        import requests
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=5)
        return response.json()["rates"]["INR"]
    except Exception:
        return 84


CURRENCY_MAP = {
    "INR": "INR\tIndian rupee",
    "Other": "Other"
}

ORG_SIZE_OPTIONS = {
    '2 to 9 employees': '2 to 9 employees',
    '5,000 to 9,999 employees': '5,000 to 9,999 employees',
    '100 to 499 employees': '100 to 499 employees',
    '20 to 99 employees': '20 to 99 employees',
    '1,000 to 4,999 employees': '1,000 to 4,999 employees',
    '10 to 19 employees': '10 to 19 employees',
    '10,000 or more employees': '10,000 or more employees',
    '500 to 999 employees': '500 to 999 employees',
    'Just me - I am a freelancer, sole proprietor, etc.': 'Just me - I am a freelancer, sole proprietor, etc.',
    "I don't know": "I don\u2019t know"
}

REQUIRED_COLUMNS = [
    'Age', 'AISelect', 'OrgSize', 'DevType',
    'YearsCode', 'WorkExp', 'YearsCodePro',
    'RemoteWork', 'Currency', 'EdLevel',
    'LanguageHaveWorkedWith', 'DatabaseHaveWorkedWith', 'LearnCode'
]

SAMPLE_ROWS = [
    {
        "Age": "25-34 years old", "AISelect": "Yes",
        "OrgSize": "100 to 499 employees", "DevType": "Developer, full-stack",
        "YearsCode": 5, "WorkExp": 4, "YearsCodePro": 3,
        "RemoteWork": "Hybrid (some remote, some in-person)", "Currency": "INR",
        "EdLevel": "Bachelor's degree (B.A., B.S., B.Eng., etc.)",
        "LanguageHaveWorkedWith": "Python;JavaScript",
        "DatabaseHaveWorkedWith": "MySQL;PostgreSQL", "LearnCode": "Online courses;Books"
    },
    {
        "Age": "35-44 years old", "AISelect": "No, and I don't plan to",
        "OrgSize": "1,000 to 4,999 employees",
        "DevType": "Data scientist or machine learning specialist",
        "YearsCode": 10, "WorkExp": 8, "YearsCodePro": 7,
        "RemoteWork": "Remote", "Currency": "Other",
        "EdLevel": "Master's degree (M.A., M.S., M.Eng., MBA, etc.)",
        "LanguageHaveWorkedWith": "Python;R;SQL",
        "DatabaseHaveWorkedWith": "MongoDB;Redis", "LearnCode": "Colleague;Online courses"
    },
    {
        "Age": "18-24 years old", "AISelect": "No, but I plan to soon",
        "OrgSize": "20 to 99 employees", "DevType": "Developer, back-end",
        "YearsCode": 2, "WorkExp": 1, "YearsCodePro": 1,
        "RemoteWork": "In-person", "Currency": "INR",
        "EdLevel": "Some college/university study without earning a degree",
        "LanguageHaveWorkedWith": "Java;Python",
        "DatabaseHaveWorkedWith": "MySQL", "LearnCode": "Online courses"
    }
]


def predict_bulk(df_raw, inr_rate):
    data = load_model()
    model = data["MODEL"]
    label_encoders = data["LABEL_ENCODERS"]
    scaler = data["SCALER"]
    results = []

    for idx, row in df_raw.iterrows():
        try:
            currency_val = str(row.get("Currency", "Other")).strip()
            raw_currency = CURRENCY_MAP.get(currency_val, "Other")
            orgsize_val = str(row.get("OrgSize", "")).strip()
            raw_orgsize = ORG_SIZE_OPTIONS.get(orgsize_val, orgsize_val)

            input_data = {
                'Age': [str(row.get('Age', ''))],
                'AISelect': [str(row.get('AISelect', ''))],
                'OrgSize': [raw_orgsize],
                'DevType': [str(row.get('DevType', ''))],
                'YearsCode': [int(row.get('YearsCode', 0))],
                'WorkExp': [int(row.get('WorkExp', 0))],
                'YearsCodePro': [int(row.get('YearsCodePro', 0))],
                'RemoteWork': [str(row.get('RemoteWork', ''))],
                'Currency': [raw_currency],
                'EdLevel': [str(row.get('EdLevel', ''))],
                'LanguageHaveWorkedWith': [str(row.get('LanguageHaveWorkedWith', ''))],
                'DatabaseHaveWorkedWith': [str(row.get('DatabaseHaveWorkedWith', ''))],
                'LearnCode': [str(row.get('LearnCode', ''))]
            }

            input_df = pd.DataFrame(input_data)
            salary_usd = prepare_dataframe(input_df, model, label_encoders, scaler)[0]

            if "INR" in raw_currency:
                salary_display = salary_usd * inr_rate
                currency_label = "INR"
                salary_str = f"₹{salary_display:,.0f}"
            else:
                salary_display = salary_usd
                currency_label = "USD"
                salary_str = f"${salary_display:,.0f}"

            results.append({
                "Row": idx + 1,
                "Name / ID": row.get("Name", f"Record {idx+1}"),
                "DevType": row.get("DevType", ""),
                "Experience (yrs)": row.get("WorkExp", ""),
                "Currency": currency_label,
                "Predicted Salary": salary_str,
                "Salary (numeric)": round(salary_display, 2),
                "Status": "✅ Success"
            })
        except Exception as e:
            results.append({
                "Row": idx + 1,
                "Name / ID": row.get("Name", f"Record {idx+1}"),
                "DevType": row.get("DevType", ""),
                "Experience (yrs)": row.get("WorkExp", ""),
                "Currency": "",
                "Predicted Salary": "N/A",
                "Salary (numeric)": None,
                "Status": f"❌ Error: {str(e)[:60]}"
            })

    return pd.DataFrame(results)


def show_bulk_scanner_page():
    st.title("🔍 Bulk Salary Scanner")
    st.markdown("### Predict salaries for multiple developers at once")
    st.markdown(
        "Upload a **CSV, Excel, or JSON** file containing developer profiles. "
        "The app will predict the salary for every row and let you download the results."
    )
    st.markdown("---")

    st.markdown("## 1️⃣ Download Sample Templates")
    st.markdown("Not sure about the format? Download a sample file to get started:")

    sample_df = pd.DataFrame(SAMPLE_ROWS)
    col1, col2, col3 = st.columns(3)

    with col1:
        csv_bytes = sample_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📄 Download CSV Sample",
            data=csv_bytes,
            file_name="sample_developers.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col2:
        excel_buffer = io.BytesIO()
        sample_df.to_excel(excel_buffer, index=False, engine='openpyxl')
        st.download_button(
            label="📊 Download Excel Sample",
            data=excel_buffer.getvalue(),
            file_name="sample_developers.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    with col3:
        json_bytes = json.dumps(SAMPLE_ROWS, indent=2).encode("utf-8")
        st.download_button(
            label="📋 Download JSON Sample",
            data=json_bytes,
            file_name="sample_developers.json",
            mime="application/json",
            use_container_width=True
        )

    st.markdown("---")
    st.markdown("## 2️⃣ Upload Your File")

    uploaded_file = st.file_uploader(
        "Choose a file to scan",
        type=["csv", "xlsx", "xls", "json"],
        help="Max 200MB. Supported formats: CSV, Excel (.xlsx/.xls), JSON"
    )

    if uploaded_file is not None:
        st.markdown("---")
        try:
            file_name = uploaded_file.name.lower()
            if file_name.endswith(".csv"):
                df_input = pd.read_csv(uploaded_file)
            elif file_name.endswith((".xlsx", ".xls")):
                df_input = pd.read_excel(uploaded_file)
            elif file_name.endswith(".json"):
                df_input = pd.read_json(uploaded_file)
            else:
                st.error("❌ Unsupported file format.")
                return
        except Exception as e:
            st.error(f"❌ Could not read file: {e}")
            return

        st.markdown("## 3️⃣ Preview Uploaded Data")
        st.info(f"📂 **{uploaded_file.name}** — {len(df_input)} rows, {len(df_input.columns)} columns")
        st.dataframe(df_input.head(5), use_container_width=True)

        missing_cols = [c for c in REQUIRED_COLUMNS if c not in df_input.columns]
        if missing_cols:
            st.error(f"❌ Missing required columns: **{', '.join(missing_cols)}**")
            st.markdown("Please add these columns to your file. Download a sample above for reference.")
            return

        st.success(f"✅ All required columns found! Ready to scan **{len(df_input)}** records.")
        st.markdown("---")
        st.markdown("## 4️⃣ Run Bulk Prediction")

        if st.button("🚀 Start Bulk Scan", type="primary", use_container_width=True):
            inr_rate = get_inr_rate()

            with st.spinner(f"⏳ Predicting salaries for {len(df_input)} records..."):
                results_df = predict_bulk(df_input, inr_rate)

            st.markdown("---")
            st.markdown("## 5️⃣ Results")

            total = len(results_df)
            success = results_df["Status"].str.startswith("✅").sum()
            failed = total - success

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total Records", total)
            m2.metric("✅ Successful", success)
            m3.metric("❌ Failed", failed)

            numeric_salaries = results_df["Salary (numeric)"].dropna()
            if not numeric_salaries.empty:
                avg_label = results_df.loc[results_df["Salary (numeric)"].notna(), "Currency"].iloc[0] if success > 0 else ""
                symbol = "₹" if avg_label == "INR" else "$"
                m4.metric("Average Salary", f"{symbol}{numeric_salaries.mean():,.0f}")
            else:
                m4.metric("Average Salary", "N/A")

            st.dataframe(
                results_df.drop(columns=["Salary (numeric)"]),
                use_container_width=True
            )

            st.markdown("### 📥 Download Results")
            dl1, dl2 = st.columns(2)

            with dl1:
                csv_result = results_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📄 Download Results as CSV",
                    data=csv_result,
                    file_name="salary_predictions.csv",
                    mime="text/csv",
                    use_container_width=True
                )

            with dl2:
                excel_result_buffer = io.BytesIO()
                results_df.to_excel(excel_result_buffer, index=False, engine='openpyxl')
                st.download_button(
                    label="📊 Download Results as Excel",
                    data=excel_result_buffer.getvalue(),
                    file_name="salary_predictions.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

            if failed > 0:
                st.warning(
                    f"⚠️ {failed} record(s) could not be predicted. "
                    "Check the 'Status' column for details and fix those rows."
                )

            st.info("💡 Salaries are estimates based on ML models trained on survey data. Actual compensation may vary.")
