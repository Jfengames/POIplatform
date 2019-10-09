/**
 * Created by x1carbon on 2018/12/19.
 */
/**
 * Created by X240 on 2018/3/20.
 */
/**
 * 参数说明
 * mapInitCenter 地图中心点
 * mapZoomLv 地图缩放级别
 * isShowSlider 是否显示缩放按钮
 * isShowScalebar 是否显示比例尺
 */
var mapInitCenter=[106.530635,29.544606];
/*重庆：106.530635,29.544606北京：116.395645,39.929986*/
var mapZoomLv=14;
var isShowSlider=false;
var isShowScalebar=true;

var gcity="北京市";
var gprovince="北京市";
var gscene="居民区";


require([
    "dojo/parser",
    "dojo/ready",
    "dojo/_base/array",
    "dojo/io-query",
    "esri/map",
    "ArcGIS/amapBaseLayer",
    "esri/dijit/Scalebar",
    "dojo/domReady!"
], function(
    parser, ready, arrayUtils,ioQuery, Map,amapBaseLayer,Scalebar
) {
    ready(function() {
        //parser.parse();

        var Url=window.location.href;
        var queryUrl = Url.substring(Url.indexOf("?") + 1, Url.length);
        var queryObject = ioQuery.queryToObject(queryUrl);
        gcity=queryObject.city;
        gprovince=queryObject.province;
        gscene=queryObject.scene;

        var mapC = getCityCenter(gcity, gprovince);
        if (mapC.center.length != 0) {
            mapInitCenter.length = 0;
            mapInitCenter = mapC.center;
            mapZoomLv = mapC.zoomLayer + 3;
        }

        //初始化地图
        map = new Map("mapDiv", {
            center:mapInitCenter,
            logo:false,
            slider:isShowSlider,
            zoom: mapZoomLv,
            isZoomSlider:isShowSlider,
        });

        //比例尺
        if(isShowScalebar){
            var scalebar = new Scalebar({
                map: map,
                scalebarUnit: "dual",
                attachTo: "bottom-left"
            });
        }
        //底图服务
        var layer1 = new amapBaseLayer();
        map.addLayer(layer1);

        addFeatureLayer();

    });
});

function addFeatureLayer(){
    require([
        "esri/tasks/query",
        "esri/tasks/QueryTask",
        "esri/dijit/PopupTemplate",
        "esri/layers/FeatureLayer",
        "esri/symbols/SimpleMarkerSymbol",
        "esri/symbols/SimpleFillSymbol",
        "esri/symbols/SimpleLineSymbol",
        "esri/Color",
        "esri/renderers/UniqueValueRenderer"
    ], function(
        Query,QueryTask,PopupTemplate,FeatureLayer,SimpleMarkerSymbol,SimpleFillSymbol,SimpleLineSymbol,Color,UniqueValueRenderer
    ) {

        // var dataSource = new esri.layers.TableDataSource();
        // dataSource.workspaceId = "GONGCAN";
        // dataSource.dataSourceName = gcity+".shp";
        // var layerSource = new esri.layers.LayerDataSource();
        // layerSource.dataSource = dataSource;
        // var dynamicLayer = new FeatureLayer(arcgisIP+"/arcgis/rest/services/deepCoverage/deepCoverageArcGIS/MapServer/dynamicLayer", {
        //     mode: FeatureLayer.MODE_SNAPSHOT,
        //     outFields: ["*"],
        //     source: layerSource,
        //     infoTemplate: new PopupTemplate({
        //         /*"title": "全部小区({小区中文名})",*/
        //         "fieldInfos": [{
        //             "fieldName": "ANGLE",
        //             label: "方位角",
        //             visible: true
        //         }]
        //     }),
        //     id:"Cell"
        //   });
        // function createSector(size,azimuth,color){
        //     var sms=new SimpleMarkerSymbol();
        //     sms.setPath("M0,0,L0,100 L0,0 L-30,-96 A15,15 0 0,1 30,-96 z");
        //     sms.setSize(size);
        //     sms.setAngle(azimuth);
        //     sms.setColor(new Color(color));
        //     sms.setOutline(null);
        //     return sms;
        // }
        // var renderer = new UniqueValueRenderer(createSector(30,0,'gray'), "ANGLE");
        // for (var i=0; i<=360 ;i+=10){
        //     renderer.addValue(i, createSector(30,i,'gray'));
        // }
        // dynamicLayer.setRenderer(renderer);
        // map.addLayer(dynamicLayer);


        var dataSource1 = new esri.layers.TableDataSource();
        switch(gscene){
            case "居民区":
                dataSource1.workspaceId = "JUMINQU";
                break;
            case "医院":
                dataSource1.workspaceId = "YIYUAN";
                break;
            case "美食":
                dataSource1.workspaceId = "MEISHI";
                break;
            case "美景":
                dataSource1.workspaceId = "MEIJING";
                break;
        }
        dataSource1.dataSourceName = gcity+".shp";
        var layerSource1 = new esri.layers.LayerDataSource();
        layerSource1.dataSource = dataSource1;
        var dynamicLayer1 = new esri.layers.FeatureLayer(arcgisIP+"/arcgis/rest/services/deepCoverage/deepCoverageArcGIS/MapServer/dynamicLayer", {
            mode: esri.layers.FeatureLayer.MODE_SNAPSHOT,
            outFields: ["*"],
            source: layerSource1,
            infoTemplate: new PopupTemplate({
                "fieldInfos": [{
                    "fieldName": "FID",
                    visible:true
                },{
                    "fieldName": "NAME",
                    label: "名称",
                    visible: true
                },{
                    "fieldName": "ADDRESS",
                    label: "地址",
                    visible: true
                },{
                    "fieldName": "CLASSIFY",
                    label: "分类",
                    visible: true
                },{
                    "fieldName": "PROVINCE",
                    label: "省份",
                    visible: true
                },{
                    "fieldName": "CITY",
                    label: "地区/市",
                    visible: true
                }]
            }),
            id:"building"
        });

        switch(gscene){
            case "居民区":
                var renderer1 = new UniqueValueRenderer(
                    new SimpleFillSymbol(
                        SimpleFillSymbol.STYLE_SOLID,
                        new SimpleLineSymbol(
                            SimpleLineSymbol.STYLE_SOLID,
                            new Color([0,150,136,1]),
                            2
                        ),
                        new Color([34,29,97,0.25])
                    ),
                    "FID"
                );

                break;
            case "医院":
                var renderer1 = new UniqueValueRenderer(
                    new SimpleFillSymbol(
                        SimpleFillSymbol.STYLE_SOLID,
                        new SimpleLineSymbol(
                            SimpleLineSymbol.STYLE_SOLID,
                            new Color([255,77,77,1]),
                            2
                        ),
                        new Color([255,229,229,0.25])
                    ),
                    "FID"
                );
                break;
            case "美食":
                dataSource1.workspaceId = "MEISHI";
                break;
            case "美景":
                dataSource1.workspaceId = "MEIJING";
                break;
        }




        dynamicLayer1.setRenderer(renderer1);
        map.addLayer(dynamicLayer1);
    });
}