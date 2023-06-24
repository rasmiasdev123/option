import requests
import pandas as pd

def option_chain():

    baseurl = "https://www.nseindia.com/"
    url = f"https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                            'like Gecko) '
                            'Chrome/80.0.3987.149 Safari/537.36',
            'accept-language': 'en,gu;q=0.9,hi;q=0.8', 'accept-encoding': 'gzip, deflate, br'}
    session = requests.Session()
    request = session.get(baseurl, headers=headers, timeout=5)
    cookies = dict(request.cookies)
    response = session.get(url, headers=headers, timeout=5, cookies=cookies)
    # print(response.json())

    data = response.json()
    exp_date = data['records']['expiryDates'][0]

    ce = []
    pe = []
    
    ltp = 0
    try:
        ltp = data['records']['data'][0]['CE']['underlyingValue']
    except:
        ltp = data['records']['data'][0]['PE']['underlyingValue']

    near_stike = round(ltp / 50) * 50
    data = data['records']['data']
    for i in data:
        
        if i['expiryDate'] == exp_date:
    
            if 'PE' in i and 'CE' in i:
                CE = i['CE']
                PE = i['PE']

                ce.append(CE)
                pe.append(PE)

    ce_df = pd.DataFrame(ce)
    ce_df = ce_df[['strikePrice', 'openInterest', 'changeinOpenInterest','pchangeinOpenInterest', 'totalTradedVolume', 'lastPrice']]
    ce_df.rename(columns={'strikePrice':'strikePrice','changeinOpenInterest': 'oiChange' ,'openInterest':'oi', 'pchangeinOpenInterest':'pctOiChange', 'totalTradedVolume':'volume'}, inplace=True)
    pe_df = pd.DataFrame(pe)
    pe_df = pe_df[['strikePrice', 'openInterest','changeinOpenInterest' ,'pchangeinOpenInterest', 'totalTradedVolume', 'lastPrice']]
    pe_df.rename(columns={'strikePrice':'strikePrice','changeinOpenInterest':'oiChange' ,'openInterest':'oi', 'pchangeinOpenInterest':'pctOiChange', 'totalTradedVolume':'volume'}, inplace=True)


    merged_df = pd.merge(ce_df, pe_df, on='strikePrice', suffixes=('_ce', '_pe'))
    chain = merged_df[['oi_ce', 'oiChange_ce', 'pctOiChange_ce', 'volume_ce', 'lastPrice_ce', 'strikePrice','lastPrice_pe' , 'volume_pe', 'pctOiChange_pe', 'oiChange_pe','oi_pe']]
    target_index = chain[merged_df['strikePrice'] == near_stike].index[0]

    start_index = max(target_index - 10, 0)
    end_index = min(target_index + 10 + 1, len(chain))

    selected_rows = merged_df.iloc[start_index:end_index]
    final = selected_rows[['oi_ce', 'oiChange_ce', 'pctOiChange_ce', 'lastPrice_ce', 'volume_ce', 'strikePrice', 'volume_pe','lastPrice_pe' ,'pctOiChange_pe','oiChange_pe','oi_pe']]
    return final, ltp
