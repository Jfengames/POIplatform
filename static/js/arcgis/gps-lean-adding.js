function transformlat(x, y){  
    var ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * Math.sqrt(Math.abs(x));  
    ret += (20.0 * Math.sin(6.0 * x * Math.PI) + 20.0 * Math.sin(2.0 * x * Math.PI)) * 2.0 / 3.0;  
    ret += (20.0 * Math.sin(y * Math.PI) + 40.0 * Math.sin(y / 3.0 * Math.PI)) * 2.0 / 3.0;  
    ret += (160.0 * Math.sin(y / 12.0 * Math.PI) + 320 * Math.sin(y * Math.PI / 30.0)) * 2.0 / 3.0;  
    return ret;  
}  

function transformlng(x, y){
    var ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * Math.sqrt(Math.abs(x));  
    ret += (20.0 * Math.sin(6.0 * x * Math.PI) + 20.0 * Math.sin(2.0 * x * Math.PI)) * 2.0 / 3.0;  
    ret += (20.0 * Math.sin(x * Math.PI) + 40.0 * Math.sin(x / 3.0 * Math.PI)) * 2.0 / 3.0;  
    ret += (150.0 * Math.sin(x / 12.0 * Math.PI) + 300.0 * Math.sin(x / 30.0 * Math.PI)) * 2.0 / 3.0;  
    return ret;
}  

function wgs84togcj02(lng, lat) {
    var a = 6378245.0;
    var ee = 0.00669342162296594323;
    var dlat = transformlat(lng - 105.0, lat - 35.0);
    var dlng = transformlng(lng - 105.0, lat - 35.0);
    var radlat = lat / 180.0 * Math.PI;
    var magic = Math.sin(radlat);
    magic = 1 - ee * magic * magic;
    var sqrtmagic = Math.sqrt(magic);
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * Math.PI);
    dlng = (dlng * 180.0) / (a / sqrtmagic * Math.cos(radlat) * Math.PI);
    var mglat = lat + dlat;
    var mglng = lng + dlng;
    return [mglng, mglat]
};

function gcj02towgs84(lng, lat) {
    var a = 6378245.0;
    var ee = 0.00669342162296594323;
    var dlat = transformlat(lng - 105.0, lat - 35.0);
    var dlng = transformlng(lng - 105.0, lat - 35.0);
    var radlat = lat / 180.0 * Math.PI;
    var magic = Math.sin(radlat);
    magic = 1 - ee * magic * magic;
    var sqrtmagic = Math.sqrt(magic);
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * Math.PI);
    dlng = (dlng * 180.0) / (a / sqrtmagic * Math.cos(radlat) * Math.PI);
    var mglat = lat - dlat;
    var mglng = lng - dlng;
    return [mglng, mglat]
};

function gcj02_To_Bd09(gg_lon,gg_lat) {
    var x_pi = 3.14159265358979324 * 3000.0 / 180.0;
    var x = gg_lon, y = gg_lat;
    var z = Math.sqrt(x * x + y * y) + 0.00002 * Math.sin(y * x_pi);
    var theta = Math.atan2(y, x) + 0.000003 * Math.cos(x * x_pi);
    var bd_lon = z * Math.cos(theta) + 0.0065;
    var bd_lat = z * Math.sin(theta) + 0.006;
    return [bd_lon,bd_lat];
}

function bd09_To_gcj02(lon,lat) {
    var x_pi = 3.14159265358979324 * 3000.0 / 180.0;
    var x = lon - 0.0065, y = lat - 0.006;
    var z = Math.sqrt(x * x + y * y) - 0.00002 * Math.sin(y * x_pi);
    var theta = Math.atan2(y, x) - 0.000003 * Math.cos(x * x_pi);
    var gg_lon = z * Math.cos(theta);
    var gg_lat = z * Math.sin(theta);
    return [gg_lon,gg_lat];
}

function getDistance( longt1, lat1,  longt2,  lat2){
    var R = 6371229;
    var x=(longt2-longt1)* Math.PI*R*Math.cos( ((lat1+lat2)/2)*Math.PI/180)/180;
    var  y=(lat2-lat1)*Math.PI*R/180;
    var  distance=Math.hypot(x,y);
    return distance;
}

function  getLongt(lat1,  distance){
    var R = 6371229;
    var a = (180*distance)/(Math.PI*R*Math.cos(lat1*Math.PI/180));
    return a;
}
function  getLat(distance){
    var b=distance*0.000009;
    return b;
}