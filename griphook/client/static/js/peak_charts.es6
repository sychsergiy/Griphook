"use strict";
var doc = document,
    INTERVALS = [
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
            value: 3 * 30 * 24 * 3600,
            verbose: 'Квартал'
        }
    ],
    METRICS_URL = '/peaks/peaks';


class PeakBarChart extends Chart {

    constructor (...args) {
        args[1].type = 'bar';
        super(...args);
    }

    update (data_label, labels, data) {
        let chart_data = this.config.data;

        chart_data.datasets[0].label = data_label;
        chart_data.labels = labels;
        chart_data.datasets[0].data = data;

        super.update();
    }

}


function getPeakChartFilteredData() {
    // Getting metric for bar chart here.
    let samples = [
        {claster: "olympus", server: "temp3", services_group: "prom-furiosa", service: "furiosa-celery-highpriority-2", instance: "0"},
        {claster: "olympus", server: "temp3", services_group: "prom-furiosa", service: "furiosa-celery-lowpriority-2", instance: "0"},
        {claster: "olympus", server: "hermes", services_group: "han_solo-trunk", service: "han_solo-app-2", instance: "0"},
        {claster: "olympus", server: "hermes", services_group: "han_solo-trunk", service: "han_solo-sche-2", instance: "0"},
        {claster: "olympus", server: "hephaestus", services_group: "qa-slack-bot", service: "qa-slack-bot-qa-2", instance: "0"},
        {claster: "kalm", server: "enyo", services_group: "pyup-bot--bot", service: "web", instance: "0"},
        {claster: "olympus", server: "hephaestus", services_group: "qa-slack-bot", service: "qa-slack-bot-qa-1", instance: "0"},
        {claster: "kalm", server: "aphrodite", services_group: "tofu--tofu-trunk", service: "celery", instance: "0"},
        {claster: "kalm", server: "aphrodite", services_group: "tofu--tofu-trunk", service: "celery", instance: "1"},
        {claster: "kalm", server: "enyo", services_group: "pyup-bot--bot", service: "redis", instance: "0"},
        {claster: "kalm", server: "enyo", services_group: "tofu--tofu-trunk", service: "celerybeat", instance: "0"},
        {claster: "olympus", server: "stheno", services_group: "walle", service: "walle-sexy-group-walle-by-2", instance: "0"},
        {claster: "olympus", server: "stheno", services_group: "walle", service: "walle-sexy-group-walle-kz-2", instance: "0"}
    ]
    let randomSample = samples[Math.floor(Math.random() * samples.length)];
    randomSample['since'] = '2018-05-01';
    randomSample['until'] = '2018-05-30';
    randomSample['step'] = INTERVALS[3].value;
    randomSample['metric_type'] = 'user_cpu_percent';


    return fetch(
        METRICS_URL + '?' + Object.keys(randomSample)
                            .map(k => `${encodeURIComponent(k)}=${encodeURIComponent(randomSample[k])}`)
                            .join('&'), 
        {
            method: 'get'
        }
    )   ;
};


window.onload = () => {
    // Init datetime widgets
	$('#peak_chart_time_from').datetimepicker({
        locale: 'ru',
        format: 'YYYY-MM-DD'
    });
    $('#peak_chart_time_until').datetimepicker({
        locale: 'ru',
        format: 'YYYY-MM-DD'
    });

    // Init step representation;
    let step_val_input = doc.getElementById('step-value')
    step_val_input.addEventListener('input', function() {
        for (let verb_block of doc.getElementsByClassName('step-value-verbose')) {
            verb_block.textContent = INTERVALS[this.value].verbose
        }
    });
    step_val_input.dispatchEvent(new Event('input'));

    let peak_chart = new PeakBarChart(
        doc.getElementById('peak_chart'), 
        {
            data: {
                labels: [],
                datasets: [
                    {
                        label: [],
                        backgroundColor: '#041558',
                        data: []
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
                        gridLines: {
                            offsetGridLines: false,
                            paddingLeft: 0
                        },
                    }],
                },
            }
        }
    );
};
