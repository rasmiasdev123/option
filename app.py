import streamlit as st
from Option import option_chain
import pandas as pd
import time
from streamlit_autorefresh import st_autorefresh

df = None
while df is None:
    try:
        df, ltp = option_chain()
    except:
        print('Got some error trying again...')

df = df.astype(float).round(2)


highest_vol_ce = df['volume_ce'].max()
highest_vol_pe = df['volume_pe'].max()


highest_oi_ce = df['oi_ce'].max()
highest_oi_pe = df['oi_pe'].max()

second_highest_oi_ce = df['oi_ce'].nlargest(2).iloc[-1]
second_highest_oi_pe = df['oi_pe'].nlargest(2).iloc[-1]

second_highest_vol_ce = df['volume_ce'].nlargest(2).iloc[-1]
second_highest_vol_pe = df['volume_pe'].nlargest(2).iloc[-1]

oi_change_abs_ce = df['oiChange_ce'].abs()
oi_change_abs_pe = df['oiChange_pe'].abs()

highest_cng_ce = oi_change_abs_ce.max()
highest_cng_pe = oi_change_abs_pe.max()

# Display the title with the custom background color
page_css = """
    <style>
        #nifty-option-chain{
            background-color:#FFD0D0;
            margin-top:-50px;
            text-align:center;
            color: #40128B;
            border-radius: 10px;
            max-width: 60%;
        }
        .css-1y4p8pa{
            max-width: 90%;
        }
        .css-1629p8f{
            display:flex;
            justify-content:center;
        }
        .green{
            background-color:#2e6a5c;
            color:white;
        }
        .red{
            background-color:#a11110;
            color:white;
        }
        table{
            text-align: center;
        }
        .first{
            background-color:#2e6a5c;
            color: #ffffff;
        }
        .second{
            background-color:#e6ce5f;
        }
        .positive{
            color:#116d6e;
        }
        .negetive{
            color:#a11110;
        }
        .stike{
            background-color:#357683;
            color:white;
        }
        .oi-highest{
            background-color: #F266AB;
            color: white;
        }


    </style>
"""
st.markdown(page_css, unsafe_allow_html=True)
st.title("NIFTY OPTION CHAIN")



# Create the table HTML
table_html = '<table style="width: 100%;margin-top:40px;">'

table_html += "<thead> <th class='green'>OI CHANGE</th>\
                    <th class='green'> OI CHANGE PCT</th>\
                    <th class='green'> OI</th>\
                    <th class='green'> VOLUME</th>\
                    <th class='green'> LTP</th>\
                    <th class='second'> {}</th>\
                    <th class='red'> LTP</th>\
                    <th class='red'> VOLUME</th>\
                    <th class='red'> OI</th>\
                    <th class='red'> OI CHANGE PCT</th>\
                    <th class='red'> OI CHANGE</th>\
                </thead>\
                <tbody> \
                ".format(ltp)

for index, row in df.iterrows():

    if row['strikePrice'] < ltp and row['strikePrice'] + 50 > ltp:
        table_html += "<tr style='border-bottom: red 2px solid;'>"
    else:
        table_html += "<tr>"




    if row['oiChange_ce'] > 0:
        if abs(row['oiChange_ce']) == highest_cng_ce:table_html += '<td class="oi-highest">{}</td>'.format(row['oiChange_ce'])
        else:table_html += '<td class="positive">{}</td>'.format(row['oiChange_ce'])
    else: table_html += '<td class="negetive">{}</td>'.format(row['oiChange_ce'])
    




    if row['pctOiChange_ce'] > 0:
        table_html += '<td class="positive">{}</td>'.format(row['pctOiChange_ce'])
    else:
         table_html += '<td class="negetive">{}</td>'.format(row['pctOiChange_ce'])

    if highest_oi_ce == row['oi_ce']:
        table_html += '<td class="first">{}</td>'.format(row['oi_ce'])
    elif second_highest_oi_ce == row['oi_ce']:
        table_html += '<td class="second">{}</td>'.format(row['oi_ce'])
    else:    
        table_html += '<td>{}</td>'.format(row['oi_ce'])

    if highest_vol_ce == row['volume_ce']:
        table_html += '<td class="first">{}</td>'.format(row['volume_ce'])
    elif second_highest_vol_ce == row['volume_ce']:
        table_html += '<td class="second">{}</td>'.format(row['volume_ce'])
    else:
        table_html += '<td>{}</td>'.format(row['volume_ce'])


    table_html += '<td>{}</td>'.format(row['lastPrice_ce'])

    table_html += '<td class="stike">{}</td>'.format(row['strikePrice'])
    
    table_html += '<td>{}</td>'.format(row['lastPrice_pe'])


    if highest_vol_pe == row['volume_pe']:
        table_html += '<td class="first">{}</td>'.format(row['volume_pe'])
    elif second_highest_vol_pe  == row['volume_pe']:
        table_html += '<td class="second">{}</td>'.format(row['volume_pe'])
    else:
        table_html += '<td>{}</td>'.format(row['volume_pe'])


    if highest_oi_pe == row['oi_pe']:
        table_html += '<td class="first">{}</td>'.format(row['oi_pe'])
    elif second_highest_oi_pe == row['oi_pe']:
        table_html += '<td class="second">{}</td>'.format(row['oi_pe'])
    else:    
        table_html += '<td>{}</td>'.format(row['oi_pe'])

    
    if row['pctOiChange_pe'] > 0:
        table_html += '<td class="positive">{}</td>'.format(row['pctOiChange_pe'])
    else:
        table_html += '<td class="negetive">{}</td>'.format(row['pctOiChange_pe'])
    

    if row['oiChange_pe'] > 0:
        if abs(row['oiChange_pe']) == highest_cng_pe:
            table_html += '<td class="oi-highest">{}</td>'.format(row['oiChange_pe'])
        else:table_html += '<td class="positive">{}</td>'.format(row['oiChange_pe'])
    else:
        table_html += '<td class="negetive">{}</td>'.format(row['oiChange_pe'])
    
    table_html += "</tr>"
table_html += "</tbody></table>"


# Display the table using Streamlit
st.markdown(table_html, unsafe_allow_html=True)



count = st_autorefresh(interval=60000)
