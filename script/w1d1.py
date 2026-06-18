
# day01_project.py — Personal Profile Card
import streamlit as st
st.title('👤 Alex Johnson')
st.header('About Me', divider='blue')
st.markdown('I am a first-year student learning **data analytics** with Python and Streamlit. '
            'I enjoy working with real datasets and building interactive dashboards.'
            )
st.latex(r'\text{Profit Margin} = \frac{\text{Profit}}{\text{Sales}} \times 100')
st.markdown('---')
st.header('Skills', divider='green')
st.markdown(
 '- **Python** — pandas, NumPy, Matplotlib'
 '\n- Streamlit dashboard development'
 '\n- SQL and relational databases'
 '\n- Data cleaning and exploratory analysis'
 '\n- :green[Growing skill]: Machine Learning basics'
)
st.subheader('Favourite Code Snippet', help='A pattern I use all the time')
st.code('''
import pandas as pd
df = pd.read_csv('data/sales.csv')
print(df.shape) # rows, cols
print(df.describe()) # quick stats
''', language='python')
st.markdown('---')
st.header('Contact', divider='orange')
st.write({'Email': 'alex@example.com', 'GitHub': 'github.com/alexj', 'City':
'Kozhikode, Kerala'})
st.markdown('---')
st.caption('Built with Streamlit · Day 1 Project · 2024')