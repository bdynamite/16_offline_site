from bs4 import BeautifulSoup
import requests
import os


def get_html():
    with open('index.html', 'r') as index:
        html_code = index.read()
        return html_code


def get_all_links(html_code):
    all_links = []
    soup = BeautifulSoup(html_code, 'html.parser')
    all_links.extend(get_all_href(soup))
    all_links.extend(get_all_src(soup))
    return all_links


def get_all_href(soup):
    links = soup.find_all(href=True)
    return [x.attrs['href'] for x in links]


def get_all_src(soup):
    links = soup.find_all(src=True)
    return [x.attrs['src'] for x in links]


def get_data(urls):
    urls_with_content = []
    for url in urls:
        try:
            responce = requests.get(url)
            urls_with_content.append([url, responce.content])
        except requests.exceptions.MissingSchema:
            continue
    return urls_with_content


def create_local_data(remote_data):
    for element in remote_data:
        file_name = element[0].split('/')[-1]
        file_dir = file_name.split('.')[-1]
        new_file_name = os.path.join(file_dir, file_name)
        with open(new_file_name, 'wb') as new_file:
            new_file.write(element[1])
        element.append(new_file_name)
    return remote_data


def change_html(html, local_data):
    for element in local_data:
        html = html.replace(element[0], element[2])
    with open('index.html', 'w') as new_html:
        new_html.write(html)


def print_result():
    print('Now you have offline version index.html')


if __name__ == '__main__':
    html = get_html()
    all_links = get_all_links(html)
    links_with_data = get_data(list(all_links))
    links_with_local_data = create_local_data(list(links_with_data))
    change_html(html, links_with_local_data)
    print_result()
