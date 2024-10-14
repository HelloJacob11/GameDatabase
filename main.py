import requests
from bs4 import BeautifulSoup
import pandas as pd
def get_data(url):
    data_result = pd.DataFrame({'title':[],'question':[],'answer':[]})
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"}
    response = requests.get(url,headers=header)  
    idx = 0 
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        frame = soup.find("ol",class_="discussionListItems")
        items = frame.find_all('li',class_="discussionListItem visible")
        for item in items:
            data = item.find('a',class_='PreviewTooltip')
            new_url = f"https://forums.playredfox.com/{data['href']}"
            #print(new_url)
            response = requests.get(new_url,headers=header)   
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')      
                title_frame = soup.find("div",class_="titleBar")
                title = title_frame.find('h1')
                t_text = title.text
                q_text = []
                table = soup.find('ol',class_="messageList")
                contents = table.find_all('li','message')
                for content in contents:
                    text_content = content.find('div','messageContent')
                    q_text.append(text_content.text)
                
                ans_contents = table.find_all('li',class_='message staff')
                a_text = []
                if len(ans_contents) >0:
                    #print('ans_data')
                    for content in ans_contents:
                        text_content = content.find('div','messageContent')
                        remove_content = content.find('div','bbCodeBlock bbCodeQuote')
                        a_text.append(text_content.text.replace(remove_content.text,''))
                data_result.loc[idx] = [t_text,' '.join(q_text),' '.join(a_text)]
                idx += 1
    return data_result
    
            
        

if __name__ == "__main__":
    ans = pd.DataFrame({})
    for i in range(1,5):
        print(f"Get start page {i}")
        new_result = get_data(f"https://forums.playredfox.com/index.php?forums/general-discussion.12/page-{i}")
        ans = pd.concat([ans,new_result])
        print(f"add page{i}")
    ans.to_excel('RedFoxGame.xlsx',index=False)
    print('Save file')