import React, { Component, PropTypes } from "react";
import Map from './Map';
import MapboxGl from "mapbox-gl/js/mapbox-gl";
import {Popup} from "mapbox-gl/js/mapbox-gl";
import GeoCentroidActions from '../actions/GeoCentroidActions';
import SearchStore from '../stores/SearchStore';
import Cartographer, {defaultZoom} from '../helpers/Cartographer';


export default class MapContainer extends Component {

  componentDidMount() {
    SearchStore.listen(this.onSearchResults);
  }

  handleMapLoad = () => {
    this.mapCtl = new Cartographer(this.refs.map._map);
    GeoCentroidActions.fetch();
  }

  handleMapClick = (event) => {
    this.mapCtl.queryForPopup(event);
  }

  onSearchResults = (data) => {
    const {results} = data;
    this.mapCtl.removePopup();
    if (results && results.length > 0) {
      this.mapCtl.resetMapZoom();
      const geoIdentifiers = results.filter((element, index) => element.geo)
                                    .map((element) => element.geo);
      if (geoIdentifiers.length > 0) {
        this.mapCtl.setCurrentGeo(geoIdentifiers);
      }
    } else {
      this.mapCtl.setCurrentGeo();
    }
  }

  render() {
    const mapProps = this.props;
    return (
      <Map {...mapProps}
        initialZoom={defaultZoom}
        ref="map"
        onMapLoad={this.handleMapLoad}
        onClick={this.handleMapClick}
      />
    )
  }
}
