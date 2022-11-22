import requests
import json
import datetime
import pandas as pd

MAXIMAL_RETRY = 3

# call with token
def response(url, postdata, token):
    #headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11'}
    headers = {'Authorization': "Bearer {0}".format(token)}
    res = requests.post(url=url, data=postdata, headers=headers)
    resposn = res.json()
    return resposn

        

def response_with_retry(url, postdata, token, times):
    #time.sleep(1)
    try:
        return response(url, postdata, token)
    except Exception as e:
        if times >= MAXIMAL_RETRY:
            print(f'>> Exceed maximal retry {MAXIMAL_RETRY}, Raise exception...')
            raise(e) # will stop the program without further handling
        else:
            times += 1
            print(f'>> Exception, Retry {times} begins...')
            return response_with_retry(url, postdata, token, times)

# call todoist dev api to get activity of completed tasks
# refer https://developer.todoist.com/sync/v9/#activity
def todoist_completed_activity(token, page, limit, offset):
    data = {"event_type":"completed", "page":page, "limit":limit, "offset": offset}
    url = "https://api.todoist.com/sync/v9/activity/get"
    re = response_with_retry(url, data, token, 1)
    return re

# json expect to be list of events format
# with event_date, event_type, id 
def normalize_df(jsondata):
    if jsondata["count"] == 0:
        return pd.DataFrame(columns = ["event_date", "event_type", "id"])
    df = pd.json_normalize(jsondata["events"])
    df = df[["event_date", "event_type", "id"]]
    df['event_date'] = df['event_date'].str.slice(0, 10)
    return df

# current only support to generate current calendar year
def get_current_year(token):
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    number_of_days = datetime.date.today().timetuple().tm_yday
    pages = number_of_days // 7 + 1
    first_day_of_year = datetime.datetime(datetime.datetime.now().year, 1,1).strftime('%Y-%m-%d')

    df = pd.DataFrame(columns = ["event_date", "event_type", "id"])
    for page in range(0, pages + 1):
        offset = 0
        limit = 100
        while True:
            res = todoist_completed_activity(token, page, limit, offset)
            if res["count"] >= offset:
                offset = offset + limit
                df_res = normalize_df(res)
                df = pd.concat([df, df_res])
            else:
                break
    # in case last week page is beyond first day of the year.
    df = df[df['event_date'] >= first_day_of_year] 
    return df

def count_by_date(df):
    return df.groupby(['event_date'])['event_date'].count()

if __name__ == "__main__":
    print(datetime.datetime.now())
    token = ''
    
    df = get_current_year(token)

    df_2 = count_by_date(df)
    print(df_2)

    
