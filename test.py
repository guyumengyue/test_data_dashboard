import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

st.title("xxx项目")
st.header("售电公司1")
st.subheader("指标1")
st.text("指标内容描述")
st.latex(r'''
        a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
        \sum_{k=0}^{n-1} ar^k =
        a \left(\frac{1-r^{n}}{1-r}\right)
        ''')

st.header("修改参数(包括但不限于以下方法)：")
st.text("具体可以参考网页: https://docs.streamlit.io/library/api-reference")
number_text = st.text_input('1、输入文本', '1')
st.write('此处会随之改变', number_text, '。')

number = st.number_input('2、输入数字')
st.write('当前数字为', number)

option = st.selectbox(
    '3、选择工具箱',
    ('Email', 'Home phone', 'Mobile phone'))
st.write('当前选中:', option)

genre = st.radio(
    "4、radio选择",
    ('Comedy', 'Drama', 'Documentary'))

if genre == 'Comedy':
    st.write('选中comedy.')
else:
    st.write("没有选中comedy.")

uploaded_file = st.file_uploader("5、本地上传文件")

if uploaded_file is not None:
  df = pd.read_csv(uploaded_file)
  st.subheader('DataFrame')
  st.write(df)
  st.subheader('Descriptive Statistics')
  st.write(df.describe())
else:
  st.info('☝️ Upload a CSV file')


options = st.multiselect(
    '6、多个选择参数',
    ['Green', 'Yellow', 'Red', 'Blue'],
    ['Yellow', 'Red'])

st.write('当前选中:', options)

number_slide = st.slider('7、滑动条选择参数(单个)', 0, 130, 25)
st.write("当前选中", number_slide)

values = st.slider(
    '7、通过滑动条选择参数(范围)',
    0.0, 100.0, (25.0, 75.0))
st.write('Values:', values)

color = st.select_slider(
    '8、选择类型(单个)',
    options=['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet'])
st.write('当前选中', color)

start_color, end_color = st.select_slider(
    '8、选择类型(范围)',
    options=['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet'],
    value=('red', 'blue'))
st.write('当前选中', start_color, '和', end_color)

st.header("结果展示(包括但不限于以下方法)：")
st.text("具体可以参考网页: https://docs.streamlit.io/library/api-reference")
st.write('1、')
with st.expander('收起的结果'):
  st.write('详细结果展示')
  st.image('https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png', width=250)

st.write("2、进度条展示结果")
import time
my_bar = st.progress(0)
my_bar.progress(25)
if st.button("启动进度条"):
    for percent_complete in range(100):
        time.sleep(0.05)
        my_bar.progress(percent_complete + 1)

    st.balloons()

st.write("3、文本以及图表展示结果，数据文本可修改，图形随之修改")
# 首先，我们需要给应用导入以下的库

import json
from pathlib import Path

# 然后我们需要 Streamlit Elements 中的这些对象
# 有关全部对象及其用法的说明请见：https://github.com/okld/streamlit-elements#getting-started

from streamlit_elements import elements, dashboard, mui, editor, media, lazy, sync, nivo

# 初始化代码编辑器和图表的默认数据
#
# 在这篇教程中，我们会用到 Nivo Bump 图的数据
# 你能在“data”标签页下获取随机的数据：https://nivo.rocks/bump/
#
# 如下所示，当代码编辑器发生更改时，会话状态就会被更新
# 然后会被读入至 Nivo Bump 图并将其绘制出来

if "data" not in st.session_state:
    st.session_state.data = Path("data.json").read_text()

# 定义默认的仪表盘布局
# 默认情况下仪表盘会分为 12 列
#
# 更多可用参数见：
# https://github.com/react-grid-layout/react-grid-layout#grid-item-props

layout = [
    # 编辑器对象定位在坐标 x=0 且 y=0 处，占据 12 列中的 6 列以及 3 行
    dashboard.Item("editor", 0, 0, 6, 3),
    # 图表对象定位在坐标 x=6 且 y=0 处，占据 12 列中的 6 列以及 3 行
    dashboard.Item("chart", 6, 0, 6, 3),
]

# 创建显示各元素的框体

