import requests
from bs4 import BeautifulSoup

URL = 'http://course-query.acad.ncku.edu.tw/qry/' 
def get_web_page(url):
	resp = requests.get(url)
	resp.encoding = 'big-5'

	if resp.status_code != 200:
		print('Invalid url:', resp.url)
		return None
	else:
		return resp.text

def get_articles(dom):
	soup = BeautifulSoup(dom, 'html.parser')

	articles = []  # 儲存取得的文章資料
	divs = soup.find_all('div', 'dept')
	for d in divs:
		if d.find('a'):
			title = d.find('a').string
			href = d.find('a')['href']
			articles.append({
				'title': title,
				'href':URL + href
			})
	return articles

if __name__ == "__main__":
	page = get_web_page('http://course-query.acad.ncku.edu.tw/qry/')
	if page:
		current_articles = get_articles(page)
		for post in current_articles:
			print(post)