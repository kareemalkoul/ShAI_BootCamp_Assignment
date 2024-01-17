import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io

st.title("Mohammed Kareem Alkoul")
st.header("Data Visualization Section")
# st.subheader("Subsection: Pie Chart Analysis")


@st.cache()
def data():
    return pd.read_csv("./Salaries.csv")


df = data()


st.write(df)


st.header("1.Basic Data Exploration")

st.subheader("1.1.Number of Columns and Rows")
st.write(f"Number of rows: **{len(df.axes[0])}**")
st.write(f"Number of columns: **{len(df.axes[1])}**")


st.subheader("1.2.Types of Columns")
st.write(df.dtypes.astype(str))

st.subheader("1.3.Number check missing value")

st.write("- Non Null values in each columns")
buffer = io.StringIO()
df.info(buf=buffer)
s = buffer.getvalue()

st.text(s)


st.write("- Null values in each columns")
st.write(df.isna().sum())


st.header("2.Descriptive Statistics")

st.subheader("2.1.Calculate basic statistics")
st.write(
    "We can use describe() function to get mutpile statics prameters or use direct declarative function like mean(), median(), ....,etc"
)

st.write(df.TotalPay.describe())


st.header("3.Data Cleaning")

st.subheader("3.1.check Nan values in columns")


st.write(df.isnull().sum() * 100 / len(df))

st.subheader("3.2.Drop Nan values in columns and rows and fill with zero")
st.write(
    "- Because columns `Notes` and `Status` have all values are Nan, Then will be drop it"
)


def clean_data(df):
    clean_df = df.drop(columns=["Notes", "Status"])
    clean_df.JobTitle.replace("", np.nan, inplace=True)
    clean_df.Benefits = clean_df.Benefits.fillna(0)
    clean_df = clean_df.dropna()
    return clean_df


clean_df = clean_data(df)

st.write(clean_df)


st.write("Null values after cleaning")

st.write(clean_df.isnull().sum())


st.subheader("3.3.Drop nagitve values in columns")


def clean_data2(df):
    clean_df = df[(df["BasePay"] > 0) & (df["OvertimePay"] > 0) & (df["TotalPay"] > 0)]
    return clean_df


clean_df = clean_data2(clean_df)

st.write(clean_df.describe())


st.subheader("3.4.Convert JobTitle to LowerCase")


def clean_data3(df):
    df.JobTitle = df.JobTitle.str.lower().str.strip().replace(" ", "", regex=True)
    return df


st.write(f"job Title before convert is: {clean_df.JobTitle.nunique()}")
clean_df = clean_data3(clean_df)
st.write(f"job Title after convert is: {clean_df.JobTitle.nunique()}")


st.header("4.Basic Data Visualization")

st.subheader("4.1.histogram of Salary")


st.pyplot(clean_df.TotalPay.hist(bins=40).figure)


st.subheader("4.2.Pie of Departments")

st.pyplot(
    clean_df["JobTitle"]
    .value_counts()
    .head()
    .plot.pie(label="department", autopct="%1.0f%%")
    .figure
)

st.write("JobTitle with ascending")

st.write(clean_df["JobTitle"].value_counts().sort_values(ascending=False))


st.header("5.Grouped Analysis")


st.write("Sum TotalPay by Year")

st.write(clean_df.groupby("Year")["TotalPay"].sum())


st.write("Sum TotalPay by Year and JobTitle")

st.write(
    clean_df.groupby(["JobTitle", "Year"])["TotalPay"]
    .sum()
    .sort_values(ascending=False)
)


st.write(clean_df.describe())


st.header("6.Simple Correlation Analysis")


correlation = clean_df[["TotalPay", "OvertimePay"]].corr(numeric_only=True)


st.write(correlation)


correlation = clean_df.corr(numeric_only=True)


st.write(correlation)


plt.scatter(clean_df["TotalPay"], clean_df["OvertimePay"])
plt.xlabel("Total Pay")
plt.ylabel("Benefits")
fig, ax = plt.subplots()

st.pyplot(fig)


# st.scatter_chart(clean_df, x="TotalPay", y="OvertimePay")

st.header("7.Summary of Insight")
st.markdown(
    """
- The Data is About Employees' positions and their salaries details for four years 2011,2012,2013 and 2014.
- Data have two dummy columns without values (Nan value) Status and Notes
- The Benefits fill Nan values with Zero
- Drop rows with illogical data like BaseSalary is zero and negative value for fields must be value bigger than zero like salary, overTime and BaseSalary.
- Unification jobTitle string to lowercase
- The data after cleaned it more than half deleted
- Most of the salary is between 75000 and 100000
- About 12% of jobs is Transit Operator
- Most of Paid Salaries is gone to Transit Operator Jobs
- Most Jobs that have large Salary is Assistant Deputy Chief
- Salary and OverTime Have positive Correlation
"""
)
