from api import Text2ImageAPI
from config_reader import config
# from bs import BeautifulSoup
import pandas as pd
import asyncio

async def generate(date, wof, place, aspect):

    date_from = 0
    date_to = 0
    from_place = True
    width = 0
    height = 0
    
    # Соотношение сторон
    if aspect == '16:9':
        width = 1024
        height = 576
    if aspect == '1:1':
        width = 1024
        height = 1024
    if aspect == '9:16':
        width = 576
        height = 1024

    # TODO: получение ключевых слов
    # table = pd.read_excel('data.xlsx')
    # df.loc['1910-01-01':'1912-01-01']

    # from_country = df.loc[]

    # Парсим страницу открытки на теги (А БЫЛО БЫ НАМНОГО ЛУЧШЕ ЕСЛИ
    # БЫ У НИХ БЫЛ ХОТЯ БЫ КАКОЙ-ТО API) PS: ((я не успел))
    # url = 'https://pishutebe.ru/card/74/'
    # response = requests.get(url)
    
    # bs = BeautifulSoup(response.text,"lxml")

    # tags = bs.find('div', 'postcard-tags')
    # print(tags.text) :sob:
    
    api = Text2ImageAPI(
        'https://api-key.fusionbrain.ai/',
        config.api_token.get_secret_value(),
        config.secret_api_token.get_secret_value()
    )

    prompt = date
    if wof == 'Куда':
        prompt += ' в '
    else:
        prompt += ' из '

    prompt += place
    # prompt += f' из {from_country}'

    print(prompt)
    
    model_id = await api.get_model()
    uuid = await api.generate(
        prompt, # TODO: промпт
        model_id,
        1, # может генерировать только одно изображение за запрос (API)
        width,
        height
    ) 
    images = await api.check_generation(uuid)
    return images