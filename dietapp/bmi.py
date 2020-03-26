from plotly.offline import plot
from plotly.graph_objects import Indicator

def BMI(weight,height,plotit=True):
    bmi = float(weight)/((float(height)/100)**2)
    bmi_indicator = None
    bmi_status = ""
    bmi_color = ""
    if plotit:
        bmi_indicator = plot(
            [Indicator(
                mode = "gauge+number",
                value = bmi,
                domain={'x': [0, 1], 'y': [0, 1]},
                title = {'text':'BMI'},
                gauge = {
                    'bar':{'color':'rgba(50,50,50,0.5)','thickness':0.75},
                    'steps': [
                        {'range':[0,15],'color':'red',},
                        {'range':[15,16],'color':'orange'},
                        {'range': [16,18.5],'color':'yellow'},
                        {'range': [18.5,25],'color':'green',},
                        {'range': [25,30],'color':'yellow' },
                        {'range': [30,35],'color': 'orange' },
                        {'range': [35,40],'color':'orangered'},
                        {'range': [40,222],'color':'red' },
                    ],
                    'threshold': {
                        'line': {'color': "rgb(50,50,50)", 'width': 5},
                        'thickness': 0.95,
                        'value': bmi}
                },
            )],
            output_type='div',
            include_plotlyjs=False,
            show_link=False,
            link_text="",
        )
    if 0 <= bmi < 15:
        bmi_status = 'Very severely underweight'
        bmi_color = 'red'
    elif 15 <= bmi < 16:
        bmi_status = 'Severely underweight'
        bmi_color = 'orange'
    elif 16 <= bmi < 18.5:
        bmi_status = 'Underweight'
        bmi_color = 'yellow'
    elif 18.5 <= bmi < 25:
        bmi_status = 'Normal (healthy weight)'
        bmi_color = 'green'
    elif 25 <= bmi < 30:
        bmi_status = 'Overweight'
        bmi_color = 'yellow'
    elif 30 <= bmi < 35:
        bmi_status = 'Moderately obese'
        bmi_color = 'orange'
    elif 35 <= bmi < 40:
        bmi_status = 'Severely obese'
        bmi_color = 'orangered'
    else:
        bmi_status = 'Very severely obese'
        bmi_color = 'red'
    return {'bmi':bmi,'bmi_status':bmi_status,'bmi_color':bmi_color,'bmi_indicator':bmi_indicator}