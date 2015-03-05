class LocationMap extends google.maps.Map
    constructor: (mapDiv) ->
        @focusName     = "Aotea Centre"
        @mapCentre     = lat: -36.851951, lng: 174.762256
        @focusLocation = lat: -36.851951, lng: 174.762256
        @focusAddress  = "50 Mayoral Drive, Auckland"
        google.maps.Map.apply(@, [mapDiv, @mapOpts()])
        @addMarker()
        @addCustomControls()

    mapOpts: ->
        center: @mapCentre
        zoom:        14
        scrollwheel: false
        mapTypeControlOptions:
            style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
            mapTypeIds: [
                google.maps.MapTypeId.ROADMAP,
                google.maps.MapTypeId.SATELLITE
            ]
        mapTypeId: google.maps.MapTypeId.ROADMAP
        styles: [
            featureType: "road"
            elementType: "geometry"
            stylers: [ color: "#d1d1b8" ]
           ,
            featureType: "road"
            elementType: "labels.icon"
            stylers: [ visibility: "off" ]
           ,
            featureType: "road.highway"
            elementType: "labels.text.fill"
            stylers: [ color: "#585141" ]
           ,
            featureType: "road.highway"
            elementType: "geometry"
            stylers: [ color: "#bebea8" ]
           ,
            featureType: "road.highway.controlled_access"
            elementType: "geometry"
            stylers: [ color: "#f1d980" ]
           ,
            featureType: "transit"
            elementType: "all"
            stylers: [ visibility: "on" ]
           ,
            featureType: "water"
            elementType: "geometry"
            stylers: [ color: "#c6e2ff" ]
           ,
            featureType: "poi"
            elementType: "all"
            stylers: [ visibility: "off" ]
           ,
            featureType: "poi.park"
            elementType: "all"
            stylers: [ visibility: "on" ]
           ,
            featureType: "poi.school"
            elementType: "all"
            stylers: [ visibility: "on" ]
           ,
            featureType: "poi"
            elementType: "geometry.fill"
            stylers: [ color: "#c5e3bf" ]
           ,
            featureType: "administrative.locality"
            elementType: "labels.text"
            stylers: [ color: "#a22222" ]
           ,
            featureType: "all"
            elementType: "labels.text.stroke"
            stylers: [ visibility: "off" ]
        ]

    addMarker: ->
        marker = new google.maps.Marker
            title:    @focusName
            position: @focusLocation
            map:      @
        infowindow = new google.maps.InfoWindow
            content:  $("#map-focusinfo-src").html()
        infowindow.open(@, marker)
        google.maps.event.addListener marker, 'click', =>
            infowindow.open(@, marker)
        return

    addCustomControls: ->
        TOP_RIGHT    = google.maps.ControlPosition.TOP_RIGHT
        RIGHT_CENTER = google.maps.ControlPosition.RIGHT_CENTER

        customControls = $('<div id="map-controls" />')
        customControls.css
            padding:    "5px"
            textAlign:  "center"
            color:      "black"
        getdir = $('<div id="get-directions" />')
        getdir.css
            padding:    "1px 5px"
            marginLeft: "5px"
            background: "white"
            display:    "inline-block"
            border:     "1px solid black"
            cursor:     "pointer"
            title:      "Get directions to #{@focusName} from an address"
        getdir.text("Get Directions")
        customControls.append(getdir)
        @controls[TOP_RIGHT].push(customControls[0])

        # FIXME: #map-directions etc should probably be generated dynamically
        mapdir = $("#map-directions")
        mapdir.hide()
        getdir.click =>
            if mapdir.is(":hidden")
                mapdir.show()
                @controls[RIGHT_CENTER].push(mapdir[0])

        $("#transit-time-option").change => @giveDirections()
        transitTime = moment()
        $("#transit-time").val(transitTime.format("h:mm a"))
        yyyymmdd = transitTime.format("YYYY-MM-DD")
        $("#transit-date").append($("<option value=\"#{yyyymmdd}\">Today</option>"))
        $("#transit-time").change => @giveDirections()
        for daynum in [1...7]
            transitTime.add(1, "day")
            yyyymmdd = transitTime.format("YYYY-MM-DD")
            dayName = transitTime.format("D MMM, ddd")
            $("#transit-date").append($("<option value=\"#{yyyymmdd}\">#{dayName}</option>"))
        $("#transit-date").change => @giveDirections()

        origin = $('#map-directions-origin')
        origin.val("")
        steps = $("#map-directions-steps")
        @autocomplete = new google.maps.places.Autocomplete origin[0],
            componentRestrictions: country: "nz"
        @autocomplete.bindTo('bounds', @)
        @dirService = new google.maps.DirectionsService()
        @dirDisplay = new google.maps.DirectionsRenderer
            panel: steps[0]
            preserveViewport: true
        $("#map-directions .close").click =>
            $("#transit-time").val(moment().format("h:mm a"))
            origin.val("")
            mapdir.hide()
            steps.empty()
            @dirDisplay.setMap(null)
            @controls[RIGHT_CENTER].pop()
        $(".travel-mode").click (ev) =>
            selectedIcon = $(".selected-travel-mode")
            if selectedIcon[0] != ev.target
                if $(ev.target).hasClass("travel-by-transit")
                    $(".transit-options").show()
                else
                    $(".transit-options").hide()
                selectedIcon?.removeClass("selected-travel-mode")
                $(ev.target).addClass("selected-travel-mode")
                @giveDirections()
        google.maps.event.addListener @autocomplete, 'place_changed', =>
            @giveDirections()
        return

    giveDirections: ->
        if $('#map-directions-origin').val() == ""
            return
        selectedIcon = $(".selected-travel-mode")
        place = @autocomplete.getPlace()
        if not place.geometry
            return

        transitOpts = null
        routeOpts =
            origin:         place.geometry.location
            destination:    @focusAddress

        if selectedIcon.hasClass("travel-by-transit")
            routeOpts['travelMode'] = google.maps.TravelMode.TRANSIT
            transitTimeOption = $("#transit-time-option").val()
            transitTime = moment($("#transit-date").val()+
                                   " "+$("#transit-time").val(),
                                 ["YYYY-MM-DD h:mm a",
                                  "YYYY-MM-DD h:mma",
                                  "YYYY-MM-DD ha",
                                  "YYYY-MM-DD h:m:sa",
                                  "YYYY-MM-DD HH:mm",
                                  "YYYY-MM-DD HH:mm:s",
                                  "YYYY-MM-DD h"])
            transitOpts = {}
            transitOpts[transitTimeOption] = transitTime.toDate()
            routeOpts['transitOptions'] = transitOpts
        else if selectedIcon.hasClass("travel-by-bicycle")
            routeOpts['travelMode'] = google.maps.TravelMode.BICYCLING
        else if selectedIcon.hasClass("travel-by-foot")
            routeOpts['travelMode'] = google.maps.TravelMode.WALKING
        else
            routeOpts['travelMode'] = google.maps.TravelMode.DRIVING

        @dirService.route routeOpts, (response, status) =>
            if (status == google.maps.DirectionsStatus.OK)
                @dirDisplay.setMap(@)
                @dirDisplay.setDirections(response)
                @getDiv().scrollIntoView()
            return
        return

$ ->
    locationMap = $('#location-map')
    if locationMap.length
        new LocationMap(locationMap[0])
        $('header .address').wrap('<a id="location-link" href="#location"></a>')
    return

