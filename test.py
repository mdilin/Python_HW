# делаем приложение на сервере, чтобы с ним могли взаимодействовать другие люди

# рассмотрим крутейшую библиотеку streamlit, которая позволяет в пару строчек сделать веб-приложения
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

df = pd.DataFrame({'x': [10, 20, 30, 40],
                   'y': [100, 200, 300, 400],
                   'name': ['alpha', 'beta', 'gamma', 'delta']
                   })
x_max = st.slider('Max value of x', float(df['x'].max()))
st.title("My streamlit app")
st.markdown("""
Let's look down at this fine dataframe (tested):
""")

df[df['x'] < x_max]

st.markdown("""
### Now let's draw something!
""")

a = st.slider('Amplitude', 0., 10.)
b = st.slider('Frequency', 0., 10.)
x = np.linspace(0, 10, 500) #точки ставаим, чтобы Python воспринимал числа, как float, 500 = число точек


fig = plt.figure()
plt.plot(x, a * np.sin(x * b))
plt.ylim(-5, 5)
st.pyplot(fig)

st.markdown("""
### Put some file and we will decode it!
""")

# можно принимать на вход файл, и визуализировать его:
uploaded_file = st.file_uploader("Upload some file")
if uploaded_file is not None:
    for i, line in enumerate(
            uploaded_file.getvalue().decode('utf-8').splitlines()):
        st.text(f"{i}. {line}".rstrip())


# познакомимся с такой вещью, как git (github)
# как написать код, который будут дорабатывать другие люди?

# git - это программа, которая позволяет отслеживать последние версии файла
# github - это сайт, который работает с этой программой

# создаём репозиторий через PyCharm
# затем делаем "commit": добавление файлов в репозиторий
