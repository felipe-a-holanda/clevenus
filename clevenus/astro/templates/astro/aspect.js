function gen_label(value, valueText, valueAxis){
    var orb = {{ orb }};
    var max_value = 100;
    var angle = orb*(max_value-value)/max_value;
    
    var d = Math.floor(angle);
    var m = Math.floor((angle - d)*60);
    return d+'° '+m+"'";
}

function parseData(data){

    retrogrades = data.retro;
    
    return data.data;
}

function loadedData(x, chart, z){

    retrogrades.forEach(function (r, index, array) {

        var guide     = new AmCharts.Guide();
        guide.date = r.date;
        guide.toDate = r.toDate;
        guide.label = r.label;
        guide.position = "top";
        guide.lineAlpha = 1;
        guide.fillAlpha = 0.2;
        guide.fillColor = "#CC0000";
        guide.lineColor = "#CC0000";
        chart.categoryAxis.addGuide(guide);
    });


    chart.validateNow();
}


var chart = AmCharts.makeChart("chartdiv", {
    "type": "serial",
    "theme": "light",
    "columnWidth": 1,
    "dataDateFormat": "YYYY-MM-DD HH:NN",
    "marginRight":30,
    "balloon": {
        "adjustBorderColor": true,
        "color": "#000000",
        "cornerRadius": 5,
        "fillColor": "#FFFFFF",
        "fadeOutDuration": 5
      },
    "legend": {
        "equalWidths": false,
        //"periodValueText": "total: [[value.sum]]",
        "position": "top",
        "valueAlign": "left",
        "valueWidth": 100
    },
    "dataLoader": {
        "url": "{{ data_url }}",
        "postProcess": parseData,
        "load": loadedData,
        "format": "json"
      },
    "valueAxes": [{
        "stackType": "regular",
        "gridAlpha": 0.09,
        labelFunction: gen_label,

        "position": "top",
        "title": "Orb"
    }],
    "graphs": [
    {% for aspect in aspects %}    
    {
        "balloonText": "<span style='font-size:14px; color:#000000;'><b>[[date_str]]</b></span><br><img src='{{ p1.img }}' style='vertical-align:bottom; margin-left: 0px; width:32px; height:32px;'> <img src='{{ aspect.url }}' style='vertical-align:bottom;  width:20px; height:20px;'> <img src='{{ p2.img }}' style='vertical-align:bottom; margin-right: 10px; width:32px; height:32px;'><span style='font-size:14px; color:#000000;'><b>[[dms]]</b></span>",
        "fillAlphas": 1,
        //"bullet": "round",
        //"connect": true,
        "lineAlpha": 1,
        "type": "column",
        "title": "{{ aspect.name }}",
        "valueField": "{{ aspect.name }}",
        "urlField": "url"
    },
    {% endfor %}
    ],
    "plotAreaBorderAlpha": 0,
    "marginTop": 10,
    "marginLeft": 0,
    "marginBottom": 0,
    "chartScrollbar": {},
    "chartCursor": {
        "cursorAlpha": 0
    },
    "categoryField": "date",
    "categoryAxis": {
        "parseDates": true,
        "minPeriod": "hh",
        
        "startOnAxis": true,
        "axisColor": "#DADADA",
        "gridAlpha": 0.07,
        "title": "Timeline",
        "guides": [{
            date: "{{today}}",
            lineColor: "#AAAAFF",
            lineThickness: 5,
            id: 'today-guide',
            lineAlpha: 1,
            fillAlpha: 1,
            fillColor: "#CC0000",
            dashLength: 0,
            inside: true,
            labelRotation: 90,
            label: "Today"
        },
        
        ]
    },
    "export": {
    	"enabled": true
     },
    
});


function handleClick(event)
{
    alert(event.item.category + ": " + event.item.values.value);
}


chart.addListener("clickGraphItem", handleClick);
