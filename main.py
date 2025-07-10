import streamlit as st
import mysql.connector as sql
from fpdf import FPDF
import datetime
my_db=sql.connect(host="localhost",user="admin",password="root",database="pay")
st.title("IKON COMPUTER EDUCATION & TRAINING INSTITUTE")
st.subheader("payment section")
name=st.text_input("Name ")
registration_number=st.text_input("Registration number")
option=st.selectbox("Choose payment Mode",["choose option","Bank Transfer","UPI"])
def create_pdf(pdf_data):
    pdf=FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt="Payment Receipt", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", "", 12)
    for key, value in pdf_data.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

    filename = f"invoice_{pdf_data['registration number']}.pdf"
    pdf.output(filename)
    st.success(f"✅ PDF generated and saved as {filename}")
    with open(filename, "rb") as file:
        st.download_button(
            label="📥 Download PDF",
            data=file,
            file_name=filename,
            mime="application/pdf"
        )
    


def add_data(name,registration_number,option):
    cur=my_db.cursor()
    data=[name,registration_number,option]
    cur.execute("insert into payment(name,registration_number,payment_type,time_of_payment)values(%s,%s,%s,now())",data)
    my_db.commit()
    pdf_data={
        "name" :name,
        "registration number":registration_number,
        "payment type":option,
        "time of payment":datetime.datetime.now()
    }
    create_pdf(pdf_data)
if st.button("Submit"):
    add_data(name,registration_number,option)