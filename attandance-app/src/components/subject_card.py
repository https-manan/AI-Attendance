import streamlit as st


def subject_card(name, code, section, stats=None, footer_callback=None):
    html = f"""
    <div style="
        background:white;
        border-left:8px solid #EB459E;
        padding:25px;
        border-radius:20px;
        border:1px solid black;
        margin-bottom:20px;
        box-shadow:0 4px 10px rgba(0,0,0,0.08);
    ">
        <h3 style="
            margin:0;
            color:#1e293b;
            font-size:1.5rem;
        ">
            {name}
        </h3>
        <p style="color:#64748b; margin:10px 0;">
            Code :
            <span style="
                background:#E0E3FF;
                color:#5865F2;
                padding:2px 8px;
                border-radius:5px;
                font-weight:bold;
            ">
                {code}
            </span>

            &nbsp;&nbsp;&nbsp;

            Section :
            <span style="
                background:#DCFCE7;
                color:#15803D;
                padding:2px 8px;
                border-radius:5px;
                font-weight:bold;
            ">
                {section}
            </span>
        </p>
    """
    if stats:
        html += """
        <div style="
            display:flex;
            gap:8px;
            flex-wrap:wrap;
            margin-top:15px;
        ">
        """
        for icon, label, value in stats:
            html += f"""
            <div style="
                background:#EB459E10;
                padding:5px 12px;
                border-radius:12px;
                font-size:0.9rem;">
                {icon}
                <b>{value}</b>
                {label}
            </div>
            """
        html += "</div>"
    html += "</div>"

    #jo leading spaces hai har line ke start mai unko hata rahe hai warna markdown parser
    #4+ space indent ko code block samajh leta hai and raw HTML tags text ki tarha dikhne lagte hai
    clean_html = "\n".join(line.lstrip() for line in html.splitlines())
    st.markdown(clean_html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()