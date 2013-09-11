$('body').ready(function(){
Proj4js.defs["EPSG:3644"] = "+proj=lcc +lat_1=43 +lat_2=45.5 +lat_0=41.75 +lon_0=-120.5 +x_0=399999.9999984 +y_0=0 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +to_meter=0.3048 +no_defs";
Proj4js.defs["EPSG:3857"] = "+proj=merc +lon_0=0 +k=1 +x_0=0 +y_0=0 +a=6378137 +b=6378137 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs";

	/*I don't know if some of this gis stuff is right. 
	* I stole some of it it from config.js on old site 
        * but I don't know what i'm doing. */

    var lat = 5437819;
    var lon = -13379521;
    var zoom = 7;
 
    var fromProjection = new OpenLayers.Projection("EPSG:3857");   
    var toProjection   = new OpenLayers.Projection("EPSG:3857"); 
    var position       = new OpenLayers.LonLat(lon, lat).transform( fromProjection, toProjection);
 
    var map = new OpenLayers.Map("map");
    //use openstreet maps for now.
    map.addLayer(new OpenLayers.Layer.OSM("OpenStreetMap (Mapnik)"));
    
    map.setCenter(position, zoom);
});
