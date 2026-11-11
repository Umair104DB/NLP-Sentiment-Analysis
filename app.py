import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score,classification_report
st.set_page_config(page_title='Sentiment Insights',page_icon='💬',layout='wide')
st.title('💬 Sentiment Analysis Studio')
st.caption('TF-IDF + Logistic Regression on a labelled review practice dataset.')
df=pd.read_csv(Path(__file__).parent/'data/reviews_100_rows.csv')
Xtr,Xte,ytr,yte=train_test_split(df.review_text,df.sentiment_label,test_size=.25,random_state=42,stratify=df.sentiment_label)
model=Pipeline([('tfidf',TfidfVectorizer(ngram_range=(1,2),stop_words='english')),('clf',LogisticRegression(max_iter=1000))]).fit(Xtr,ytr)
pred=model.predict(Xte)
a,b,c=st.columns(3); a.metric('Reviews',len(df)); b.metric('Test accuracy',f'{accuracy_score(yte,pred):.1%}'); c.metric('Labels',df.sentiment_label.nunique())
st.plotly_chart(px.histogram(df,x='sentiment_label',color='sentiment_label',title='Sentiment distribution'),use_container_width=True)
st.dataframe(df,use_container_width=True)
text=st.text_area('Enter a review to analyse',placeholder='Write a product review...')
if st.button('Analyse sentiment',type='primary'):
    if len(text.strip())<3: st.warning('Enter a little more text.')
    else: st.success(f'Predicted sentiment: {model.predict([text])[0].title()}')
st.subheader('Evaluation'); st.text(classification_report(yte,pred))
st.info('The 100 reviews are short synthetic examples. This model is a learning baseline, not a reliable measure of public opinion. Use a larger, representative and properly licensed dataset for real analysis.')
