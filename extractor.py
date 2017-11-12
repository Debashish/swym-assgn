from bs4 import BeautifulSoup
import requests
import json
import pprint
import sys

def get_html(url):

	# Get the html document

	headers = {"user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"}
	s = requests.get(url)
	html_doc =  s.text
	return html_doc

def find_new_images(html_doc):

	# find new images for instagram, that are related to the product

	soup = BeautifulSoup(html_doc, 'html.parser')

	title = soup.title.string

	print title

	l = soup.find_all('h1')
	prod_name = l[0].text
	prod_name = "".join(prod_name.split(' ')[:2])

	instagram_query = "https://www.instagram.com/explore/tags/"+prod_name+"/?hl=en"
	print instagram_query
	html_doc = get_html(instagram_query)

	img_lst = html_doc.split('window._sharedData =')[1].split(';</script>')[0]
	d = json.loads(img_lst.strip())
	lst = []
	for key in d.keys():
		# print key
		if 'entry_data' in key:
			node_lst = d['entry_data']['TagPage'][0]['tag']['media']['nodes']
			for item in node_lst:
				for img in item['thumbnail_resources']:
					lst.append(img['src'])
	return lst

def find_missing_elements(texts):

	# Find if important elements are missing

	dct = {}

	if "Rating" or "rating" in texts:
		dct['rating'] = True
	else:
		dct['rating'] = False
		
	if "Reviews" or "reviews" in texts:
		dct['reviews'] = True
	else:
		dct['reviews'] =False

	if "Questions" or "questions" or "answers" or "Answers" or "answered" in texts:
		dct['questions'] = True
	else:
		dct['questions'] = False

	if "Warranty" or "warranty" in texts:
		dct['warranty'] = True
	else:
		dct['warranty'] = False

	return dct

def tag_extractor(element):

	# Remove the below tags before finding the text

	if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
		return False
	return True

def text_from_html(body):

	# Get visible text on the product detail page

	soup = BeautifulSoup(html_doc, 'html.parser')
	texts = soup.findAll(text=True)
	visible_texts = filter(tag_extractor, texts)  
	return u" ".join(t.strip() for t in visible_texts)


if __name__ == '__main__':

	url = sys.argv[1]
	try:
		html_doc = get_html(url)
		texts = text_from_html(html_doc)
		insta_img_lst = find_new_images(html_doc)

		elements_missing = find_missing_elements(texts)

		list_elements = []

		for key, val in elements_missing.items():

			if val == False:
				list_elements.append(key)

		if len(list_elements) != 0:

			print "This information on website can enrich the data: ", list_elements

		print "This images can enhance the user engagement: ", insta_img_lst[:10]
	except Exception as e:

		print "Some error occured:", e








