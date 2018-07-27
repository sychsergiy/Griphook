var peak_chart = new Chart(document.getElementById('peak_chart'), {
    type: 'bar',
    data: {
        labels: [
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
        datasets: [
            {
                label: 'user_cpu_peaks',
                type: 'bar',
                backgroundColor: '#041558',
                data: [
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
                    0
                ]
            }
        ]
    },
    options: {
        scales: {
            xAxes: [{
                barPercentage: 1.1,
                stacked: true,
                gridLines: {
                    // offsetGridLines: false,
                    zeroLineBorderDashOffset: 10
                },
                ticks: {
                    labelOffset: -23,
                },
                position: 'left'
            }],
            yAxes: [{
                // barPercentage: 0.7,
                stacked: true
            }],
        },
    }
});