import React, { Component, PropTypes } from "react";
import {Button} from './forms';

export default class ResultsBox extends Component {
  static propTypes = {
    results: PropTypes.array.isRequired,
  }

  handleDetailClick = (event) => {
    if (event.target.value) {
      window.open(event.target.value, '_blank');
    }
  }

  handleMapViewClick = (event) => {
    console.log(`handleMapViewClick: ${event.target.value}`);
  }

  render() {
    return (
      <ul className="search-results">
      {
        this.props.results.map((result, index) => {
          return (
            <li key={index} className="result">
              <p>{result.name}</p>
              <p>{result.infrastructure_type}</p>
              <div className='button-bar'>
                <Button type='button'
                  onClick={this.handleMapViewClick}
                  value={result.geo}
                >View on Map</Button>
                <Button type='button'
                  onClick={this.handleDetailClick}
                  value={result.page_url}
                >Open detail page</Button>
              </div>
            </li>
          );
        })
      }
      </ul>
    );
  }
}
