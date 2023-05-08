import streamlit as st
import pandas as pd
import os
import subprocess
import base64
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
def parp1(ic50_parp1):
    return (1 / (1 + np.exp(0.22*(ic50_parp1-27.5)))) * ((1 - 0.1) + 0.1)
def parp2(ic50_parp2):
    return (1 / (1 + np.exp(0.0204*(ic50_parp2-255)))) * ((1 - 0.1) + 0.1)
def tankyrase(ic50_tankyrase):
    return (1 / (1 + np.exp(-0.0034*(ic50_tankyrase-1550)))) * ((1 - 0.1) + 0.1)
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
#local_css("theme.css")
local_css("style.css")
def run_app(input_file):
    command = ["python", "app.py", "--input_file", input_file]
    subprocess.run(command)
def main():
    banner = "banner.png"
    st.image(banner, use_column_width=True)
    st.markdown("<h1 style='text-align: center; font-family: Times New Roman; font-size: 22px;'>This Web Server allows the multiparameter optimization that includes on-target potency, off-target potency, CYP-3A4 and hERG inhibition. It will classify inhibitors into desirable and undesirable considering multiple parameters.  If you have any questions or problems, please use the contact form below.</h1>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    with st.container():
        st.write("---")
        left_column, right_column = st.columns(2)
        with left_column:
               st.subheader("Instructions for the input file")
               st.write(
             """
            - Prepare the input .CSV file with the same column headers as given in image in the right.
            - The potency are given in nM only.
            - Texts in the header are case sensitive.
            - If any problem persists please write us in the contact form below.
            - For more information and citing us please follow the link given below.
             """
            )
               st.write("[Click here>](https://doi.org/10.1016/j.ejmech.2023.115300)")
        with right_column:
            st.image("input.png", use_column_width=True)
            st.markdown(
              """
              Developed by : 
              Krishan Dev Singh (MS Scholar)
              and Bhakti Hirlekar (PhD. Scholar)\n
              Supervised by: Dr. Vaibhav A. Dixit      
              Assistant Professor Dept. of Medicinal Chemistry
        """ )     
    if uploaded_file is not None:
        uploaded_file.name = "input.csv"
        with open("input.csv", "wb") as f:
            f.write(uploaded_file.getbuffer())
        run_app("input.csv")
        if os.path.exists("output.csv"):
            df = pd.read_csv("output.csv")
            st.write(df)
            st.download_button(
                label="Download Output CSV",
                data=df.to_csv(index=False),
                file_name="output.csv",
                mime="text/csv",
            )
            submit_button = st.button('Sigmoidal plots')
        for index, row in df.iterrows():
            UF_parp1 = parp1(row['IC50_parp1'])
            UF_parp2 = parp2(row['IC50_parp2'])
            UF_tankyrase = tankyrase(row['IC50_tankyrase'])
            df.loc[index, 'S_parp1'] = UF_parp1
            df.loc[index, 'S_parp2'] = UF_parp2
            df.loc[index, 'S_tankkyrase'] = UF_tankyrase
        df.to_csv('plots.csv', index=False)
        fig, axs = plt.subplots(1, 3, figsize=(15, 5))
        for index, ax in enumerate(axs):
            if index == 0:
                x = df['IC50_parp1']
                y = df['S_parp1']
                label = 'PARP1'
                sigmoid_func = parp1
                xlabel = 'IC50_parp1'
            elif index == 1:
                x = df['IC50_parp2']
                y = df['S_parp2']
                label = 'PARP2'
                sigmoid_func = parp2
                xlabel = 'IC50_parp2'
            else:
                x = df['IC50_tankyrase']
                y = df['S_tankkyrase']
                label = 'Tankyrase'
                sigmoid_func = tankyrase
                xlabel = 'IC50_tankyrase'
            ax.plot(np.linspace(min(x), max(x), 100), sigmoid_func(np.linspace(min(x), max(x), 100)), color='black', label='Sigmoid Curve')
            ax.scatter(x, y, label=label)
            ax.set_xlabel(xlabel)
            ax.set_ylabel('UF')
            ax.set_title(label)
            ax.legend()
            for i, txt in enumerate(df['ID']):
              ax.annotate(txt, (x[i], y[i]))
        if submit_button:
            st.pyplot(fig)
        with st.container():
              st.write("---")
              st.header("For Contacts")
              st.write("#")   
        contact_form = """
        <form action="https://formsubmit.co/vaibhav@niperguwahati.in" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email" required>
        <textarea name="message" placeholder="Your message here" required></textarea>
        <button type="submit">Send</button>
        </form>
                """
        left_column, right_column = st.columns(2)
        with left_column:
          st.markdown(contact_form, unsafe_allow_html=True)
        with right_column:
          st.markdown("<h5>Sponsored/Funded By:<h5>", unsafe_allow_html=True)
          st.markdown("""Ministry of Electronincs and Information Technology (Meity)""" )
          st.image("input1.png", use_column_width=True)
if __name__ == "__main__":
    main()
