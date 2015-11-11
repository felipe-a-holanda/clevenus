function gen_label(value, valueText, valueAxis){
    var orb = {{ orb }};
    var max_value = 100;
    var angle = orb*(max_value-value)/max_value;
    
    var d = Math.floor(angle);
    var m = Math.floor((angle - d)*60);
    return d+'° '+m+"'";
}

function parseData(data){
    
    d1 = data.retrogrades1[0][0];
    d2 = data.retrogrades1[0][1];
    retrogrades = data.retrogrades;
    
    
    return data.data;
}

function loadedData(x, y, z){
    //console.log(x);
    //console.log(y);
    //console.log(z);
    console.log(d1);
    for r in retrogrades{
        console.log(r);
    }
    var guide     = new AmCharts.Guide();
    
    guide.date = d1;
    guide.toDate = d2;
    guide.label = "xuxu";
    guide.position = "top";
    guide.lineAlpha = 1;
    guide.labelRotation = 90;
    guide.lineColor = AmCharts.randomColor();
    
    y.categoryAxis.addGuide(guide);
    y.validateNow();
    console.log("data loaded");
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
        "url": "/test/",
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
        "balloonText": "<span style='font-size:14px; color:#000000;'><b>[[date_str]]</b></span><br><img src='{{ venus }}' style='vertical-align:bottom; margin-left: 0px; width:32px; height:32px;'> <img src='{{ aspect.url }}' style='vertical-align:bottom;  width:20px; height:20px;'> <img src='{{ jupiter }}' style='vertical-align:bottom; margin-right: 10px; width:32px; height:32px;'><span style='font-size:14px; color:#000000;'><b>[[dms]]</b></span>",
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
        {% for r in retrogrades1 %}
        {
            date: "{{r.0.date_str}}",
            toDate: "{{r.1.date_str}}",
            lineColor: "#CC0000",
            lineAlpha: 1,
            fillAlpha: 0.2,
            fillColor: "#CC0000",
            
            dashLength: 2,
            position: "top",
            
            balloonText: "Venus Retrograde",
            //inside: true,
            //labelRotation: 90,
            label: "Venus Retrograde"
        }, 
        {% endfor %}
        
        {% for r in retrogrades2 %}
        {
            date: "{{r.0.date_str}}",
            toDate: "{{r.1.date_str}}",
            lineColor: "#CC0000",
            lineAlpha: 1,
            fillAlpha: 0.2,
            fillColor: "#CC0000",
            dashLength: 2,
            position: "top",
            //inside: true,
            //labelRotation: 90,
            label: "Jupiter Retrograde"
        }, 
        {% endfor %}
        
        
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
