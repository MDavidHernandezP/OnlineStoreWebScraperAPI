import requests

def get_robots_txt(url):
    if not url.startswith('http'):
        url = 'http://' + url
    if not url.endswith('/'):
        url += '/'
    try:
        response = requests.get(url + 'robots.txt')
        response.raise_for_status()  # Esto asegura que se lance una excepción si la respuesta no es exitosa
        return response.text
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error: {err}")
    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")

robots_content = get_robots_txt('https://es.aliexpress.com/w/wholesale-Conjuntos-de-pantalones.html?spm=a2g0o.categorymp.0.0.3070VOVmVOVmfM&categoryUrlParams=%7B%22q%22%3A%22Conjuntos%20de%20pantalones%22%2C%22s%22%3A%22qp_nw%22%2C%22osf%22%3A%22category_navigate%22%2C%22sg_search_params%22%3A%22on___%2528%2520prism_tag_id%253A%25271000333116%2527%2520%2529%22%2C%22guide_trace%22%3A%22e3d642f6-e6eb-4ca1-a57c-d008fd7c5ef3%22%2C%22scene_id%22%3A%2232124%22%2C%22searchBizScene%22%3A%22openSearch%22%2C%22recog_lang%22%3A%22es%22%2C%22bizScene%22%3A%22category_navigate%22%2C%22guideModule%22%3A%22category_navigate_vertical%22%2C%22postCatIds%22%3A%22200000345%2C320%2C301%2C200000532%2C200001894%22%2C%22scene%22%3A%22category_navigate%22%7D&isFromCategory=y')  # Reemplaza con la URL real
print(robots_content)
