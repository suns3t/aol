// These are the required projections for use on the map 
Proj4js.defs["EPSG:3644"] = "+proj=lcc +lat_1=43 +lat_2=45.5 +lat_0=41.75 +lon_0=-120.5 +x_0=399999.9999984 +y_0=0 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +to_meter=0.3048 +no_defs";
Proj4js.defs["EPSG:3857"] = "+proj=merc +lon_0=0 +k=1 +x_0=0 +y_0=0 +a=6378137 +b=6378137 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs";

$(document).ready(function(){
    // base layer
    var base_layer = new OpenLayers.Layer.XYZ.Modified("Naturalistic", "http://pan.rc.pdx.edu/arcgis/rest/services/aol/nlcd/MapServer/tile/${z}/${y}/${x}", {
        sphericalMercator: false,
        transitionEffect: 'resize',
        tileOrigin: new OpenLayers.LonLat(-300000, 2763954),
        format: "jpg",
        isBaseLayer: true
    });

    // layer for the lakes
    var lakes_kml_layer = new OpenLayers.Layer.Vector("KML", {
        projection: new OpenLayers.Projection("EPSG:4326"),
        strategies: [new OpenLayers.Strategy.BBOX({resFactor: 1})],
        protocol: new OpenLayers.Protocol.HTTP({
            url: 'map/lakes.kml',
            params: {},
            format: new OpenLayers.Format.KML({
                extractStyles: true,
                extractAttributes: true,
                maxDepth: 16
            })
        }),
        styleMap: new OpenLayers.StyleMap({
            default: new OpenLayers.Style(),
            select: new OpenLayers.Style(),
        }),
        minScale: 432002,
        maxScale: 1
    });

    // don't have a clue why this is needed. Pulled out and simplified from the old AOL code
    lakes_kml_layer.initResolutions = function(){
        this.maxResolution = OpenLayers.Util.getResolutionFromScale(this.options.minScale, this.map.units);
        this.minResolution = OpenLayers.Util.getResolutionFromScale(this.options.maxScale, this.map.units);
        this.maxScale = OpenLayers.Util.getScaleFromResolution(this.minResolution, this.units);
        this.minScale = OpenLayers.Util.getScaleFromResolution(this.maxResolution, this.units);
    };

    lakes_kml_layer.events.register("featureselected", lakes_kml_layer, function(evt){
        // FYI a global `event` object magically is accessible in this function
        // somehow
        var feature = this.selectedFeatures[0];
        var attrs = feature.attributes;
        var html = "<h2>" + attrs.name + "</h2>" + "<div>" + attrs.description + "</div>";

        var onClose = function(){

        }

        var popup = new OpenLayers.Popup.FramedCloud(
            "foobar", 
            this.map.getLonLatFromViewPortPx(event.xy),
            new OpenLayers.Size(450, 150), 
            html, 
            null, 
            true, 
            onClose
        );

        this.map.addPopup(popup)
            


    });

    /*
    // handle the selected event when the lake is clicked
    lakes_kml_layer.events.on({
        featureselected: function(){
            attr
            console.log("here")
            console.log(this);

        }
    })*/


    // map config
    var scales = [1728004.3888287468, 864002.1944143734, 432001.0972071867, 216000.5486035933, 108000.2743017966, 54000.1371508983, 27000.0685754491, 13500.0342877245, 6750.0171438622];
    var map_options = {
        maxExtent: new OpenLayers.Bounds(-330000, -200000, 2630000, 1900000),
        projection: new OpenLayers.Projection("EPSG:3644"),
        displayProjection: new OpenLayers.Projection("EPSG:4326"),
        numZoomLevels: scales.length,
        restrictedExtent: new OpenLayers.Bounds(127741, 4648, 2363853, 1733815),
        scales: scales,
        units: "ft"
    }

    // create the map, add the layers, and zoom to the initial location
    var map = new OpenLayers.Map('map', map_options);
    map.addLayer(base_layer);
    map.addLayer(lakes_kml_layer);
    map.zoomToMaxExtent();
    map.setCenter(new OpenLayers.LonLat(1294408, 865759), 0);

    // when the map is moved update the lakes_kml_layer since it lazily fetches
    // the KML from the server
    map.events.register("moveend", map, function(event){
        lakes_kml_layer.protocol.params.scale = Math.round(this.getScale());
        lakes_kml_layer.protocol.params.bbox_limited = this.getExtent().toBBOX();
        lakes_kml_layer.redraw(true);
    })


    // make the KML layers clickable
    var control = new OpenLayers.Control.SelectFeature([lakes_kml_layer])
    map.addControl(control)
    control.activate()

});

// Custom layer class...because?
OpenLayers.Layer.XYZ.Modified = OpenLayers.Class(OpenLayers.Layer.XYZ, {
    getURL: function (bounds) {
        var res = this.map.getResolution();
        var x = Math.round((bounds.left - this.tileOrigin.lon) / (res * this.tileSize.w));
        var y = Math.round((this.tileOrigin.lat - bounds.top) / (res * this.tileSize.h));
        var z = this.map.getZoom();

        if ( ( x < 0 ) || ( y < 0 ) || ( z < 0 ) ) {
            return null;
        }

        var url = this.url;
        var s = '' + x + y + z;
        if ( url instanceof Array ) {
            url = this.selectUrl(s, url);
        }

        var path = OpenLayers.String.format(url, {'x': x, 'y': y, 'z': z});

        return path;
    },
    calculateGridLayout: function(bounds, extent, resolution) {
        var tilelon = resolution * this.tileSize.w;
        var tilelat = resolution * this.tileSize.h;

        var offsetlon = bounds.left - this.tileOrigin.lon;
        var tilecol = Math.floor(offsetlon/tilelon) - this.buffer;
        var tilecolremain = offsetlon/tilelon - tilecol;
        var tileoffsetx = -tilecolremain * this.tileSize.w;
        var tileoffsetlon = this.tileOrigin.lon + tilecol * tilelon;

        var offsetlat = this.tileOrigin.lat - bounds.top + tilelat;
        var tilerow = Math.floor(offsetlat/tilelat) - this.buffer;
        var tilerowremain = tilerow - offsetlat/tilelat;
        var tileoffsety = tilerowremain * this.tileSize.h;
        var tileoffsetlat = this.tileOrigin.lat - tilelat*tilerow;

        return {
            "tilelon"       : tilelon,
            "tilelat"       : tilelat,
            "tileoffsetlon" : tileoffsetlon,
            "tileoffsetlat" : tileoffsetlat,
            "tileoffsetx"   : tileoffsetx,
            "tileoffsety"   : tileoffsety
        };
    },

    CLASS_NAME: "OpenLayers.Layer.XYZ.Modified"
});
