import streamlit as st 
import pandas as pd 
data = { 
'Name':    
['Aisha','Bob','Clara','Dev','Eva','Finn','Grace','Hiro','Ines','Jay'], 
'Math':    
[88, 52, 76, 91, 43, 67, 85, 59, 78, 95], 
'Science': [72, 45, 88, 83, 38, 71, 90, 62, 55, 80], 
'English': [65, 70, 82, 77, 60, 58, 74, 88, 91, 73], 
'Art':     
[90, 85, 60, 55, 78, 92, 68, 75, 83, 61], 
} 
df = pd.DataFrame(data) 
df['Average'] = df[['Math','Science','English','Art']].mean(axis=1).round(1)


st.title('📚 Student Grade Dashboard') 
st.write(f'Showing results for {len(df)} students across 4 subjects.') 
st.markdown('---')

c1, c2, c3, c4 = st.columns(4) 
c1.metric('Class Average', f"{df['Average'].mean():.1f}") 
c2.metric('Highest Score', f"{df['Average'].max():.1f}") 
c3.metric('Lowest Score',  f"{df['Average'].min():.1f}") 
c4.metric('Above 70',      
int((df['Average'] >= 70).sum())) 


st.subheader('All Students') 
def colour_avg(v): 
    if isinstance(v, (int, float)): 
        return 'color:green' if v >= 70 else 'color:red' 
    return '' 
st.dataframe( 
    df.style.map(colour_avg, subset=["Average"]), 
    use_container_width=True, hide_index=True 
)


st.subheader('🏆 Top 3 Students') 
top3 = df.sort_values('Average', ascending=False).head(3).reset_index(drop=True) 
top3.index += 1 
st.table(top3) 


st.subheader('Subject Summary') 
summary = {} 
for subj in ['Math','Science','English','Art']: 
    summary[subj] = { 
    'min':  int(df[subj].min()), 
    'max':  int(df[subj].max()), 
    'mean': round(float(df[subj].mean()), 1) 
} 
st.json(summary) 



st.markdown('---') 
st.caption('Day 2 Project · Student Grade Dashboard · DBI Skill Park') 