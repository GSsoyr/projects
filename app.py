import streamlit as st
import easyocr
import numpy as np
from PIL import Image
import re

# Настройка на заглавието на страницата
st.set_page_config(page_title="ИИ Анализатор на храни", page_icon="🧪")

# База данни с вредни съставки
HARMFUL_INGREDIENTS = {
    "E407": "Карагенан - Може да предизвика възпаления в червата.",
    "E621": "Мононатриев глутамат - Подсилвател на вкуса. Може да причини главоболие.",
    "E250": "Натриев нитрит - Свързва се с риск от онкологични заболявания.",
    "E450": "Дифосфати - Нарушават калциево-фосфорния баланс.",
    "E202": "Калиев сорбат - Консервант, считан за безопасен, но дразнещ при някои хора.",
    "E102": "Тартразин - Оцветител, може да причини хиперактивност.",
    "E129": "Алура червено - Потенциален алерген.",
    "E330": "Лимонена киселина - Уврежда зъбния емайл в големи количества."
}

# Кеширане на модела, за да не се зарежда при всяко кликване
@st.cache_resource
def load_reader():
    return easyocr.Reader(['bg', 'en'])

reader = load_reader()

st.title("🧪 ИИ Химия на храните")
st.write("Снимай етикета и аз ще открия опасните Е-номера.")

# Качване на снимка
uploaded_file = st.file_uploader("Качи снимка на етикет", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Обработка...', use_container_width=True)
    
    with st.spinner('Анализирам текста...'):
        # Превръщане на снимката в разпознаваем формат
        img_array = np.array(image)
        results = reader.readtext(img_array, detail=0)
        full_text = " ".join(results).upper()
        
        # Показване на разпознатия текст (за проверка)
        with st.expander("Виж разпознатия текст"):
            st.write(full_text)
        
        # Търсене на съставки
        found = []
        for code, desc in HARMFUL_INGREDIENTS.items():
            # Regex за намиране на Е-номер (напр. Е621 или Е 621)
            pattern = rf"{code[0]}\s?{code[1:]}"
            if re.search(pattern, full_text):
                found.append((code, desc))
        
        st.divider()
        
        if found:
            st.error(f"⚠️ Внимание! Намерени са {len(found)} опасни съставки:")
            for code, desc in found:
                st.write(f"**{code}**: {desc}")
        else:
            st.success("✅ Не бяха открити опасни Е-номера от базата данни.")
