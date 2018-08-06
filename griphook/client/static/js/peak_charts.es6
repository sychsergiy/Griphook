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
    METRICS_URL = '/peaks/peaks',
    AVARAGE_SERVICE_LOAD_URL = '/average_load/service';

var samples = [
    {claster: "olympus", server: "temp3", services_group: "prom-furiosa", service: "furiosa-celery-highpriority-2"},
    {claster: "olympus", server: "temp3", services_group: "prom-furiosa", service: "furiosa-celery-lowpriority-2"},
    {claster: "olympus", server: "hermes", services_group: "han_solo-trunk", service: "han_solo-app-2"},
    {claster: "olympus", server: "hermes", services_group: "han_solo-trunk", service: "han_solo-sche-2"},
    {claster: "olympus", server: "hephaestus", services_group: "qa-slack-bot", service: "qa-slack-bot-qa-2"},
    {claster: "kalm", server: "enyo", services_group: "pyup-bot--bot", service: "web"},
    {claster: "olympus", server: "hephaestus", services_group: "qa-slack-bot", service: "qa-slack-bot-qa-1"},
    {claster: "kalm", server: "aphrodite", services_group: "tofu--tofu-trunk", service: "celery"},
    {claster: "kalm", server: "enyo", services_group: "pyup-bot--bot", service: "redis"},
    {claster: "kalm", server: "enyo", services_group: "tofu--tofu-trunk", service: "celerybeat"},
    {claster: "olympus", server: "stheno", services_group: "walle", service: "walle-sexy-group-walle-by-2"},
    {claster: "olympus", server: "stheno", services_group: "walle", service: "walle-sexy-group-walle-kz-2"}
]


function initTestServiceFilter() {
    let filterListBlock = doc.querySelector('.services-filter ul'),
        filterRow,
        s;
    
    for (let i in samples) {
        s = samples[i];
        filterRow = doc.createElement('li');
        filterRow.setAttribute('class', 'list-group-item search-list-item');
        filterRow.innerHTML = `<input type="radio" 
                                      name="full_service_name" 
                                      value="${i}"
                                      id="full_service_name${i}">
                               <label for="full_service_name${i}">
                               ${s.services_group}.${s.service}
                               </label>`

        filterListBlock.appendChild(filterRow);
    };
};


function validateTimeInputs() {
    // Checks `div#peak_chart_time_from > input`, `div#peak_chart_time_until > input`
    // values.
    // Returns values if both valid
    let INVALID_CLASS = 'is-invalid';

    let since_input = doc.querySelector('div#peak_chart_time_from > input'),
        until_input = doc.querySelector('div#peak_chart_time_until > input'),
        since_date = new Date(since_input.value),
        until_date = new Date(until_input.value);

    // Check since_date
    if (since_date.toString() === 'Invalid Date') {
        since_input.classList.add(INVALID_CLASS)
        return;
    }
    since_input.classList.remove(INVALID_CLASS)

    // Check until date
    if (until_date.toString() === 'Invalid Date') {
        until_input.classList.add(INVALID_CLASS)
        return;
    }
    until_input.classList.remove(INVALID_CLASS)

    // Return valid data
    return {since: since_input.value, until: until_input.value}
}


function getPeakChartFilteredData() {
    // Getting metric for bar chart here.
    let service_input = doc.querySelector('input[type=radio][name=full_service_name]:checked'),
        sample,
        validated_dates;

    if (service_input) {
        sample = samples[service_input.value],
        validated_dates = validateTimeInputs();
    }

    if (validated_dates !== undefined) {
        sample['since'] = validated_dates.since,
        sample['until'] = validated_dates.until;
    }
    else {
        return;
    }
    
    sample['step'] = INTERVALS[doc.querySelector('input#step-value').value].value;
    sample['metric_type'] = 'user_cpu_percent';

    return fetch(
        METRICS_URL + '?' + Object.keys(sample)
                            .map(k => `${encodeURIComponent(k)}=${encodeURIComponent(sample[k])}`)
                            .join('&'), 
        {
            method: 'get'
        }
    );
};


function drawPeakChart(peak_chart) {
    // Get metric for peak chart and draw chart in `peak_chart`
    let chart_data_promise = getPeakChartFilteredData()
    if (chart_data_promise === undefined) return;

    chart_data_promise.then((response) => {
        return response.json();
    })
    .catch(())
    .then((json) => {
        let data_label = 'user_cpu_percent',
            labels = [],
            values = [];

        for (let metric of json.data) {
            labels.push(metric[1]);
            values.push(metric[0]);
        }
        labels.push('-');
        values.push(0);

        let chart_data = peak_chart.config.data;
        chart_data.datasets[0].label = data_label;
        chart_data.labels = labels;
        chart_data.datasets[0].data = values;

        peak_chart.update();
    });
};


