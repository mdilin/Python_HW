import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt

with st.echo(code_location='below'):
    st.title("Визуализация данных о трендовых видео российского YouTube")

    st.markdown(""" ## Привет! """)

    st.markdown("""
    Я буду визуализировать данные о трендах российского YouTube. Они обновляются ежедневно, и в данной работе 
    я буду использовать данные, актуальные на 11 апреля. Самую актуальную версию вы можете найти на сайте:
    https://www.kaggle.com/rsrishav/youtube-trending-video-dataset/code
    """)

    st.markdown("""
    Сразу замечу, что у нас данных о чуть более 47 тысячах
    видео, для каждого из которых есть 16 колонок данных: название видео, дата и время публикации,
    название канала, дата попадания в тренды, количество просмотров, лайков, дизлайков, комментариев.
    """)

    df = pd.read_csv('RU_youtube_trending_data.csv')
    st.markdown("""Выведем количество видео и количество колонок, используя функцию df.shape: """)
    df.shape
    st.markdown("""Выведем все возможные колонки, используя функцию df.columns: """)
    df.columns

    st.markdown("""## Давайте определим, какие каналы чаще всего попадают в Российские тренды?""")
    x1 = st.slider('Количество отображаемых каналов (от 5 до 20)', 5, 20)

    st.markdown("""Точное количество видео в трендах:""")
    trending_channels = pd.DataFrame(df['channelTitle'].value_counts().head(x1))
    trending_channels

    st.markdown("""Визуальное представление:""")

    ### FROM: https://www.kaggle.com/spodali/youtube-trending-videos-eda

    videos_by_channel = df.groupby("channelTitle").size().reset_index(name="no_of_videos") \
        .sort_values("no_of_videos", ascending=False).head(x1)
    fig1, ax = plt.subplots(figsize=(10,6))
    vbc_plot = sns.barplot(x="no_of_videos", y="channelTitle", data=videos_by_channel, palette="YlGnBu_r")
    vbc_plot = ax.set(xlabel="Количество видео в трендах", ylabel="Канал")
    plt.title("Каналы, у которых видео чаще всего попадают в тренды")
    plt.show()
    st.pyplot(fig1)

    ### END FROM

    st.markdown("""Для любителей: можем посмотреть на самые залайканные и задизлайканные видео, которые
    появлялись во вкладке "в тренде".""")
    x2 = st.slider('Количество отображаемых видео (от 5 до 25)', 5, 25)

    st.markdown("""Видео с наибольшим количеством лайков, которые были "в тренде": """)
    most_liked = df[['title', 'likes']].groupby('title').sum().sort_values(by='likes', ascending=False).head(x2)
    most_liked

    st.markdown("""Видео с наибольшим количеством дизлайков, которые были "в тренде": """)
    most_disliked = df[['title', 'dislikes']].groupby('title').sum().sort_values(by='dislikes', ascending=False).head(x2)
    most_disliked

    st.write(""" ### Давайте поговорим об корреляциях. """)

    st.markdown("""Составим общую таблицу корреляции, используя функцию df.corr():""")

    correlation = df.corr()
    correlation

    fig5 = plt.figure()
    sns.heatmap(correlation, annot=True, fmt='.1g', cmap='YlOrRd')
    st.pyplot(fig5)

    st.markdown("""Рассмотрим две самые значимые корреляции из общей таблицы: между количеством просмотров и лайков,
    а также между количеством просмотров и оставленных под видео комментариев:""")

    fig4, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), sharey=True)
    ax1.scatter(df['view_count'], df['likes'])
    ax2.scatter(df['view_count'], df['comment_count'])
    ax1.set_xlabel('Количество просмотров')
    ax2.set_xlabel('Количество просмотров')
    ax1.set_ylabel('Количество лайков')
    ax2.set_ylabel('Количество комментариев')
    fig4

    st.markdown("""Как мы можем заметить, корреляция действительно присутствует, и она положительна (что следует из
    общей таблицы корреляции). Но немаловажно отметить, что корреляция между просмотрами и лайками выше, чем между
    просмотрами и комментариями. Это следует из графика (точки корреляции расположены ниже), а также из
    таблицы коэффициентов корреляции (коэффициенты: 0.9 против 0.8)""")

    st.markdown("""Давайте ненадолго побудем блоггерами. Наша задача: понять, в какое время лучше всего
    выложить видео, чтобы оно попало "в тренды" и набрало как можно больше просмотров. Для этого визуально
    изобразим таблицу, показывающую количество видео, попавших в тренды, в зависимости от времени их публикации.""")

    ### FROM: https://www.kaggle.com/spodali/youtube-trending-videos-eda

    df["publish_hour"] = df["publishedAt"].apply(lambda x: x[11:13])
    videos_by_pub_hour = df.groupby("publish_hour").size().reset_index(name="no_of_videos")
    figtime, ax = plt.subplots(figsize=(8,8))
    vph_plot = sns.barplot(x="publish_hour", y="no_of_videos", data=videos_by_pub_hour,palette="flare")
    vph_plot = ax.set(xlabel="Время публикации", ylabel="Количество видео в трендах")
    plt.title("Видео в трендах в зависимости от времени публикации")
    plt.show()
    st.pyplot(figtime)

    ### END FROM

    st.markdown("""Как мы можем заметить, для Российского YouTube важно, чтобы видео выходило утром (с 7 до 9 утра) - 
    вероятно, из-за того, что люди любят смотреть видео, пока завтракают, или добираются до учёбы / работы.""")

    st.markdown("""Кроме того, часто "выстреливают" видео, которые были выложены в 16 часов дня. Тут, вероятно,
    причина состоит в том, что в это время большинство школьников уже закончило учиться (то есть они, вероятно,
    будут смотреть видео), а затем к ним прибавляются люди, которые закончили работать (то есть где-то в районе 18).
    Из-за этого суммарное количество просмотров максимально, и, следовательно, попасть "в тренды" становится легко.""")

    st.markdown("""### Спасибо за внимание и предоставленное время!""")

    st.markdown("""Вот мой код:""")