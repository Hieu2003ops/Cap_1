import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="Dashboard", layout="wide")

@st.cache_data
def load_data(file_name, sheet_name):
    return pd.read_excel(file_name, sheet_name=sheet_name)

def main():
    # Load data
    data = load_data('HR Data.xlsx', 'HR')
    # Create header in the center
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        st.markdown("<h1 style='text-align: center; font-size: 60px;'>Phân Tích Nguyên Nhân Nghỉ Việc</h1>", unsafe_allow_html=True)

    if 'current_tab' not in st.session_state:
        st.session_state['current_tab'] = 'Tab 1'
    tabs = ["Tab 1", "Tab 2", "Tab 3", "Tab 4", "Tab 5"]
    tab_buttons = st.columns(len(tabs))
    for i, button in enumerate(tab_buttons):
        if button.button(tabs[i]):
            st.session_state['current_tab'] = tabs[i]

    if st.session_state['current_tab'] == "Tab 1":
        st.markdown("<h1 style='text-align: center; font-size: 60px;'>Company Profile</h1>", unsafe_allow_html=True)
        @st.cache_data
        def calculate_metrics(data):
            total_employees = len(data)
            employees_attrition = (data['Attrition'] == 'Yes').sum()
            attrition_rate = round(employees_attrition / total_employees * 100, 2)
            employees_activate = total_employees - employees_attrition
            mean_age = round(data['Age'].mean(), 2)
            return total_employees, employees_attrition, attrition_rate, employees_activate, mean_age

        total_employees, employees_attrition, attrition_rate, employees_activate, mean_age = calculate_metrics(data)

        col_a, col_b, col_c, col_d, col_e = st.columns(5)

        col_a.metric("Tổng số nhân viên", f"{total_employees:,}")
        col_b.metric("Tổng số nhân viên nghỉ việc", f"{employees_attrition:,}")
        col_c.metric("Tỉ lệ nhân viên nghỉ việc", f"{attrition_rate:,}")
        col_d.metric("Tổng số nhân viên còn làm việc", f"{employees_activate:,}")
        col_e.metric("Độ tuổi trung bình của nhân viên", f"{mean_age:,}")
            # Gender Distribution
        gender_fig = px.pie(data_frame=data, names='Gender', title='Gender Distribution',
                            color_discrete_sequence=px.colors.qualitative.Set2)
        
            # Gender Distribution
        gender_fig = px.pie(data_frame=data, names='Gender', title='Gender Distribution',
                            color_discrete_sequence=px.colors.qualitative.Set2)

        # Department Distribution
        department_counts = data['Department'].value_counts().reset_index(name="Number of Employees")
        department_counts.columns = ['Department', 'Number of Employees']
        department_fig = px.bar(data_frame=department_counts,
                                x='Number of Employees', y='Department', title='Department Distribution',
                                labels={'Department': 'Department', 'Number of Employees': 'Number of Employees'},
                                color='Department', color_discrete_sequence=px.colors.qualitative.Bold)

        # Marital Status Distribution
        marital_fig = px.pie(data_frame=data, names='Marital Status', title='Marital Status Distribution',
                            color_discrete_sequence=px.colors.qualitative.Pastel1)

        # Job Role Distribution
        job_role_counts = data['Job Role'].value_counts().reset_index(name="Number of Employees")
        job_role_counts.columns = ['Job Role', 'Number of Employees']
        job_role_fig = px.bar(data_frame=job_role_counts,
                            x='Number of Employees', y='Job Role', title='Job Role Distribution',
                            labels={'Job Role': 'Job Role', 'Number of Employees': 'Number of Employees'},
                            color='Job Role', color_discrete_sequence=px.colors.qualitative.Set3)

        # Education Field Distribution
        education_field_counts = data['Education Field'].value_counts().reset_index(name="Number of Employees")
        education_field_counts.columns = ['Education Field', 'Number of Employees']
        education_field_fig = px.bar(data_frame=education_field_counts,
                                    x='Number of Employees', y='Education Field', title='Education Field Distribution',
                                    labels={'Education Field': 'Education Field', 'Number of Employees': 'Number of Employees'},
                                    color='Education Field', color_discrete_sequence=px.colors.qualitative.Set1)

        # Education Level Distribution
        education_level_fig = px.pie(data_frame=data, names='Education', title='Education Level Distribution',
                                    color_discrete_sequence=px.colors.sequential.Rainbow)

        # Age Distribution
        age_fig = px.histogram(data_frame=data, x='Age', title='Age Distribution',
                            color_discrete_sequence=['skyblue'], nbins=20)  # Adjust the number of bins
        
        # Add Median Age Line
        median_age = data['Age'].median()
        age_fig.add_vline(x=median_age, line_dash="dash", line_color="#e63946",
                        annotation_text="Median", annotation_position="top right",
                        annotation_font_size=12, annotation_font_color="#e63946",
                        annotation_textangle=-90)  # Rotate text for better spacing

        # Add Mean Age Line
        mean_age = data['Age'].mean()
        age_fig.add_vline(x=mean_age, line_dash="solid", line_color="black",
                        annotation_text="Mean", annotation_position="top right",
                        annotation_font_size=12, annotation_font_color="black",
                        annotation_textangle=-90)  # Rotate text for better spacing

        # Improve visual styling
        age_fig.update_layout(
            xaxis_title='Age',
            yaxis_title='Frequency',
            legend_title_text='Age Metrics',
            template='plotly_white',
            margin=dict(t=60)  # Add more top margin to accommodate title
        )


        # Arrange plots in Streamlit
        col1, col2, col3 = st.columns(3)
        with col1:
            st.plotly_chart(gender_fig, use_container_width=True)
        with col2:
            st.plotly_chart(department_fig, use_container_width=True)
        with col3:
            st.plotly_chart(marital_fig, use_container_width=True)

        col4, col5, col6 = st.columns(3)
        with col4:
            st.plotly_chart(job_role_fig, use_container_width=True)
        with col5:
            st.plotly_chart(education_field_fig, use_container_width=True)
        with col6:
            st.plotly_chart(education_level_fig, use_container_width=True)

        st.plotly_chart(age_fig, use_container_width=True)

if __name__ == "__main__":
    main()