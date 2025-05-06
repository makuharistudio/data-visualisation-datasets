**Goal:** Validate the ability to use Vega or Vega-Lite custom mapping in Power BI using AppSource Deneb.

**Approach:** Embed the geographic data within the Vega or Vega-Lite specification itself.

Click the :earth_asia: icon to visit relevant web pages, or the :inbox_tray: icon to download a file.


### RESULT

- **My Power BI report** [:earth_asia:](https://community.powerbi.com/t5/Data-Stories-Gallery/AppSource-Deneb-Maps/m-p/2930366)

[![My Power BI report](https://github.com/makuharistudio/makuharistudio.github.io/blob/main/src/assets/portfolio/img-2022-11-power-bi-appsource-deneb-maps.gif?raw=true)](https://community.powerbi.com/t5/Data-Stories-Gallery/AppSource-Deneb-Maps/m-p/2930366)

- Original data sources
  - GeoJSON Maps of the globe by Ash Kyd [:earth_asia:](https://geojson-maps.ash.ms)
  - World Cities Datasets" by Viswanathan C on Kaggle [:earth_asia:](https://www.kaggle.com/datasets/viswanathanc/world-cities-datasets)

- Modified data source
  - Trimmed version of GeoJSON map data [:inbox_tray:](/AppSource%20Deneb%20maps/compressed.geo.json)


### POWER BI REPORT CODE

For comprehensive step-by-step on how to implement the following Deneb visual specifications, see my blog post: [:earth_asia:](https://makuharistudio.github.io/#/blog/how-to-use-geographic-maps-in-power-bi-with-appsource-deneb)


### FILLED AREA MAP

![Deneb: Filled area map fixed (Vega-Lite)](/AppSource%20Deneb%20maps/Power%20BI%20gif%20preview/Filled%20area%20map%20fixed.gif?raw=true)

**Deneb specification**

```
{"background": "null",
 "view": {"fill": "#F0F8FF", 
          "fillOpacity": 1.0 },
 "width": 1000,
 "height": 500,
 "data": {
    "name": "map",
    "values": {
      "type": "FeatureCollection",
      << add map data here >>
    },
    "format": {"type": "json", "property": "features"}
 },
 "transform": [{
    "lookup": "properties.Country",
    "from": {
      "data": {"name": "dataset"},
        "key": "Country",
        "fields": ["Population"]
    }
 }],
 "projection": { "type": "mercator" },
 "mark": {"type": "geoshape", 
          "strokeWidth": "0.5",
          "stroke": "#000000"},
 "encoding": {
    "tooltip": [{"field": "properties.Country", 
                 "title": "Country"}, 
                {"field": "Population"}],
    "color": {
      "field": "Population",
      "type": "quantitative",
      "scale": {"range": ["#EBF7BB", "#1D368A"]}
    }
 }
}
```


### COORDINATE POINT MAP

![Deneb: Coordinate point map fixed (Vega-Lite)](/AppSource%20Deneb%20maps/Power%20BI%20gif%20preview/Coordinate%20point%20map%20fixed.gif?raw=true)

**Deneb specification**

```
{"background": "null",
 "view": {"fill": "#F0F8FF", 
          "fillOpacity": 1.0 },
 "width": 1000,
 "height": 500,
 "layer": [
    { "data": {
        "values": {
          "type": "FeatureCollection",
          << add map data here >>
        },
        "format": {"type": "json", "property": "features"}
      },
      "mark": {"type": "geoshape", 
               "strokeWidth": "0.5",
               "stroke": "#000000",
               "fill": "#E8F5B9" },
      "encoding": {
        "tooltip": {"field": "properties.Country", "title": "Country"},
        "shape": {"type": "geojson"}
      }
    },
    { "data": { "name": "dataset" },
      "projection": { "type": "mercator"},
      "mark": "circle",
      "encoding": {
        "tooltip": [{"field": "Country"},
                    {"field": "City"},
                    {"field": "Latitude"},
                    {"field": "Longitude"},
                    {"field": "Population"}],
        "longitude": {
          "field": "Longitude",
          "type": "quantitative"
        },
        "latitude": {
          "field": "Latitude",
          "type": "quantitative"
        },
        "size": {"value": 5},
        "color": {"value": "red"}
      }
    }
  ]
}
```


### FILLED AREA WITH COORDINATE POINT MAP

![Deneb: Filled area with coordinate point map fixed (Vega-Lite)](/AppSource%20Deneb%20maps/Power%20BI%20gif%20preview/Filled%20area%20with%20coordinate%20point%20map%20fixed.gif?raw=true)


**Deneb specification**

```
{
  "background": "null",
  "view": {
    "fill": "#F0F8FF",
    "fillOpacity": 1
  },
  "width": 1000,
  "height": 500,
  "layer": [
    {
      "data": {
        "values": {
          "type": "FeatureCollection",
          << add map data here >>
        },
        "format": {
          "type": "json",
          "property": "features"
        }
      },
      "transform": [
        {
          "lookup": "properties.Country",
          "from": {
            "data": {"name": "dataset"},
            "key": "Country",
            "fields": [
              "Population",
              "Population by Country"
            ]
          }
        }
      ],
      "projection": {
        "type": "mercator"
      },
      "mark": {
        "type": "geoshape",
        "strokeWidth": "0.5",
        "stroke": "#000000"
      },
      "encoding": {
        "tooltip": [
          {
            "field": "properties.Country",
            "title": "Country"
          },
          {
            "field": "Population by Country",
            "title": "Population"
          }
        ],
        "color": {
          "field": "Population by Country",
          "type": "quantitative",
          "scale": {
            "range": [
              "#EBF7BB",
              "#1D368A"
            ]
          }
        }
      }
    },
    {
      "data": {"name": "dataset"},
      "projection": {
        "type": "mercator"
      },
      "mark": "circle",
      "encoding": {
        "tooltip": [
          {"field": "Country"},
          {"field": "City"},
          {"field": "Latitude"},
          {"field": "Longitude"},
          {"field": "Population"}
        ],
        "longitude": {
          "field": "Longitude",
          "type": "quantitative"
        },
        "latitude": {
          "field": "Latitude",
          "type": "quantitative"
        },
        "size": {"value": 5},
        "color": {"value": "red"}
      }
    }
  ]
}
```


### MAP PROJECTION EXPLORER

![Deneb: Map projection explorer fixed (Vega-Lite)](/AppSource%20Deneb%20maps/Power%20BI%20gif%20preview/Map%20projection%20explorer%20fixed.gif?raw=true)

**Deneb specification**

```
{"background": "null",
 "view": {"fill": "#F0F8FF", 
          "fillOpacity": 1.0 },
 "width": 1000,
 "height": 500,
 "params": [
    { "name": "projection",
      "value": "albers",
      "bind": {
        "input": "select",
        "options": [
          "albers",
          "albersUsa",
          "azimuthalEqualArea",
          "azimuthalEquidistant",
          "conicConformal",
          "conicEqualArea",
          "conicEquidistant",
          "equalEarth",
          "equirectangular",
          "gnomonic",
          "mercator",
          "naturalEarth1",
          "orthographic",
          "stereographic",
          "transverseMercator"
        ]
      }
    }
 ],
 "layer": [
    { "data": {
        "values": {
          "type": "FeatureCollection",
          << add map data here >>
        },
        "format": {"type": "json", "property": "features"}
      },
      "transform": [{
        "lookup": "properties.Country",
          "from": {
            "data": {"name": "dataset"},
                     "key": "Country",
                     "fields": ["Population", "Population by Country"]
          }
      }],
      "projection": {"type": {"expr": "projection"}},
      "mark": {"type": "geoshape",
               "strokeWidth": "0.5",
               "stroke": "#000000"
      },
      "encoding": {
        "tooltip": [{"field": "properties.Country", 
                     "title": "Country"}, 
                    {"field": "Population by Country"}],
        "color": {
          "field": "Population by Country",
          "type": "quantitative",
          "scale": {"range": ["#EBF7BB", "#1D368A"]}
        }
      }
    },
    { "data": { "name": "dataset" },
      "projection": {"type": {"expr": "projection"}},
      "mark": "circle",
      "encoding": {
        "tooltip": [{"field": "Country"},
                    {"field": "City"},
                    {"field": "Latitude"},
                    {"field": "Longitude"},
                    {"field": "Population"}],
        "longitude": {
          "field": "Longitude",
          "type": "quantitative"
        },
        "latitude": {
          "field": "Latitude",
          "type": "quantitative"
        },
        "size": {"value": 5},
        "color": {"value": "red"}
      }
    }
  ]
}
```


### SLIDER INTERACTIVE GLOBE

![Deneb: Slider interactive globe fixed (Vega-Lite)](/AppSource%20Deneb%20maps/Power%20BI%20gif%20preview/Slider%20interactive%20globe%20fixed.gif?raw=true)


**Deneb specification**

```
{
  "width": 500,
  "height": 500,
  "projection": {
    "type": "orthographic",
    "rotate": {"expr": "[rotate0, rotate1, 0]"}
  },
  "params": [
    {
      "name": "rotate0",
      "value": 0,
      "bind": {"input": "range", "min": -90, "max": 90, "step": 1}
    },
    {
      "name": "rotate1",
      "value": 0,
      "bind": {"input": "range", "min": -90, "max": 90, "step": 1}
    },
    {
      "name": "populationSize",
      "value": 2.0,
      "bind": {"input": "range", "min": 0.1, "max": 4, "step": 0.1}
    }
  ],
  "layer": [
    {
      "data": {"sphere": true},
      "mark": {"type": "geoshape", "fill": "#F0F8FF"}
    },
    {
      "data": { "graticule": true },
      "mark": {
        "type": "geoshape",
        "stroke": "#B0D8FF",
        "strokeWidth": 0.25
      }
    },
    {
      "data": {
        "values": {
          "type": "FeatureCollection",
          << add map data here >>
        },
        "format": {"type": "json", "property": "features"}
      },
      "transform": [{
        "lookup": "properties.Country",
          "from": {
            "data": {"name": "dataset"},
            "key": "Country",
            "fields": ["Population", "Population by Country"]
          }
      }],
      "mark": {"type": "geoshape",
               "strokeWidth": "0.5",
               "stroke": "#000000"
      },
      "encoding": {
        "shape": {"type": "geojson"},
        "tooltip": [{"field": "properties.Country", 
                     "title": "Country"}, 
                    {"field": "Population by Country",
                     "title": "Population"
                    }],
        "color": {
          "field": "Population by Country",
          "type": "quantitative",
          "scale": {"range": ["#EBF7BB", "#1D368A"]}
        }
      }
    },
    {
      "data": { "name": "dataset" },
      "transform": [
        {"calculate": "datum.Longitude", "as": "longitude"},
        {"calculate": "datum.Latitude", "as": "latitude"},
        {"filter": "(rotate0 * -1) - 90 < datum.longitude && datum.longitude < (rotate0 * -1) + 90 && (rotate1 * -1) - 90 < datum.latitude && datum.latitude < (rotate1 * -1) + 90"},
        {"calculate": "abs(datum.Longitude)", "as": "magnitude"}
      ],
      "mark": {"type": "circle", "color": "red", "opacity": 1.0},
      "encoding": {
        "longitude": {"field": "longitude", "type": "quantitative"},
        "latitude": {"field": "latitude", "type": "quantitative"},
        "size": {
          "legend": null,
          "field": "magnitude",
          "type": "quantitative",
          "scale": {
            "type": "sqrt",
            "domain": [0, 100],
            "range": [0, {"expr": "pow(populationSize, 3)"}]
          }
        },
        "tooltip": [{"field": "Country", "name": "Country"},
                    {"field": "City"},
                    {"field": "Latitude"},
                    {"field": "Longitude"},
                    {"field": "Population"}]
      }
    }
  ]
}
```


### INTERACTIVE MAP (PAN & ZOOM)

![Deneb: Interactive map pan & zoom (Vega-Lite)](/AppSource%20Deneb%20maps/Power%20BI%20gif%20preview/Interactive%20map%20pan%20and%20zoom.gif?raw=true)


**Deneb specification**

```
{
  "width": 1100,
  "height": 700,
  "autosize": "true",
  "background": "#EEFFFF",
  "signals": [
    { "name": "tx", "update": "width / 2" },
    { "name": "ty", "update": "height / 2" },
    { "name": "scale",
      "value": 150,
      "on": [{
        "events": {"type": "wheel", "consume": true},
        "update": "clamp(scale * pow(1.0005, -event.deltaY * pow(16, event.deltaMode)), 150, 3000)"
      }]
    },
    { "name": "angles",
      "value": [0, 0],
      "on": [{
        "events": "mousedown",
        "update": "[rotateX, centerY]"
      }]
    },
    { "name": "cloned",
      "value": null,
      "on": [{
        "events": "mousedown",
        "update": "copy('projection')"
      }]
    },
    { "name": "start",
      "value": null,
      "on": [{
        "events": "mousedown",
        "update": "invert(cloned, xy())"
      }]
    },
    { "name": "drag",
      "value": null,
      "on": [{
        "events": "[mousedown, window:mouseup] > window:mousemove",
        "update": "invert(cloned, xy())"
      }]
    },
    { "name": "delta", "value": null,
      "on": [{
        "events": {"signal": "drag"},
        "update": "[drag[0] - start[0], start[1] - drag[1]]"
      }]
    },
    { "name": "rotateX", "value": 0,
      "on": [{
        "events": {"signal": "delta"},
        "update": "angles[0] + delta[0]"
      }]
    },
    { "name": "centerY", "value": 0,
      "on": [{
        "events": {"signal": "delta"},
        "update": "clamp(angles[1] + delta[1], -60, 60)"
      }]
    }
  ],

  "projections": [
    {
      "name": "projection",
      "type": "mercator",
      "scale": {"signal": "scale"},
      "rotate": [{"signal": "rotateX"}, 0, 0],
      "center": [0, {"signal": "centerY"}],
      "translate": [{"signal": "tx"}, {"signal": "ty"}]
    }
  ],

  "data": [
    { "name": "world",
      "values": {
        "type": "FeatureCollection",
        << add map data here >>
      },
      "format": {"type": "json", "property": "features"}
    },
    { "name": "dataset", "format": {} },
    { "name": "graticule",
      "transform": [ { "type": "graticule", "step": [15, 15] } ]
    },
    { "name": "world_map",
      "source": "world",
      "transform": [
        { "type": "formula",
          "expr": "datum[\"properties\"] && datum[\"properties\"][\"Country\"]",
          "as": "properties.Country"
        },
        { "type": "lookup",
          "from": "dataset",
          "key": "Country",
          "fields": ["properties.Country"],
          "values": ["Population", "Population by Country"]
        },
        { "type": "filter",
          "expr": "isValid(datum[\"Population\"]) && isFinite(+datum[\"Population\"])"
        }
      ]
    },
    { "name": "powerbi_dataset",
      "source": "dataset",
      "transform": [
        { "type": "geojson",
          "fields": ["Longitude", "Latitude"],
          "signal": "layer_1_geojson_0"
        },
        { "type": "geopoint",
          "projection": "projection",
          "fields": ["Longitude", "Latitude"],
          "as": ["layer_1_x", "layer_1_y"]
        }
      ]
    }
  ],

  "marks": [
    { "type": "shape",
      "from": {"data": "graticule"},
      "encode": {
        "enter": {
          "strokeWidth": {"value": 0.25},
          "stroke": {"value": "#88D5FF"},
          "fill": {"value": "#88D5FF"}
        }
      },
      "transform": [ { "type": "geoshape", "projection": "projection" } ]
    },
    { "type": "shape",
      "style": ["geoshape"],
      "from": {"data": "world_map"},
      "encode": {
        "enter": {
          "strokeWidth": {"value": 0.5},
          "stroke": {"value": "#000000"}
        },
        "update": {
          "fill": {"scale": "color", "field": "Population by Country"},
            "tooltip": {
              "signal": "{\"Country\": isValid(datum[\"properties.Country\"]) ? datum[\"properties.Country\"] : \"\"+datum[\"properties.Country\"], \"Population\": isValid(datum[\"Population by Country\"]) ? datum[\"Population by Country\"] : \"\"+datum[\"Population by Country\"]}"
            },
            "ariaRoleDescription": {"value": "geoshape"},
            "description": {
              "signal": "\"Population: \" + (format(datum[\"Population\"], \"\")) + \"; Country: \" + (isValid(datum[\"properties.Country\"]) ? datum[\"properties.Country\"] : \"\"+datum[\"properties.Country\"])"
            }
        }
      },
      "transform": [ { "type": "geoshape", "projection": "projection" } ]
    },
    { "type": "symbol",
      "style": ["circle"],
      "from": {"data": "powerbi_dataset"},
      "encode": {
        "update": {
          "opacity": {"value": 1.0},
          "fill": {"value": "red"},
          "tooltip": {
            "signal": "{\"Country\": isValid(datum[\"Country\"]) ? datum[\"Country\"] : \"\"+datum[\"Country\"], \"City\": isValid(datum[\"City\"]) ? datum[\"City\"] : \"\"+datum[\"City\"], \"Population\": isValid(datum[\"Population\"]) ? datum[\"Population\"] : \"\"+datum[\"Population\"]}"
          },
          "ariaRoleDescription": {"value": "circle"},
          "description": {
            "signal": "\"Longitude: \" + (format(datum[\"Longitude\"], \"\")) + \"; Latitude: \" + (format(datum[\"Latitude\"], \"\")) + \"; Country: \" + (isValid(datum[\"Country\"]) ? datum[\"Country\"] : \"\"+datum[\"Country\"]) + \"; City: \" + (isValid(datum[\"City\"]) ? datum[\"City\"] : \"\"+datum[\"City\"])"
          },
          "x": {"field": "layer_1_x"},
          "y": {"field": "layer_1_y"},
          "size": {"value": 10},
          "shape": {"value": "circle"}
        }
      }
    }
  ],
  "scales": [
    { "name": "color",
      "type": "linear",
      "domain": {"data": "world_map", "field": "Population by Country"},
      "range":  ["#EBF7BB", "#1D368A"],
      "interpolate": "hcl",
      "zero": false
    }
  ]
}
```