with elements("demo"):

    # 使用以上指定的布局创建新仪表盘
    #
    # draggableHandle 是一个 CSS 查询选择器，定义了仪表盘中可拖拽的部分
    # 以下为将带 'draggable' 类名的元素变为可拖拽对象
    #
    # 更多仪表盘网格相关的可用参数请见：
    # https://github.com/react-grid-layout/react-grid-layout#grid-layout-props
    # https://github.com/react-grid-layout/react-grid-layout#responsive-grid-layout-props

    with dashboard.Grid(layout, draggableHandle=".draggable"):

        # 第一个卡片，代码编辑器
        #
        # 我们使用 'key' 参数来选择正确的仪表盘对象
        #
        # 为了让卡片的内容自动填充占满全部高度，我们将使用 flexbox CSS 样式
        # sx 是所有 Material UI 组件均可使用的参数，用于定义其 CSS 属性
        #
        # 有关卡片、flexbox 和 sx 的更多信息，请见：
        # https://mui.com/components/cards/
        # https://mui.com/system/flexbox/
        # https://mui.com/system/the-sx-prop/

        with mui.Card(key="editor", sx={"display": "flex", "flexDirection": "column"}):

            # 为了让标题可拖拽，我们只需要将其类名设为 'draggable'
            # 与 dashboard.Grid 当中 draggableHandle 的查询选择对应

            mui.CardHeader(title="数据文本编辑器", className="draggable")

            # 要使卡片内容占满全高，我们需要将 CSS 样式中 flex 的值设为 1
            # 同时我们也想要卡片内容随卡片缩放，因此将其 minHeight 设为 0

            with mui.CardContent(sx={"flex": 1, "minHeight": 0}):

                # 以下是我们的 Monaco 代码编辑器
                #
                # 首先，我们将其默认值设为之前初始化好的 st.session_state.data
                # 其次，我们将设定所用的语言，这里我们设为 JSON
                #
                # 接下来，我们想要获取编辑器中内容的变动
                # 查阅 Monaco 文档后，我们发现可以用 onChange 属性指定一个函数
                # 这个函数会在每次变动发生后被调用，并且变更后的内容将被传入函数
                # (参考 onChange: https://github.com/suren-atoyan/monaco-react#props)
                #
                # Streamlit Elements 提供了一个特殊的 sync() 函数
                # 能够创建一个自动将其参数同步到 Streamlit 会话状态的回调函数
                #
                # 样例
                # --------
                # 创建一个自动将第一个参数同步至会话状态中 "data" 的回调函数：
                # >>> editor.Monaco(onChange=sync("data"))
                # >>> print(st.session_state.data)
                #
                # 创建一个自动将第二个参数同步至会话状态中 "ev" 的回调函数：
                # >>> editor.Monaco(onChange=sync(None, "ev"))
                # >>> print(st.session_state.ev)
                #
                # 创建一个自动将两个参数同步至会话状态的回调函数：
                # >>> editor.Monaco(onChange=sync("data", "ev"))
                # >>> print(st.session_state.data)
                # >>> print(st.session_state.ev)
                #
                # 那么问题来了：onChange 会在每次发生变动时被调用
                # 那么意味着每当你输入一个字符，整个 Streamlit 应用都会重新运行
                #
                # 为了避免这个问题，可以使用 lazy() 令 Streamlit Elements 等待其他事件发生
                # （比如点击按钮）然后再将更新后的数据传给回调函数
                #
                # 有关 Monaco 其他可用参数的说明，请见：
                # https://github.com/suren-atoyan/monaco-react
                # https://microsoft.github.io/monaco-editor/api/interfaces/monaco.editor.IStandaloneEditorConstructionOptions.html

                editor.Monaco(
                    defaultValue=st.session_state.data,
                    language="json",
                    onChange=lazy(sync("data"))
                )

            with mui.CardActions:

                # Monaco 编辑器已经将一个延迟回调函数绑定至 onChange 了，因此即便你更改了 Monaco 的内容
                # Streamlit 也不会立刻接收到，因此不会每次都重新运行
                # 因此我们需要另一个非延迟的事件来触发更新
                #
                # 解决方法就是创建一个在点击时回调的按钮
                # 我们的回调函数实际上不需要做任何事
                # 你可以创建一个空的函数，或者直接使用不带参数的 sync()
                #
                # 然后每当你点击按钮的时候，onClick 回调函数会被调用
                # 而期间其他延迟调用了的回调函数也会被一并执行

                mui.Button("Apply changes", onClick=sync())

        # 第二个卡片，Nivo Bump 图
        # 我们将使用和第一个卡片同样的 flexbox 配置来自动调整内容高度

        with mui.Card(key="chart", sx={"display": "flex", "flexDirection": "column"}):

            # 为了让标题可拖拽，我们只需要将其类名设为 'draggable'
            # 与 dashboard.Grid 当中 draggableHandle 的查询选择对应

            mui.CardHeader(title="图形展示", className="draggable")

            # 和前面一样，我们想要让我们的内容随着用户缩放卡片而缩放
            # 因此将 flex 属性设为 1，minHeight 设为 0

            with mui.CardContent(sx={"flex": 1, "minHeight": 0}):

                # 以下我们将绘制 Bump 图
                #
                # 在这个练习里，我们就借用一下 Nivo 的示例，将其用在 Streamlit Elements 里面
                # Nivo 的示例可以在这里此页面的 'code' 标签页中找到：https://nivo.rocks/bump/
                #
                # data 参数接收一个字典，因此我们需要用 `json.loads()` 将 JSON 数据从字符串转化为字典对象
                #
                # 有关更多其他类型的 Nivo 图表，请见：
                # https://nivo.rocks/

                nivo.Bump(
                    data=json.loads(st.session_state.data),
                    colors={ "scheme": "spectral" },
                    lineWidth=3,
                    activeLineWidth=6,
                    inactiveLineWidth=3,
                    inactiveOpacity=0.15,
                    pointSize=10,
                    activePointSize=16,
                    inactivePointSize=0,
                    pointColor={ "theme": "background" },
                    pointBorderWidth=3,
                    activePointBorderWidth=3,
                    pointBorderColor={ "from": "serie.color" },
                    axisTop={
                        "tickSize": 5,
                        "tickPadding": 5,
                        "tickRotation": 0,
                        "legend": "",
                        "legendPosition": "middle",
                        "legendOffset": -36
                    },
                    axisBottom={
                        "tickSize": 5,
                        "tickPadding": 5,
                        "tickRotation": 0,
                        "legend": "",
                        "legendPosition": "middle",
                        "legendOffset": 32
                    },
                    axisLeft={
                        "tickSize": 5,
                        "tickPadding": 5,
                        "tickRotation": 0,
                        "legend": "ranking",
                        "legendPosition": "middle",
                        "legendOffset": -40
                    },
                    margin={ "top": 40, "right": 100, "bottom": 40, "left": 60 },
                    axisRight=None,
                )

