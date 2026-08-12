import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================
st.set_page_config(
    page_title="Função do 1º Grau — Explorador",
    page_icon="📈",
    layout="wide"
)

# ============================================
# CSS PERSONALIZADO
# ============================================
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a1a2e;
        text-align: center;
        margin-bottom: 0.3rem;
    }
    .subtitle {
        font-size: 1.05rem;
        color: #555;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .func-card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1rem;
        border-left: 5px solid;
        margin-bottom: 0.8rem;
    }
    .formula-box {
        background: #1a1a2e;
        color: #fff;
        padding: 0.7rem 1rem;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        font-size: 1.15rem;
        text-align: center;
        margin: 0.4rem 0;
    }
    .info-box {
        background: #e8f4ff;
        border-radius: 10px;
        padding: 0.8rem 1rem;
        margin: 0.5rem 0;
        font-size: 0.95rem;
    }
    .highlight-red { color: #e74c3c; font-weight: 700; }
    .highlight-blue { color: #3498db; font-weight: 700; }
    .highlight-green { color: #2ecc71; font-weight: 700; }
    .highlight-orange { color: #f39c12; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# ============================================
# CORES DAS FUNÇÕES
# ============================================
CORES_FUNCOES = ["#e74c3c", "#3498db", "#2ecc71", "#f39c12"]
NOMES_CORES = ["Vermelho", "Azul", "Verde", "Laranja"]

# ============================================
# TÍTULO
# ============================================
st.markdown('<div class="main-title">📈 Função do 1º Grau</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">f(x) = ax + b — Explore o coeficiente angular, o linear e a escala do gráfico</div>', unsafe_allow_html=True)

# ============================================
# BARRA LATERAL — CONTROLES
# ============================================
with st.sidebar:
    st.header("⚙️ Controles das Funções")
    st.markdown("---")

    # Quantidade de funções
    n_funcoes = st.slider("📊 Quantidade de funções no gráfico", 1, 4, 2)

    st.markdown("---")

    funcoes = []
    for i in range(n_funcoes):
        cor = CORES_FUNCOES[i]
        nome = NOMES_CORES[i]

        st.markdown(f"<div style='font-weight:700;color:{cor};font-size:1.1rem;'>📉 Função {i+1} ({nome})</div>", unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            a = st.slider(f"a (angular)", -10.0, 10.0, float(2-i), 0.5, key=f"a_{i}")
        with col_b:
            b = st.slider(f"b (linear)", -20.0, 20.0, float(3-i*2), 1.0, key=f"b_{i}")

        funcoes.append({"a": a, "b": b, "cor": cor, "nome": nome, "label": f"f_{i+1}(x) = {a:.1f}x + {b:.1f}"})
        st.markdown("---")

    st.header("📐 Escala do Gráfico")
    st.markdown("---")

    col_x1, col_x2 = st.columns(2)
    with col_x1:
        x_min = st.number_input("x mínimo", -50.0, 50.0, -10.0, 1.0)
    with col_x2:
        x_max = st.number_input("x máximo", -50.0, 50.0, 10.0, 1.0)

    col_y1, col_y2 = st.columns(2)
    with col_y1:
        y_min = st.number_input("y mínimo", -50.0, 50.0, -15.0, 1.0)
    with col_y2:
        y_max = st.number_input("y máximo", -50.0, 50.0, 15.0, 1.0)

    st.markdown("---")

    mostrar_grade = st.checkbox("📊 Mostrar grade", value=True)
    mostrar_eixos = st.checkbox("➕ Mostrar eixos destacados", value=True)
    mostrar_raizes = st.checkbox("🔴 Mostrar raízes (zeros)", value=True)
    mostrar_intersecoes = st.checkbox("🔵 Mostrar interseções entre funções", value=True)

    st.markdown("---")
    st.info('💡 **Dica:** Use a escala para "zoom in" em regiões específicas. Adicione até 4 funções para comparar inclinações e interceptos.')

# ============================================
# GRÁFICO PRINCIPAL
# ============================================
st.markdown("---")
st.header("📉 Plano Cartesiano")

# Geração dos pontos
x = np.linspace(x_min, x_max, 500)

fig = go.Figure()

# Eixos coordenados
if mostrar_eixos:
    fig.add_hline(y=0, line=dict(color='#333', width=1.5), hoverinfo='skip')
    fig.add_vline(x=0, line=dict(color='#333', width=1.5), hoverinfo='skip')
else:
    fig.add_hline(y=0, line=dict(color='gray', width=0.8), hoverinfo='skip')
    fig.add_vline(x=0, line=dict(color='gray', width=0.8), hoverinfo='skip')

# Plotar cada função
raizes = []
for i, f in enumerate(funcoes):
    a, b, cor = f["a"], f["b"], f["cor"]
    y = a * x + b

    # Limitar y para não extrapolar muito a escala (clip visual)
    y_clip = np.clip(y, y_min - 5, y_max + 5)

    fig.add_trace(go.Scatter(
        x=x, y=y_clip,
        mode='lines',
        line=dict(color=cor, width=3),
        name=f"f<sub>{i+1}</sub>(x) = {a:.1f}x + {b:.1f}",
        hovertemplate=f"f<sub>{i+1}</sub>(%{{x:.2f}}) = %{{y:.2f}}<extra></extra>"
    ))

    # Raiz (zero)
    if a != 0:
        raiz = -b / a
        if x_min <= raiz <= x_max:
            raizes.append({"func": i+1, "raiz": raiz, "cor": cor, "a": a, "b": b})
            if mostrar_raizes:
                fig.add_trace(go.Scatter(
                    x=[raiz], y=[0],
                    mode='markers+text',
                    marker=dict(size=14, color=cor, symbol='diamond', line=dict(width=2, color='white')),
                    text=[f'x<sub>{i+1}</sub>'],
                    textposition='bottom center',
                    textfont=dict(size=11, color=cor, family='Arial Black'),
                    hovertemplate=f"Raiz f<sub>{i+1}</sub>: x = {raiz:.3f}<extra></extra>",
                    showlegend=False
                ))

    # Intercepto y
    if y_min <= b <= y_max:
        fig.add_trace(go.Scatter(
            x=[0], y=[b],
            mode='markers',
            marker=dict(size=10, color=cor, symbol='circle', line=dict(width=2, color='white')),
            hovertemplate=f"Intercepto f<sub>{i+1}</sub>: (0, {b:.2f})<extra></extra>",
            showlegend=False
        ))

# Interseções entre funções
intersecoes = []
if mostrar_intersecoes and len(funcoes) >= 2:
    for i in range(len(funcoes)):
        for j in range(i+1, len(funcoes)):
            a1, b1 = funcoes[i]["a"], funcoes[i]["b"]
            a2, b2 = funcoes[j]["a"], funcoes[j]["b"]

            if a1 != a2:  # Retas não paralelas
                x_int = (b2 - b1) / (a1 - a2)
                y_int = a1 * x_int + b1

                if x_min <= x_int <= x_max and y_min <= y_int <= y_max:
                    intersecoes.append({
                        "f1": i+1, "f2": j+1,
                        "x": x_int, "y": y_int,
                        "cor1": funcoes[i]["cor"], "cor2": funcoes[j]["cor"]
                    })

                    fig.add_trace(go.Scatter(
                        x=[x_int], y=[y_int],
                        mode='markers+text',
                        marker=dict(size=16, color='white', symbol='star',
                                   line=dict(width=2, color='#333')),
                        text=[f'P'],
                        textposition='top center',
                        textfont=dict(size=12, color='#333', family='Arial Black'),
                        hovertemplate=f"Interseção f<sub>{i+1}</sub> ∩ f<sub>{j+1}</sub><br>({x_int:.3f}, {y_int:.3f})<extra></extra>",
                        showlegend=False
                    ))

# Layout do gráfico
fig.update_layout(
    title=dict(text='Plano Cartesiano — Funções Afins', font=dict(size=16)),
    xaxis=dict(
        title='x', range=[x_min, x_max],
        showgrid=mostrar_grade, gridwidth=0.5, gridcolor='rgba(200,200,200,0.4)',
        zeroline=True, zerolinewidth=1.5, zerolinecolor='#333' if mostrar_eixos else 'gray',
        tickmode='linear', dtick=1 if (x_max - x_min) <= 20 else 5
    ),
    yaxis=dict(
        title='f(x)', range=[y_min, y_max],
        showgrid=mostrar_grade, gridwidth=0.5, gridcolor='rgba(200,200,200,0.4)',
        zeroline=True, zerolinewidth=1.5, zerolinecolor='#333' if mostrar_eixos else 'gray',
        tickmode='linear', dtick=1 if (y_max - y_min) <= 20 else 5,
        scaleanchor='x', scaleratio=1
    ),
    height=650,
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=60, r=30, t=50, b=50),
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
    dragmode='pan'
)

st.plotly_chart(fig, use_container_width=True)

# ============================================
# SEÇÃO: INFORMAÇÕES DAS FUNÇÕES
# ============================================
st.markdown("---")
st.header("📋 Análise das Funções")

cols = st.columns(min(4, len(funcoes)))
for i, f in enumerate(funcoes):
    with cols[i]:
        a, b, cor = f["a"], f["b"], f["cor"]
        raiz = -b/a if a != 0 else "∄ (reta horizontal)"
        raiz_str = f"{raiz:.3f}" if isinstance(raiz, float) else raiz

        st.markdown(f"""
        <div class="func-card" style="border-left-color: {cor};">
            <div style="font-size:1.2rem;font-weight:700;color:{cor};margin-bottom:0.5rem;">
                f<sub>{i+1}</sub>(x) = {a:.1f}x + {b:.1f}
            </div>
            <div class="formula-box" style="font-size:1rem;">
                f<sub>{i+1}</sub>(x) = {a:.1f}x + {b:.1f}
            </div>
            <div style="font-size:0.95rem;color:#555;line-height:1.8;margin-top:0.5rem;">
                <b>Coeficiente angular (a):</b> <span style="color:{cor};font-weight:700;">{a:.1f}</span><br>
                <b>Coeficiente linear (b):</b> {b:.1f}<br>
                <b>Raiz (zero):</b> x = {raiz_str}<br>
                <b>Intercepto y:</b> (0, {b:.1f})<br>
                <b>Crescimento:</b> {"↗ Crescente" if a > 0 else "↘ Decrescente" if a < 0 else "→ Constante"}<br>
                <b>Inclinação:</b> {"|a| > 1: íngreme" if abs(a) > 1 else "|a| < 1: suave" if abs(a) < 1 and a != 0 else "a = 0: horizontal"}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# SEÇÃO: TABELA DE VALORES
# ============================================
st.markdown("---")
st.header("📊 Tabela de Valores")

# Pontos de x para a tabela
n_pontos = st.slider("Quantidade de pontos na tabela", 3, 15, 7)
x_tab = np.linspace(x_min, x_max, n_pontos)

tabela = {"x": [f"{xi:.2f}" for xi in x_tab]}
for i, f in enumerate(funcoes):
    a, b = f["a"], f["b"]
    tabela[f"f_{i+1}(x)"] = [f"{a*xi + b:.2f}" for xi in x_tab]

st.dataframe(tabela, use_container_width=True, hide_index=True)

# ============================================
# SEÇÃO: INTERSEÇÕES
# ============================================
if len(funcoes) >= 2 and len(intersecoes) > 0:
    st.markdown("---")
    st.header("🔵 Pontos de Interseção")

    for inter in intersecoes:
        st.markdown(f"""
        <div class="info-box" style="border-left: 4px solid #9b59b6;">
            <b>f<sub>{inter['f1']}</sub> ∩ f<sub>{inter['f2']}</sub>:</b> 
            P = <b>({inter['x']:.3f}, {inter['y']:.3f})</b><br>
            <span style="font-size:0.9rem;color:#777;">Resolvendo {funcoes[inter['f1']-1]['a']:.1f}x + {funcoes[inter['f1']-1]['b']:.1f} = {funcoes[inter['f2']-1]['a']:.1f}x + {funcoes[inter['f2']-1]['b']:.1f}</span>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# SEÇÃO: ANÁLISE DO SINAL
# ============================================
st.markdown("---")
st.header("➕➖ Análise do Sinal (Positivo/Negativo)")

for i, f in enumerate(funcoes):
    a, b, cor = f["a"], f["b"], f["cor"]

    if a == 0:
        # Função constante
        sinal = "positivo" if b > 0 else "negativo" if b < 0 else "nulo"
        st.markdown(f"""
        <div style="background:{cor}11;border-radius:10px;padding:0.8rem 1rem;margin:0.4rem 0;border-left:4px solid {cor};">
            <b>f<sub>{i+1}</sub>(x) = {b:.1f}</b> (função constante): sempre <b>{sinal}</b> para todo x ∈ ℝ
        </div>
        """, unsafe_allow_html=True)
    else:
        raiz = -b / a
        if a > 0:
            st.markdown(f"""
            <div style="background:{cor}11;border-radius:10px;padding:0.8rem 1rem;margin:0.4rem 0;border-left:4px solid {cor};">
                <b>f<sub>{i+1}</sub>(x) = {a:.1f}x + {b:.1f}</b> (crescente):<br>
                f<sub>{i+1}</sub>(x) < 0  →  x < {raiz:.3f}<br>
                f<sub>{i+1}</sub>(x) = 0  →  x = {raiz:.3f}<br>
                f<sub>{i+1}</sub>(x) > 0  →  x > {raiz:.3f}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background:{cor}11;border-radius:10px;padding:0.8rem 1rem;margin:0.4rem 0;border-left:4px solid {cor};">
                <b>f<sub>{i+1}</sub>(x) = {a:.1f}x + {b:.1f}</b> (decrescente):<br>
                f<sub>{i+1}</sub>(x) < 0  →  x > {raiz:.3f}<br>
                f<sub>{i+1}</sub>(x) = 0  →  x = {raiz:.3f}<br>
                f<sub>{i+1}</sub>(x) > 0  →  x < {raiz:.3f}
            </div>
            """, unsafe_allow_html=True)

# ============================================
# SEÇÃO: CONCEITOS TEÓRICOS
# ============================================
st.markdown("---")
st.header("📚 Conceitos Fundamentais")

col_t1, col_t2 = st.columns(2)

with col_t1:
    st.markdown("""
    <div style="background:#e8f4ff;border-radius:12px;padding:1.2rem;">
        <div style="font-size:1.1rem;font-weight:700;color:#3498db;margin-bottom:0.5rem;">
            📐 Coeficiente Angular (a)
        </div>
        <div style="font-size:0.95rem;color:#333;line-height:1.7;">
            Representa a <b>taxa de variação</b> da função.<br><br>
            <b>a > 0:</b> função crescente ↗<br>
            <b>a < 0:</b> função decrescente ↘<br>
            <b>a = 0:</b> função constante →<br><br>
            Quanto maior |a|, mais <b>íngreme</b> é a reta.<br>
            |a| = 1: inclinação de 45°<br>
            |a| > 1: mais íngreme que 45°<br>
            |a| < 1: mais suave que 45°
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_t2:
    st.markdown("""
    <div style="background:#e8f5e9;border-radius:12px;padding:1.2rem;">
        <div style="font-size:1.1rem;font-weight:700;color:#2ecc71;margin-bottom:0.5rem;">
            📍 Coeficiente Linear (b)
        </div>
        <div style="font-size:0.95rem;color:#333;line-height:1.7;">
            Representa o <b>valor de f(x) quando x = 0</b>.<br><br>
            É o ponto onde a reta <b>cruza o eixo y</b>.<br><br>
            <b>b > 0:</b> intercepto acima da origem<br>
            <b>b < 0:</b> intercepto abaixo da origem<br>
            <b>b = 0:</b> reta passa pela origem (0,0)<br><br>
            Alterar b <b>translada</b> a reta para cima ou para baixo, 
            <b>sem mudar a inclinação</b>.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# SEÇÃO: EXERCÍCIO RESOLVIDO
# ============================================
st.markdown("---")
st.header("📝 Exercício Resolvido com os Valores Atuais")

# Pega a primeira função para o exercício
f_ex = funcoes[0]
a_ex, b_ex = f_ex["a"], f_ex["b"]

st.markdown(f"""
<div style="background:#fff8e1;border-radius:12px;padding:1.5rem;border:2px solid #ffc107;">
    <div style="font-size:1.1rem;font-weight:700;color:#2c3e50;margin-bottom:1rem;">
        📌 Problema
    </div>
    <div style="font-size:1rem;color:#333;line-height:1.7;margin-bottom:1rem;">
        Dada a função <b>f(x) = {a_ex:.1f}x + {b_ex:.1f}</b>, determine:<br>
        a) O valor de f(2)<br>
        b) O valor de x tal que f(x) = 0<br>
        c) Se a função é crescente ou decrescente
    </div>

    <div style="font-size:1.1rem;font-weight:700;color:#27ae60;margin-bottom:0.8rem;">
        ✏️ Resolução
    </div>
    <div style="font-size:0.95rem;color:#333;line-height:1.8;font-family:'Georgia',serif;">
        <b>a)</b> f(2) = {a_ex:.1f} · 2 + {b_ex:.1f} = {a_ex*2:.1f} + {b_ex:.1f} = <b>{a_ex*2 + b_ex:.1f}</b><br><br>
        <b>b)</b> f(x) = 0 → {a_ex:.1f}x + {b_ex:.1f} = 0 → {a_ex:.1f}x = {-b_ex:.1f} → x = <b>{-b_ex/a_ex:.3f}</b><br><br>
        <b>c)</b> Como a = {a_ex:.1f} {" > 0, a função é <b>crescente</b>" if a_ex > 0 else " < 0, a função é <b>decrescente</b>" if a_ex < 0 else " = 0, a função é <b>constante</b>"}.
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
# RODAPÉ
# ============================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.85rem; padding: 1rem;">
    📈 <b>Explorador de Função do 1º Grau</b> — Ferramenta educacional para o ensino de Matemática<br>
    Use os controles na barra lateral para ajustar os parâmetros e explorar o comportamento das funções afins.
</div>
""", unsafe_allow_html=True)
