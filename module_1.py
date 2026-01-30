import requests



def get_website_html(url):
    response = requests.get(url)
    return response.text

    # Example usage:
    # html = get_website_html("https://www.example.com")
    # print(html)

if __name__ == "__main__":
    print("hello, world")
    print (get_website_html("https://www.baidu.com"))