function getAvarageLoadChartData() {
    // Getting metric for bar chart here.
    let service_input = doc.querySelector('input[type=radio][name=full_service_name]:checked'),
        sample,
        validated_dates;

    // Getting validated dates or undefined
    if (service_input) {
        sample = samples[service_input.value],
        validated_dates = validateTimeInputs();
    }

    if (validated_dates !== undefined) {
        sample['time_from'] = new Date(validated_dates.since).valueOf() / 1000;
        sample['time_until'] = new Date(validated_dates.until).valueOf() / 1000;
    }
    else {
        return;
    }
    
    // Only user_cpu_percent and only service load for now
    sample['metric_type'] = 'user_cpu_percent';
    return fetch(
        AVARAGE_SERVICE_LOAD_URL + '?' + Object.keys(sample)
                            .map(k => `${encodeURIComponent(k)}=${encodeURIComponent(sample[k])}`)
                            .join('&'), 
        {
            method: 'get'
        }
    );
}


function drawAwarageLoadChart(avarage_chart) {
    let ROOT_BAR_COLOR = '#1b665c',
        CHILD_BAR_COLOR = '#38c9b6';

    let chart_data_promise = getAvarageLoadChartData();

    if (chart_data_promise === undefined) return;

    chart_data_promise.then((response) => {
        return response.json();
    })
    .then((json) => {

        let chart_data = avarage_chart.config.data,
            labels = [],
            values = [],
            backgroundColors = [],
            borderWidths = [];

        if (json.root.hasOwnProperty('target')) {
            labels.push(json.root.target);
            values.push(json.root.value);
        }
        else {
            labels.push('No data');
            values.push(0);
        }
        backgroundColors.push(ROOT_BAR_COLOR);
        borderWidths.push(2);

        // Set root's children sources bars
        for (let child of json.children) {
            labels.push(child.target);
            values.push(child.value);
            backgroundColors.push(CHILD_BAR_COLOR);
            borderWidths.push(0);
        }

        // Form metric type here
        chart_data.datasets[0].label = 'user_cpu_percent';
        chart_data.labels = labels;
        chart_data.datasets[0].data = values;
        chart_data.datasets[0].backgroundColor = backgroundColors;
        chart_data.datasets[0].borderWidth = borderWidths;
        
        avarage_chart.update();
    })
}


window.onload = () => {
    // Init datetime widgets
	let sinceDatePeaker = $('#peak_chart_time_from').datetimepicker({
        locale: 'ru',
        format: 'YYYY-MM-DD'
    }),
        untilDatePeaker = $('#peak_chart_time_until').datetimepicker({
        locale: 'ru',
        format: 'YYYY-MM-DD'
    });

    // Init service peak test filter
    initTestServiceFilter();

    // Init step representation;
    let step_val_input = doc.getElementById('step-value')
    step_val_input.addEventListener('input', function() {
        for (let verb_block of doc.querySelectorAll('.step-value-verbose')) {
            verb_block.textContent = INTERVALS[this.value].verbose
        }
    });
    step_val_input.dispatchEvent(new Event('input'));

    var peak_chart = new Chart(
        doc.querySelector('#peak_chart'), 
        {
            type: 'bar',
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
                    }
                },
                scales: {
                    xAxes: [{
                        gridLines: {
                            offsetGridLines: false,
                        },
                    }],
                },
            }
        }
    );

    window.avarage_load_chart = new Chart(
        doc.querySelector('#avarage-load-chart'),
        {
            type: 'horizontalBar',
            data: {
                labels: [],
                datasets: [
                    {
                        label: ['Main'],
                        backgroundColor: [],
                        data: [],
                        borderColor: '#071c19'
                    }
                ],
            },
            options: {
                scales: {
                    yAxes: [{
                        barPercentage: 0.65,
                    }],
                },
            }
        }
    );

    // Redraw peak chart if radio button was clicked
    for (let filter of doc.querySelectorAll('input[name=full_service_name]')) {
        filter.addEventListener('click', () => {drawPeakChart(peak_chart); drawAwarageLoadChart(avarage_load_chart);});
    }

    sinceDatePeaker.on('dp.change', () => {drawPeakChart(peak_chart); drawAwarageLoadChart(avarage_load_chart);});
    untilDatePeaker.on('dp.change', () => {drawPeakChart(peak_chart); drawAwarageLoadChart(avarage_load_chart);});
    doc.querySelector('input#step-value').addEventListener('change', () => {drawPeakChart(peak_chart); drawAwarageLoadChart(avarage_load_chart);});
};
