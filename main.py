import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import time

st.title("Streamlit 超入門")
st.write("progress bar")
'start!!'
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
        latest_iteration.text(f'Iteration{i+1}%')
        bar.progress(i + 1)
        time.sleep(0.01)

'done!!!!'



left_column, right_column = st.columns(2)
button =  left_column.button('put text to right')
if button:
        right_column.write('here is right column')

expander =  st.expander('問い合わせ')
expander.write('toiawase')

# option = st.text_input('your hobby?')
# 'your favorite  is:',option

# condition = st.slider('your condition?', 0, 100, 50)
# 'condition', condition




# if st.checkbox('Show Image'):
#     img = Image.open('jibun.jpg')
#     st.image(img, caption="washi", use_column_width=True)

# df = pd.DataFrame(
#     #np.random.rand(100, 2)/[50, 50] + [35.69, 139.70],
#     #columns=['lat', 'lon']
# )
# st.map(df)



##データ表示はhttps://docs.streamlit.io/library/api-reference/data参照
#st.table(df.style.highlight_max(axis=0))

# """
# # 章
# ## 節
# ### 項

# ```python
# import streamlit as st
# import numpy as np
# import pandas as pd
# ```

# """

