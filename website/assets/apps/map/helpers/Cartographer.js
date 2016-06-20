import alt from '../alt';
import ActionListeners from 'alt-utils/lib/ActionListeners';
import MapboxGl, {
  Popup,
  GeoJSONSource
} from "mapbox-gl/js/mapbox-gl";
import GeoCentroidActions from '../actions/GeoCentroidActions';
import GeoStoreActions from '../actions/GeoStoreActions';
import GeoStoreQueue from './GeoStoreQueue';
import GeoManager from './GeoManager';
import GeoStyles from './GeoStyles';
import {
  defaultZoom,
  minDetailZoom,
  maxFitZoom,
  onMoveDelayTime,
  boundsPadding,
} from './map-constants';


const identiferSep = ' : ';
const centroidsLayerId = 'project : centroids';
const metadataIdentifier = 'cartographer:identifier';
const metadataInfrastructureType = 'cartographer:infrastructureType';
const metadataProjectIdentifier = 'cartographer:projectIdentifier';
const metadataProjectName = 'cartographer:projectName';
const metadataProjectURL = 'cartographer:projectURL';


export default class Cartographer {

  constructor(map) {
    this._map = map;
    this._al = new ActionListeners(alt);
    this._gm = new GeoManager();
    this._gq = new GeoStoreQueue();
    this._stylo = new GeoStyles();
    this._lastMapUpdate = Date.now();
    this._updateDelayId = null;
    this._popup = null;
    this._popupLayerId = null;
    this._addListeners();
  }

  _addListeners() {
    this._al.addActionListener(GeoCentroidActions.UPDATE, this._handleCentroidsUpdate.bind(this));
    this._al.addActionListener(GeoCentroidActions.FAIL, this._handleCentroidsFail.bind(this));
    this._al.addActionListener(GeoStoreActions.SELECT_GEO_STORE_ID, this._handleGeoStoreSelect.bind(this));
    this._al.addActionListener(GeoStoreActions.DID_GET_GEO_STORE, this._handleDidGetGeoStore.bind(this));
    this._map.on('move', this._handleMapMove.bind(this));
    this._map.on('moveend', this._handleEndMapMove.bind(this));
    this._map.on('click', this._handleMapClick.bind(this));
  }

  // Handlers

  _handleCentroidsFail(error) {
    console.log('Error!');
  }

  _handleCentroidsUpdate(data) {
    this._gm.setGeoIdentifiers(data.features.map((feat) => feat.id));
    const source = new GeoJSONSource({
      data
    });
    const layer = Object.assign({
      source: centroidsLayerId,
      id: centroidsLayerId,
    }, this._stylo.getStyleFor('centroids'));
    this.setSource(layer.source, source);
    this.addLayer(layer);
    this._removePopup();
    this._setPopupLayer(layer.id);
  }

  _handleGeoStoreSelect(identifier) {
    this._gm.selectedGeoStore = identifier;
    if (!this._gm.hasGeo(identifier)) {
      GeoStoreActions.getGeoStore.defer(identifier);
    } else {
      const extent = this._gm.selectedGeoExtent;
      if (extent) {
        this._zoomToExtent(extent);
      }
    }
  }

  _handleDidGetGeoStore(geostore) {
    this.removePopup()
    const {
      identifier,
      extent,
      project,
    } = geostore;
    const {
      infrastructure_type,
      page_url,
      name: project_name,
      identifier: project_id,
    } = project;
    this._gq.resolveGeoStore(identifier);
    if (!this._gm.hasGeo(identifier)) {
      const geoTypes = ['lines', 'points', 'polygons'];
      let identifiers = [];
      for (let t of geoTypes) {
        const data = geostore[t];
        if (data.features.length) {
          const layerId = `${identifier}${identiferSep}${t}`;
          identifiers.push(layerId);
          const source = new GeoJSONSource({
            data
          })
          const layer = Object.assign({
            source: layerId,
            id: layerId,
            metadata: {
              metadataIdentifier: identifier,
              metadataInfrastructureType: infrastructure_type,
              metadataProjectIdentifier: project_id,
              metadataProjectName: project_name,
              metadataProjectURL: page_url
            }
          }, this._stylo.getStyleFor(t, infrastructure_type));
          this.setSource(layer.source, source, false);
          this.addLayer(layer);
        }
      }
      this._gm.addGeoRecord(identifier, identifiers, extent);
      this._updateMapState();
    }
    if (this._gm.selectedGeoStore === identifier && extent) {
      this._zoomToExtent(extent);
    }
  }

  _handleMapMove(event) {
    const now = Date.now();
    const delta = now - this._lastMapUpdate;
    if (delta > 250) {
      this._lastMapUpdate = now;
      this._updateMapState();
    }
  }

  _handleEndMapMove(event) {
    if (this._updateDelayId) {
      clearTimeout(this._updateDelayId);
      this._updateDelayId = null;
    } else {
      let self = this;
      this._updateDelayId = setTimeout(() => {
        self._updateDelayId = null;
        const zoomLevel = self._map.getZoom();
        if (zoomLevel >= minDetailZoom) {
          const identifiers = self._getCurrentCentroids()
            .map((obj) => obj.properties.geostore);
          self._updateGeometries([...new Set(identifiers)]);
        }
        self._updateMapState();
      }, onMoveDelayTime);
    }
  }

