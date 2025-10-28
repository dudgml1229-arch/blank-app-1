# -*- coding: utf-8 -*-
# 나노바나나 종횡비 생성기 (Streamlit)
import io, zipfile
from dataclasses import dataclass
from typing import List, Tuple
from PIL import Image, ImageOps, ImageColor
import streamlit as st
st.markdown("""
<style>
html, body { background:#0A0A2C !important; }
h1 { color:#FF61D6 !important; text-shadow:0 2px 8px rgba(0,0,0,.25) !important; }
.stButton>button{
  background:linear-gradient(90deg,#7B39FF,#581CA0);
  color:#fff;border:none;border-radius:12px;padding:.6rem 1rem;font-weight:700;
}
.stFileUploader{border:2px dashed rgba(255,255,255,.25);border-radius:14px;padding:1rem;background:rgba(255,255,255,.06)}
input[type=checkbox]{ accent-color:#C4B5FD }
</style>
""", unsafe_allow_html=True)

@dataclass
class Ratio:
    label: str
    w: int
    h: int

RATIOS: List[Ratio] = [
    Ratio("정사각형 (1:1)", 1, 1),
    Ratio("세로 (3:4)", 3, 4),
    Ratio("수직 (2:3)", 2, 3),
    Ratio("프로 (4:3)", 4, 3),
    Ratio("클래식 (3:2)", 3, 2),
    Ratio("와이드스크린 (16:9)", 16, 9),
    Ratio("세로 (9:16)", 9, 16),
    Ratio("시네마틱 (21:9)", 21, 9),
    Ratio("파노라마 (2:1)", 2, 1),
]

def _to_rgb(color: str = "#111827") -> Tuple[int, int, int]:
    try:
        return ImageColor.getrgb(color)
    except Exception:
        return (17, 24, 39)

def resize_with_mode(img: Image.Image, ratio: Ratio, mode: str, bg_color: str = "#0B1020") -> Image.Image:
    target_w, target_h = ratio.w, ratio.h
    long_side = 1024
    if target_w >= target_h:
        base_w, base_h = long_side, int(long_side * target_h / target_w)
    else:
        base_h, base_w = long_side, int(long_side * target_w / target_h)

    if mode == "레터박스(FIT)":
        canvas = Image.new("RGB", (base_w, base_h), _to_rgb(bg_color))
        img_copy = img.copy().convert("RGB")
        img_copy.thumbnail((base_w, base_h))
        x = (base_w - img_copy.width) // 2
        y = (base_h - img_copy.height) // 2
        canvas.paste(img_copy, (x, y))
        return canvas
    else:
        return ImageOps.fit(img.copy().convert("RGB"), (base_w, base_h))

def pil_to_bytes(img: Image.Image, fmt: str = "JPEG", quality: int = 92) -> bytes:
    buf = io.BytesIO()
    img.save(buf, format=fmt, quality=quality)
    return buf.getvalue()

st.set_page_config(page_title="나노바나나 종횡비 생성기", page_icon="🖼️", layout="wide")
st.title("나노바나나 종횡비 생성기")
st.caption("AI&디지털콘텐츠연구소")

col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.header("1. 이미지 업로드")
    up = st.file_uploader("이미지 파일을 선택하세요 (JPG/PNG)", type=["jpg", "jpeg", "png"])

    st.header("2. 화면 비율 선택")
    selected = []
    for r in RATIOS:
        if st.checkbox(r.label, value=r.label in ["와이드스크린 (16:9)", "세로 (9:16)"]):
            selected.append(r)

    st.subheader("자르기 모드")
    mode = st.radio("방식 선택", ["중앙 크롭(FILL)", "레터박스(FIT)"], index=0)
    bg = st.color_picker("배경색(FIT 모드)", value="#0B1020")
    generate = st.button("이미지 생성하기", type="primary")

with col2:
    st.header("결과물")
    gallery = st.empty()
    zip_btn = st.empty()

if generate:
    if not up:
        st.warning("이미지를 업로드해 주세요.")
        st.stop()
    if not selected:
        st.warning("최소 1개의 비율을 선택해 주세요.")
        st.stop()

    img = Image.open(up)
    results = []
    for r in selected:
        out = resize_with_mode(img, r, mode, bg)
        results.append((r.label, out))

    cols = st.columns(min(3, len(results)))
    for i, (lab, im) in enumerate(results):
        with cols[i % len(cols)]:
            st.image(im, caption=f"{lab} ({im.width}x{im.height})", use_column_width=True)

    zip_buf = io.BytesIO()
    with zipfile.ZipFile(zip_buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        for lab, im in results:
            zf.writestr(f"{lab}.jpg", pil_to_bytes(im))
    zip_buf.seek(0)

    zip_btn.download_button(
        label="전체 다운로드 (ZIP)",
        data=zip_buf,
        file_name="aspect-ratio-results.zip",
        mime="application/zip",
    )
# ===========================
# 💅 Custom CSS Styling
# ===========================
st.markdown("""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2107@1.1/GmarketSansMedium.woff2');

    html, body, [class*="css"] {
        font-family: 'GmarketSansMedium', sans-serif;
        background: linear-gradient(135deg, #0A0A2C 0%, #371C9C 100%);
        color: #F2F0F4;
    }

    h1, h2, h3 {
        color: #F2F0F4 !important;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.5);
    }

    .stButton>button {
        background: linear-gradient(90deg, #581CA0, #371C9C);
        color: #fff;
        border: none;
        border-radius: 12px;
        padding: 0.6em 1.2em;
        font-weight: bold;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: scale(1.05);
        background: linear-gradient(90deg, #6D28D9, #4338CA);
        box-shadow: 0 0 15px #6D28D9;
    }

    .stFileUploader, .stCheckbox {
        color: #E5E5F7 !important;
    }

    .css-18ni7ap {
        background: rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 1em;
    }
    </style>
""", unsafe_allow_html=True)
