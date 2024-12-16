import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import h, m_e, e

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

HBAR = h / (2 * np.pi)
ME = m_e

def transmission_coefficient(V0_ev, E_ev, width_nm):
    V0 = V0_ev * e
    E = E_ev * e
    width = width_nm * 1e-9

    if E < V0:
        k = np.sqrt(2 * ME * (V0 - E)) / HBAR
        k0 = np.sqrt(2 * ME * E) / HBAR
        T = 1 / (1 + (k ** 2 / (4 * k0 ** 2)) * np.sinh(k * width) ** 2)
        return T
    else:
        return 1.0

def plot_transmission_coefficient(E_ev, V0_ev, width_nm):
    V0_range = np.linspace(0.5, 10, 100)
    width_range = np.linspace(0.1, 2, 100)
    V0_mesh, width_mesh = np.meshgrid(V0_range, width_range)

    transmission_map = np.zeros_like(V0_mesh)
    for i in range(V0_mesh.shape[0]):
        for j in range(V0_mesh.shape[1]):
            transmission_map[i, j] = transmission_coefficient(V0_mesh[i, j], E_ev, width_mesh[i, j])

    fig, ax = plt.subplots(figsize=(10, 6))
    contour = ax.contourf(V0_mesh, width_mesh, transmission_map, levels=20, cmap='viridis')
    plt.colorbar(contour, label='투과 확률')
    ax.set_xlabel('장벽의 높이 (eV)')
    ax.set_ylabel('장벽 폭 (nm)')
    ax.set_title(f'전자 터널링 확률\n(전자 에너지 = {E_ev:.2f} eV, 장벽 높이 = {V0_ev:.2f} eV, 장벽 폭 = {width_nm:.2f} nm)')
    plt.tight_layout()
    return fig

def plot_transmission_variations(E_ev, V0_fixed, width_fixed):
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

    V0_range = np.linspace(0.1, 10, 100)
    transmissions = [transmission_coefficient(V0, E_ev, width_fixed) for V0 in V0_range]
    ax1.plot(V0_range, transmissions)
    ax1.set_title('투과 vs 장벽 높이\n(폭 고정)')
    ax1.set_xlabel('장벽 높이 (eV)')
    ax1.set_ylabel('투과 계수')
    ax1.axvline(x=V0_fixed, color='r', linestyle='--', alpha=0.5)

    width_range = np.linspace(0.1, 2, 100)
    transmissions = [transmission_coefficient(V0_fixed, E_ev, width) for width in width_range]
    ax2.plot(width_range, transmissions)
    ax2.set_title('투과 vs 장벽 폭\n(높이 고정)')
    ax2.set_xlabel('장벽의 폭 (nm)')
    ax2.set_ylabel('투과 계수')
    ax2.axvline(x=width_fixed, color='r', linestyle='--', alpha=0.5)

    E_range = np.linspace(0.1, 10, 100)
    transmissions = [transmission_coefficient(V0_fixed, E_val, width_fixed) for E_val in E_range]
    ax3.plot(E_range, transmissions)
    ax3.set_title('투과 vs 전자 에너지\n(폭&높이 고정)')
    ax3.set_xlabel('전자 에너지 (eV)')
    ax3.set_ylabel('투과 계수')
    ax3.axvline(x=E_ev, color='r', linestyle='--', alpha=0.5)

    plt.tight_layout()
    return fig

def main():
    st.title('전자 터널링 시각화')

    st.sidebar.header('매개변수 설정')

    E_ev = st.sidebar.slider('전자 에너지 (eV)', 0.1, 10.0, 1.0, 0.1)
    V0_ev = st.sidebar.slider('장벽 높이 (eV)', 0.5, 10.0, 2.0, 0.1)
    width_nm = st.sidebar.slider('장벽 폭 (nm)', 0.1, 2.0, 1.0, 0.1)

    with st.expander("전자 터널링이란?"):
        st.markdown("""
        전자 터널링은 양자역학적 현상으로, 전자가 고전역학적으로는 통과할 수 없는 
        에너지 장벽을 통과하는 현상입니다.

        - **에너지 (eV)**: 전자의 운동 에너지
        - **장벽 높이 (eV)**: 전자가 통과해야 하는 포텐셜 장벽의 높이
        - **장벽 폭 (nm)**: 포텐셜 장벽의 두께

        투과 계수는 전자가 장벽을 통과할 확률을 나타냅니다.
        """)

    st.header('2D 투과 확률 맵')
    fig1 = plot_transmission_coefficient(E_ev, V0_ev, width_nm)
    st.pyplot(fig1)

    st.header('매개변수별 투과 계수 변화')
    fig2 = plot_transmission_variations(E_ev, V0_ev, width_nm)
    st.pyplot(fig2)

    current_T = transmission_coefficient(V0_ev, E_ev, width_nm)
    st.sidebar.markdown(f'### 현재 투과 계수\n**{current_T:.4e}**')

    with st.expander("응용 예시"):
        st.markdown("""
        전자 터널링의 실제 응용 예시:
        1. **주사 터널링 현미경 (STM)**: 표면의 원자 구조를 관찰
        2. **터널 다이오드**: 고속 전자 소자
        3. **플래시 메모리**: 데이터 저장
        4. **알파 붕괴**: 원자핵에서의 터널링 현상
        """)

if __name__ == '__main__':
    main()