st.write("4、折线图")
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

st.line_chart(chart_data)

st.write("5、区域图")
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

st.area_chart(chart_data)

st.write("6、柱状图")
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["a", "b", "c"])

st.bar_chart(chart_data)

st.write("7、离散图")

import altair as alt

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

c = alt.Chart(chart_data).mark_circle().encode(
    x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])

st.altair_chart(c, use_container_width=True)

from vega_datasets import data

source = data.cars()

chart = alt.Chart(source).mark_circle().encode(
    x='Horsepower',
    y='Miles_per_Gallon',
    color='Origin',
).interactive()

tab1, tab2 = st.tabs(["Streamlit theme (default)", "Altair native theme"])

with tab1:
    # Use the Streamlit theme.
    # This is the default. So you can also omit the theme argument.
    st.altair_chart(chart, theme="streamlit", use_container_width=True)
with tab2:
    # Use the native Altair theme.
    st.altair_chart(chart, theme=None, use_container_width=True)

st.write("8、一些优化")
import plotly.figure_factory as ff
# Add histogram data
x1 = np.random.randn(200) - 2
x2 = np.random.randn(200)
x3 = np.random.randn(200) + 2

# Group data together
hist_data = [x1, x2, x3]

group_labels = ['Group 1', 'Group 2', 'Group 3']

# Create distplot with custom bin_size
fig = ff.create_distplot(
        hist_data, group_labels, bin_size=[.1, .25, .5])

# Plot!
st.plotly_chart(fig, use_container_width=True)


import plotly.express as px
import streamlit as st

df = px.data.gapminder()

fig = px.scatter(
    df.query("year==2007"),
    x="gdpPercap",
    y="lifeExp",
    size="pop",
    color="continent",
    hover_name="country",
    log_x=True,
    size_max=60,
)

tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
with tab1:
    # Use the Streamlit theme.
    # This is the default. So you can also omit the theme argument.
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
with tab2:
    # Use the native Plotly theme.
    st.plotly_chart(fig, theme=None, use_container_width=True)


import plotly.express as px
import streamlit as st

st.subheader("Define a custom colorscale")
df = px.data.iris()
fig = px.scatter(
    df,
    x="sepal_width",
    y="sepal_length",
    color="sepal_length",
    color_continuous_scale="reds",
)

tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
with tab1:
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
with tab2:
    st.plotly_chart(fig, theme=None, use_container_width=True)