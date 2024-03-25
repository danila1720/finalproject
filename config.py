IAM_TOKEN = 't1.9euelZqczZPHkYmclpqZisySyMuNj-3rnpWak5CajcaXmJCVjIqejomXlcvl8_dHInpP-e92XD44_N3z9wdRd0_573ZcPjj8zef1656VmpSejZHMks2Pxp2Sx5eaz87L7_zF656VmpSejZHMks2Pxp2Sx5eaz87LveuelZqRi5yZk8fHkMqVkJ2ZlYqPirXehpzRnJCSj4qLmtGLmdKckJKPioua0pKai56bnoue0oye.qM4jgFGLOt3x1FwfTo1dRxgtN_MxjiOMVfJK8NpBKqM6uXkPIprgpS3qqW4xTRCpk-wAHj6fF4WfPigNxOZoAQ'
FOLDER_ID = 'b1g0ekt4tgcnufeo84p3'
GPT_MODEL = 'yandexgpt-lite'

CONTINUE_STORY = 'Продолжи сюжет в 1-3 предложения и оставь интригу. Не пиши никакой пояснительный текст от себя'
END_STORY = 'Напиши завершение истории c неожиданной развязкой. Не пиши никакой пояснительный текст от себя'

SYSTEM_PROMPT = ('Ты пишешь историю с пользователем. От пользователя ты получаешь:'
                 ' Имя главного персонажа, Жанр и место действия'
                 'Если добавляешь диалоги начинай их с новой строки и отделяй знаком тире'
                 'не пиши пояснительного текста')
HEADER = {'Authorization': f'Bearer {IAM_TOKEN}', 'Content-type': 'application/json'}
