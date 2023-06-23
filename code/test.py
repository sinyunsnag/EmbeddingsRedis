import streamlit as st
import os
from utilities.helper import LLMHelper

llm_helper = LLMHelper()


import openai

response = openai.Completion.create(
  model="text-davinci-003",
  prompt= ['Content: 실료,입원제비용,입원수술비,비급여병실료 | |보장대상의료비 | 실제부담액보상제외금액* * 제3관회사가보장하지않는사항에따른금액및비 급여병실료중회사가보장하지않는금액 | |도수치료 | 치료자가손(정형용교정장치장비등의도움을받는경 우를포함합니다)을이용해서환자의근골격계통(관절,근 육,연부조직,림프절등)의기능개선및통증감소를위 하여실시하는치료행위 * 의사또는의사의지도하에물리\nSource: [https://newklfnwdkogbewiostr.blob.core.windows.net/documents/%28%EB%AC%B4%29%EA%B5%90%EB%B3%B4%EC%8B%A4%EC%86%90%EC%9D%98%EB%A3%8C%EB%B9%84%EB%B3%B4%ED%97%98%28%EA%B0%B1%EC%8B%A0%ED%98%95%293_20230601.pdf.txt](https://newklfnwdkogbewiostr.blob.core.windows.net/documents/%28%EB%AC%B4%29%EA%B5%90%EB%B3%B4%EC%8B%A4%EC%86%90%EC%9D%98%EB%A3%8C%EB%B9%84%EB%B3%B4%ED%97%98%28%EA%B0%B1%EC%8B%A0%ED%98%95%293_20230601.pdf.txt_SAS_TOKEN_PLACEHOLDER_)\n\nContent: 실료,입원제비용,입원수술비,비급여병실료 | |보장대상의료비 | 실제부담액보상제외금액* * 제3관회사가보장하지않는사항에따른금액및비 급여병실료중회사가보장하지않는금액 | |도수치료 | 치료자가손(정형용교정장치장비등의도움을받는경 우를포함합니다)을이용해서환자의근골격계통(관절,근 육,연부조직,림프절등)의기능개선및통증감소를위 하여실시하는치료행위 * 의사또는의사의지도하에물리\nSource: [https://newklfnwdkogbewiostr.blob.core.windows.net/documents/%28%EB%AC%B4%29%EA%B5%90%EB%B3%B4%EC%8B%A4%EC%86%90%EC%9D%98%EB%A3%8C%EB%B9%84%EB%B3%B4%ED%97%98%28%EA%B0%B1%EC%8B%A0%ED%98%95%293_20210331.pdf.txt](https://newklfnwdkogbewiostr.blob.core.windows.net/documents/%28%EB%AC%B4%29%EA%B5%90%EB%B3%B4%EC%8B%A4%EC%86%90%EC%9D%98%EB%A3%8C%EB%B9%84%EB%B3%B4%ED%97%98%28%EA%B0%B1%EC%8B%A0%ED%98%95%293_20210331.pdf.txt_SAS_TOKEN_PLACEHOLDER_)\n\nContent: 실료,입원제비용,입원수술비,비급여병실료 | |보장대상의료비 | 실제부담액보상제외금액* * 제3관회사가보장하지않는사항에따른금액및비 급여병실료중회사가보장하지않는금액 | |도수치료 | 치료자가손(정형용교정장치장비등의도움을받는경 우를포함합니다)을이용해서환자의근골격계통(관절,근 육,연부조직,림프절등)의기능개선및통증감소를위 하여실시하는치료행위 * 의사또는의사의지도하에물리\nSource: [https://newklfnwdkogbewiostr.blob.core.windows.net/documents/%28%EB%AC%B4%29%EA%B5%90%EB%B3%B4%EC%8B%A4%EC%86%90%EC%9D%98%EB%A3%8C%EB%B9%84%EB%B3%B4%ED%97%98%28%EA%B0%B1%EC%8B%A0%ED%98%95%293_20230331.pdf.txt](https://newklfnwdkogbewiostr.blob.core.windows.net/documents/%28%EB%AC%B4%29%EA%B5%90%EB%B3%B4%EC%8B%A4%EC%86%90%EC%9D%98%EB%A3%8C%EB%B9%84%EB%B3%B4%ED%97%98%28%EA%B0%B1%EC%8B%A0%ED%98%95%293_20230331.pdf.txt_SAS_TOKEN_PLACEHOLDER_)\n\nContent: 실료,입원제비용,입원수술비,비급여병실료 | |보장대상의료비 | 실제부담액보상제외금액* * 제3관회사가보장하지않는사항에따른금액및비 급여병실료중회사가보장하지않는금액 | |도수치료 | 치료자가손(정형용교정장치장비등의도움을받는경 우를포함합니다)을이용해서환자의근골격계통(관절,근 육,연부조직,림프절등)의기능개선및통증감소를위 하여실시하는치료행위 * 의사또는의사의지도하에물리\nSource: [https://newklfnwdkogbewiostr.blob.core.windows.net/documents/%28%EB%AC%B4%29%EA%B5%90%EB%B3%B4%EC%8B%A4%EC%86%90%EC%9D%98%EB%A3%8C%EB%B9%84%EB%B3%B4%ED%97%98%28%EA%B0%B1%EC%8B%A0%ED%98%95%293_20230601.pdf.txt](https://newklfnwdkogbewiostr.blob.core.windows.net/documents/%28%EB%AC%B4%29%EA%B5%90%EB%B3%B4%EC%8B%A4%EC%86%90%EC%9D%98%EB%A3%8C%EB%B9%84%EB%B3%B4%ED%97%98%28%EA%B0%B1%EC%8B%A0%ED%98%95%293_20230601.pdf.txt_SAS_TOKEN_PLACEHOLDER_)\nPlease reply to the question using only the information present in the text above. \nInclude references to the sources you used to create the answer if those are relevant ("SOURCES"). Answer naturally, like a person talks\nQuestion: 도수치료 치료비 알려줘\nAnswer:'], 
  engine= 'TEST', 
  temperature= 0.0, 
  max_tokens= 842, 
  top_p= 1, 
  frequency_penalty= 0, 
  presence_penalty= 0, 
  n= 1, 
  best_of= 1, 
  request_timeout= None, 
  logit_bias= {}
)


