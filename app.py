import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# Cargar datos
df = pd.read_csv('nba_all_elo.csv')

def main():
    st.title('Dashboard de Rendimiento de la NBA')
    
    # Sidebar
    st.sidebar.header('Filtros del Dashboard')
    
    # Selector de año
    available_years = sorted(df['year_id'].unique())
    selected_year = st.sidebar.selectbox('Seleccionar Año', available_years)
    
    # Selector de equipo
    available_teams = sorted(df[df['year_id'] == selected_year]['team_id'].unique())
    selected_team = st.sidebar.selectbox('Seleccionar Equipo', available_teams)
    
    # Selector de tipo de juego
    game_types = ['Temporada Regular', 'Playoffs', 'Ambos']
    selected_game_type = st.sidebar.radio('Seleccionar Tipo de Juego', game_types)
    
    # Filtrar datos
    filtered_df = df[
        (df['year_id'] == selected_year) & 
        (df['team_id'] == selected_team)
    ]
    
    # Filtrar por tipo de juego
    if selected_game_type == 'Temporada Regular':
        filtered_df = filtered_df[filtered_df['is_playoffs'] == 0]
    elif selected_game_type == 'Playoffs':
        filtered_df = filtered_df[filtered_df['is_playoffs'] == 1]
    
    # Calcular victorias y derrotas acumuladas
    filtered_df['victorias_acumuladas'] = (filtered_df['game_result'] == 'W').cumsum()
    filtered_df['derrotas_acumuladas'] = (filtered_df['game_result'] == 'L').cumsum()
    
    # Gráfica de líneas
    fig_acumulado = go.Figure()
    fig_acumulado.add_trace(go.Scatter(
        x=filtered_df.index, 
        y=filtered_df['victorias_acumuladas'], 
        mode='lines', 
        name='Victorias Acumuladas'
    ))
    fig_acumulado.add_trace(go.Scatter(
        x=filtered_df.index, 
        y=filtered_df['derrotas_acumuladas'], 
        mode='lines', 
        name='Derrotas Acumuladas'
    ))
    fig_acumulado.update_layout(
        title=f'{selected_team} - Victorias y Derrotas Acumuladas en {selected_year}',
        xaxis_title='Número de Juego',
        yaxis_title='Número Acumulado'
    )
    st.plotly_chart(fig_acumulado)
    
    # Gráfica de pastel
    total_juegos = len(filtered_df)
    victorias = len(filtered_df[filtered_df['game_result'] == 'W'])
    derrotas = len(filtered_df[filtered_df['game_result'] == 'L'])
    
    fig_porcentaje = px.pie(
        values=[victorias, derrotas], 
        names=['Victorias', 'Derrotas'], 
        title=f'Porcentaje de Victorias/Derrotas de {selected_team} en {selected_year}'
    )
    st.plotly_chart(fig_porcentaje)

if __name__ == '__main__':
    main()