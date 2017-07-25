import pytest


@pytest.fixture
def page_content():
    return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="X-UA-Compatible" content="ie=edge">
            <title>Document</title>
        </head>
        <body>
            <p>Lorem ipsum <span>Навальный</span> dolor sit amet, <a href="https://yandex.ru/blog/yandexbrowser">consectetur adipiscing elit</a>. Quisque eleifend ex vel ligula maximus, 
            sed finibus ex feugiat. In consectetur diam at Путина tellus pulvinar, <a href="blog/yandexbrowser?year=2013&month=Dec">neque arcu facilisis</a> eget dignissim nisl efficitur. 
            <a href="https://yandex.ru/blog/yandexbrowser?year=2013&month=Nov">Nunc a quam sed erat luctus</a> maximus aliquet nec ante. Fusce ipsum diam, gravida a semper a, sollicitudin sit amet lacus.</p> 
            <p>Proin cursus, sapien sed facilisis maximus, димон eros, nec semper urna в путь dolor vel lacus. Vestibulum mattis <a href="//yandex.ru/blog/yandexbrowser?year=2013&month=Oct">erat quis</a>
            sagittis rutrum. Nunc fermentum медвепут justo tincidunt tempor навальному blandit <strong>уточка</strong>. <a href="/blog/yandexbrowser?year=2013&month=Sep">уточка Suspendisse</a> hendrerit sagittis euismod.</p> 
        </body>
        </html>
        """


@pytest.fixture
def html_text():
    return """Lorem ipsum Навальный dolor sit amet, consectetur adipiscing elit . Quisque eleifend ex vel ligula maximus, sed finibus ex feugiat. In consectetur diam at Путина tellus pulvinar, neque arcu facilisis eget dignissim nisl efficitur. Nunc a quam sed erat luctus maximus aliquet nec ante. Fusce ipsum diam, gravida a semper a, sollicitudin sit amet lacus. Proin cursus, sapien sed facilisis maximus,  димон eros,
            nec semper urna в путь dolor vel lacus. Vestibulum mattis erat quis sagittis rutrum. Nunc fermentum медвепут justo tincidunt tempor навальному blandit уточка . уточка Suspendisse hendrerit sagittis euismod."""


@pytest.fixture
def words_dict():
    return {
        "0": ["путин", "путина", "путиным"],
        "1": ["уточка", "медведев", "димон"],
        "2": ["навальный", "навального", "навальному"]
    }


@pytest.fixture
def words_list():
    return ['lorem', 'ipsum', 'навальный', 'dolor', 'amet', 'consectetur', 'adipiscing', 'elit', 'quisque', 
            'eleifend', 'ligula', 'maximus', 'finibus', 'feugiat', 'consectetur', 'diam', 'путина', 'tellus', 
            'pulvinar', 'neque', 'arcu', 'facilisis', 'eget', 'dignissim', 'nisl', 'efficitur', 'nunc', 'quam', 
            'erat', 'luctus', 'maximus', 'aliquet', 'ante', 'fusce', 'ipsum', 'diam', 'gravida', 'semper', 
            'sollicitudin', 'amet', 'lacus', 'proin', 'cursus', 'sapien', 'facilisis', 'maximus', 'димон', 
            'eros', 'semper', 'urna', 'путь', 'dolor', 'lacus', 'vestibulum', 'mattis', 'erat', 'quis', 'sagittis', 
            'rutrum', 'nunc', 'fermentum', 'медвепут', 'justo', 'tincidunt', 'tempor', 'навальному', 'blandit', 
            'уточка', 'уточка', 'suspendisse', 'hendrerit', 'sagittis', 'euismod']