print(response['choices'][0]['text'].encode().decode())



#\ub3c4\uc218\uce58\ub8cc\ub294 \uce58\ub8cc\uc790\uac00 \uc190(\uc815\ud615\uc6a9 \uad50\uc815 \uc7a5\uce58 \uc7a5\ube44 \ub4f1\uc758 \ub3c4\uc6c0\uc744 \ubc1b\ub294 \uacbd\uc6b0\ub97c \ud3ec\ud568\ud569\ub2c8\ub2e4)\uc744 \uc774\uc6a9\ud574\uc11c \ud658\uc790\uc758 \uadfc\uace8\uaca9 \uacc4\ud1b5(\uad00\uc808, \uadfc\uc721, \uc5f0\ubd80 \uc870\uc9c1, \ub9bc\ud504\uc808 \ub4f1)\uc758 \uae30\ub2a5 \uac1c\uc120 \ubc0f \ud1b5\uc99d \uac10\uc18c\ub97c \uc704\ud574 \uc2e4\uc2dc\ud558\ub294 \uce58\ub8cc \ud589\uc704\ub97c \ub9d0\ud569\ub2c8\ub2e4. \uc758\uc0ac\ub098 \uc758\uc0ac\uc758 \uc9c0\ub3c4\ud558\uc5d0 \ubb3c\ub9ac\ud559\uc801 \uce58\ub8cc\ub97c \uc2e4\uc2dc\ud569\ub2c8\ub2e4.\nSOURCES: https://newklfnwdkogbewiostr.blob.core.windows.net/documents/%28%EB%AC%B4%29%EA%B5%90%EB%B3%B4%EC%8B%A4%EC%86%90%EC%9D%98%EB%A3%8C%EB%B9%84%EB%B3%B4%ED%97%98%28%EA%B0%B1%EC%8B%A0%ED%98%95%293_20230601.pdf.txt"
