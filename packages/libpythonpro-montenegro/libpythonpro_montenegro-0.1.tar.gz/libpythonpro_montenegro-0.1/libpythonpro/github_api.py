import requests


def buscar_avatar(usuario):
    """
    Busca o avatar do usuario do github-Imagem do usuario
    :param usuatio: str nome de usuario no github
    :return: str com o link do avatar
    """
    url = f'https://api.github.com/users/{usuario}'

    resp = requests.get(url)
    return resp.json()['avatar_url']


if __name__ == '__main__':
    print(buscar_avatar('79Aniro'))