  _handleMapClick(event) {
    const {
      point,
      lngLat
    } = event;
    const layers = this._gm.layerIdentifiers;
    if (layers.length) {
      const width = 20,
        height = 20;
      const bbox = [
        [point.x - width / 2, point.y - height / 2],
        [point.x + width / 2, point.y + height / 2]
      ]
      const features = this._map.queryRenderedFeatures(bbox, {
        layers
      });

      if (!features.length) return;

      const feat = features[0];
      const {
        metadataIdentifier: identifier,
        metadataInfrastructureType: infrastructureType,
        metadataProjectIdentifier: projectIdentifier,
        metadataProjectName: projectName,
        metadataProjectURL: projectURL,
      } = feat.layer.metadata;


      const popup = new Popup();

      popup.setLngLat(lngLat)
        .setHTML(`<div class='popup-content'>
           <h4>${projectName}</h4>
           <p><a class='button' href='${projectURL}' target='_blank'>Open detail page</a></p>
           </div>`);

      this._addPopup(popup);
    }
  }

    // Manage map

  _updateGeometries(identifiers) {
    identifiers.filter((id) => !this._gm.hasGeo(id))
      .forEach((id) => {
        this._gq.loadGeoStore(id);
      });
  }

  _updateMapState() {
    let visibleCentroids = [...this._gm.selectedGeoIdentifiers];
    if (this._map.getZoom() >= minDetailZoom) {
      visibleCentroids = visibleCentroids.filter(x => !this._gm.loadedGeoIdentifiers.has(x));
    }
    this.showCentroids(visibleCentroids);
    this._lastMapUpdate = Date.now();
  }

  setSource(id, source, replace = true) {
    const src = this._map.getSource(id);
    if (src && replace) {
      this._map.removeSource(id);
    }
    this._map.addSource(id, source);
  }

  addLayer(layer) {
    this._map.addLayer(layer);
  }

  filterMap(layerId, filterArray) {
    this._map.setFilter(layerId, filterArray);
  }

  // View methods

  hideLayer(layerId) {
    this._map.setLayoutProperty(layerId, 'visibility', 'none');
  }

  showLayer(layerId) {
    this._map.setLayoutProperty(layerId, 'visibility', 'visible');
  }

  resetMapZoom() {
    this._map.zoomTo(defaultZoom);
  }

  _zoomToExtent(extent) {
    const isPoint = extent[0] === extent[2] && extent[1] === extent[3];
    if (isPoint) {
      const pt = extent.slice(0, 2);
      this._map.flyTo({
        center: pt,
        zoom: maxFitZoom
      });
    } else if (extent.length === 4) {
      const bounds = new MapboxGl.LngLatBounds.convert(extent);
      this._map.fitBounds(bounds, {
        padding: boundsPadding,
        maxZoom: maxFitZoom
      });
    }
  }

  // search results

  setCurrentGeo(identifiers) {
    this._gm.selectedGeoIdentifiers = identifiers;
    this._updateMapState();
  }

  showCentroids(centroidsIds) {
    this.showLayer(centroidsLayerId);
    if (centroidsIds) {
      this.filterMap(centroidsLayerId, ['in', 'geostore'].concat(centroidsIds))
    } else {
      this.filterMap(centroidsLayerId, ['!in', 'geostore', false]);
    }
  }

  hideCentroids(centroidsIds) {
    if (centroidsIds && this._gm.centroidsLoaded) {
      this.showLayer(centroidsLayerId);
      this.filterMap(centroidsLayerId, ['!in', 'geostore'].concat(centroidsIds))
    } else {
      this.hideLayer(centroidsLayerId);
    }
  }

  _getCurrentCentroids() {
    return this._map.queryRenderedFeatures({
      layers: [centroidsLayerId]
    });
  }


  // Popups
  _setPopupLayer(layerId) {
    this._popupLayerId = layerId;
  }

  queryForPopup(event) {
    if (this._popupLayerId && event.point) {
      const features = this._map.queryRenderedFeatures(event.point, {
        layers: [this._popupLayerId]
      });

      if (!features.length) return;

      const feat = features[0];
      const popup = new Popup();

      // Create popup HTML, the hard way. (So we can easily add the event listener to that button)
      let popupContainer = document.createElement('div');
      popupContainer.className = 'popup-content';
      let header = document.createElement('h4');
      header.appendChild(document.createTextNode(feat.properties.label || ''));
      let button = document.createElement('button');
      button.appendChild(document.createTextNode('Zoom to Detail'));
      button.addEventListener('click', (event) => GeoStoreActions.selectGeoStoreId(feat.properties.geostore));
      popupContainer.appendChild(header);
      popupContainer.appendChild(button);
      popup.setLngLat(feat.geometry.coordinates)
           .setDOMContent(popupContainer);

      this._addPopup(popup);

    }
  }

  removePopup() {
    this._removePopup();
  }

  _addPopup(popup) {
    popup.addTo(this._map);
    this._popup = popup;
  }

  _removePopup() {
    if (this._popup) {
      this._popup.remove();
      this._popup = null;
    }
  }
}

export {
  defaultZoom
};
