var INTERVALS = [
    {
        value: 3600,
        verbose: '1 Час'
    },
    {
        value: 2 * 3600,
        verbose: '2 Часа'
    },
    {
        value: 24 * 3600,
        verbose: '1 День'
    },
    {
        value: 2 * 24 * 3600,
        verbose: '2 дня'
    },
    {
        value: 7 * 24 * 3600,
        verbose: 'Неделя'
    },
    {
        value: 30 * 24 * 3600,
        verbose: 'Месяц'
    },
    {
        value: 3 * 24 * 3600,
        verbose: 'Квартал'
    }
]

var peak_chart_labels = [
    '19:00',
    '20:00',
    '21:00',
    '22:00',
    '23:00',
    '00:00',
    '01:00',
    '02:00',
    '03:00',
    '04:00',
    '05:00',
    '06:00',
    '07:00',
    '08:00',
    '09:00',
    '10:00',
    '11:00',
],
    peak_chart_data = [
        0.3,
        0.4,
        0.5,
        0.37,
        0.42,
        0.6,
        0.74,
        0.55,
        0.3,
        0.4,
        0.5,
        0.37,
        0.42,
        0.6,
        0.74,
        0.55,
        0,
    ],
    peak_chart_label = 'user_cpu_peaks';


var peak_chart = new Chart(document.getElementById('peak_chart'), {
    type: 'bar',
    data: {
        labels: peak_chart_labels,
        datasets: [
            {
                xAxesID: 'first_x',
                yAxesID: 'first_y',
                label: peak_chart_label,
                backgroundColor: '#041558',
                data: peak_chart_data
            }
        ]
    },
    options: {
        layout: {
            padding: {
                left: 50,
                right: 20,
                top: 20,
                bottom: 20
            }
        },
        scales: {
            xAxes: [{
                id: 'first_x',
                gridLines: {
                    offsetGridLines: false,
                    paddingLeft: 0
                },
            }],
            yAxes: [{
                id: 'first_y',
                // barPercentage: 0.7,
                stacked: true
            }],
        },
    }
});

$(function () {
	$('#peak_chart_time_from').datetimepicker({
        locale: 'ru',
        format: 'YYYY-MM-DD'
    });

    $('#peak_chart_time_until').datetimepicker({
        locale: 'ru',
        format: 'YYYY-MM-DD'
    });
    
    $('#step-value').on('input', function () {
        $('.step-value-verbose').text(
            INTERVALS[$(this).val()].verbose
        )
    });
    $('#step-value').trigger('input');
});
