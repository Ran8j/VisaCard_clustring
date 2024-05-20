import streamlit as st
import pandas as pd 
import plotly.express as px




# import data       

df = pd.read_csv("bst_model.csv")
df['Is Enough'] = df['IsEnough'].map({1: 'Yes', 0: 'No'})
df['would repay'] = df['repay'].map({1: 'Yes', 0: 'No'})
df['Monthly'] = df['IsMonthly'].map({1: 'Yes', 0: 'No'})
df['type Of Commitment'] = df['typeOfCommitment'].map({2: 'Nonessentials', 3: 'University ',1:'Housing ',0:'Electronics',4:'Transportation'})
df['Quarter'] = df['quarter'].map({1: 'Middle quarter', 0: 'First quarter',2:'Last quarter'})
df['Payback Amount'] = df['PaybackAmou'].map({0: '100-300', 1: '300-600',2:'600-900'})
df['Cluster State'] = df['Cluster'].map({1: 'Lock', 0: 'Unlock'})




futures=df.drop(columns=['Cluster']).columns
avr_df=df.groupby('Cluster')
catigrical_futures_bar=df[['Is Enough','would repay','Monthly','type Of Commitment','Quarter','Payback Amount']].columns
catigrical_futures_pie = df[['type Of Commitment', 'Payback Amount']].columns






# page setting 

st.set_page_config(page_title="MLProject",page_icon=":bar_chart:",layout="wide")
st.image("visacard.png")
st.title(" Student Visa Card :credit_card: :bar_chart: ")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
st.subheader("Overview analysis about the dataset")
#st.text("Overview analysis about the dataset")






# Add an image before displaying the chart
st.sidebar.markdown("### Explore more :")
catigrical_future_bar_show= st.sidebar.selectbox(" For Additional analysis with Bar Chart", catigrical_futures_bar)
avr_catogrical_bar = df.groupby(['Cluster State', catigrical_future_bar_show]).size().reset_index(name='Count')




container = st.container()



chart1, chart2 = container.columns(2)


with chart1:
    st.expander("Relation between typeOfCommitment and SpendingAmount")
    region = df.groupby(by="type Of Commitment")["SpendingAmount"].mean().round(1).reset_index()  # Group by "typeOfCommitment" and calculate the mean of "SpendingAmount"
    region["SpendingAmount"] = region["SpendingAmount"].astype(str).str.rstrip('0').str.rstrip('.')  # Convert to string and remove trailing zeros and decimal points
    region.set_index("type Of Commitment", inplace=True)  # Set "typeOfCommitment" as the index
    st.write(region.style.background_gradient(cmap="pink"))



with chart2:
    st.expander(" Type Of Commitment WITH quarters ")
    # Create the pivot table
    sub_category_Year = pd.pivot_table(data=df, values="SpendingAmount", index="Quarter", columns="type Of Commitment")
    
    # Round the values to one decimal place
    sub_category_Year = sub_category_Year.round(1)
    
    # Convert the rounded values to strings and remove trailing zeros and decimal points
    sub_category_Year = sub_category_Year.astype(str).apply(lambda x: x.str.rstrip('0').str.rstrip('.'))
    
    # Display the pivot table with background gradient
    st.write(sub_category_Year.style.background_gradient(cmap="pink"))



chart3, chart4 = container.columns(2)
   
with chart3:
    average_spending_by_category = df.groupby('typeOfCommitment')['SpendingAmount'].mean().reset_index()
    fig = px.bar(average_spending_by_category, x='typeOfCommitment', y='SpendingAmount',
                labels={'typeOfCommitment': 'Type of Commitment', 'SpendingAmount': 'Average Spending Amount'},
                title='Average Spending Amount by type of Commitment', color='typeOfCommitment')
    fig.update_layout(xaxis_tickangle=-45)  # Rotate x-axis labels for better readability
    st.plotly_chart(fig, use_container_width=True)

with chart4:
    # Reset index to make 'quarter_text' a column
    sub_category_Year.reset_index(inplace=True)
    melted_df = pd.melt(sub_category_Year, id_vars='Quarter', var_name='Type of Commitment', value_name='Spending Amount')
    fig = px.bar(melted_df, x='Type of Commitment', y='Spending Amount', color='Quarter',
                 labels={'Quarter': 'Quarter', 'Spending Amount': 'Spending Amount'},
                 title='Relationship between spendind amount and type of Commitment base on the quarters', barmode='group')
    fig.update_layout(xaxis=dict(title='Type Of Commitment'), yaxis=dict(title='Spending Amount'))
    st.plotly_chart(fig, use_container_width=True)




chart6,chart7= container.columns(2)

with chart6:
    avr_df2 = df.groupby('Cluster State').size().reset_index(name='count')
    fig = px.bar(avr_df2, x='Cluster State', y='count', title='Cluster Counts', labels={'Cluster state': 'Cluster', 'count': 'Count'})
    st.plotly_chart(fig, use_container_width=True)




with chart7:
    fig1 = px.bar(avr_catogrical_bar, x='Cluster State', y='Count',  title='Additional analysis with Bar Chart',color=catigrical_future_bar_show, barmode='group', template="plotly_dark")
    st.plotly_chart(fig1, use_container_width=True)






#tree
    # Create a treem based on Region, category, sub-Category
st.subheader("Hierarchical view of futures using TreeMap")
fig3 = px.treemap(df, path = ["Cluster State","Quarter","Payback Amount"], values = "SpendingAmount",hover_data = ["SpendingAmount"],
                    color = "Payback Amount")
fig3.update_layout(width = 800, height = 650)
st.plotly_chart(fig3, use_container_width=True)




