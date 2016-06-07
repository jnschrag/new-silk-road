import React, { Component, PropTypes } from "react";
import Radium, { Style } from "radium";
import Section from "./Section";
import SearchBar from "./SearchBar";
import CountrySelectContainer from "./CountrySelectContainer";
import RegionSelectContainer from "./RegionSelectContainer";
import StatusSelectContainer from "./StatusSelectContainer";
import InfrastructureTypeSelectContainer from "./InfrastructureTypeSelectContainer";
import PrincipalAgentSelectContainer from './PrincipalAgentSelectContainer';
import CurrencyAmountSelectContainer from './CurrencyAmountSelectContainer';
import ResultsBox from './ResultsBox';
import {Select, Button} from "./forms";
import SearchActions from '../actions/SearchActions';
import SearchStore from '../stores/SearchStore';


const searchBoxStyle = {
  maxWidth: 370,
  maxHeight: '100%',
  overflow: 'hidden',
  backgroundColor: '#FFF',
  position: 'absolute',
  display: 'flex',
  flexDirection: 'column',
  top: 0,
  left: 0,
  '.section-row': {
    display: 'block',
    clear: 'both',
    marginBottom: 4
  },
  'section > footer > button': {
    display: 'block',
    fontSize: 12,
    width: '100%'
  },
  footer: {
    marginTop: 2
  },
  button: {
    backgroundColor: '#eee'
  },
  label: {
    display: 'inline-block',
    width: 80,
    marginRight: 3,
    textAlign: 'right'
  },
  input: {
    maxWidth: 214,
    marginRight: 2
  },
  select: {
    maxWidth: 280,
    marginRight: 6,
  },
  'select:last-of-type': {
    marginRight: 0
  },
  'label, input, button': {
    display: 'inline-block'
  },
  'ul.searchResults': {
    listStyle: 'none',
    padding: '0 3px',
    margin: 0
  },
  '.scrollWrap': {
    flex: '1 1 auto',
    order: 0,
    overflowX: 'hidden',
    overflowY: 'auto'
  },
  '.searchWidget': {
    flex: '0 1 auto',
    order: 0,
  },
  '.buttonBar': {
    display: 'flex',
    justifyContent: 'space-between'
  },
  '.buttonBar > button': {
    flex: '0.4 1 auto',
    order: 0
  },
  '.resultsNav': {
    display: 'flex',
    justifyContent: 'space-between'
  },
  '.resultsNav button': {
    width: 80,
    flex: '0.475 1 auto',
    order: 0
  }
}

export default class SearchBox extends Component {
  static propTypes = {
    maxHeight: PropTypes.number.isRequired,
  }

  state = {
    query: {},
    results: [],
    count: 0,
    nextURL: null,
    previousURL: null,
    errorMessage: null,
    searchEnabled: false
  }

  componentDidMount() {
    SearchStore.listen(this.onSearchResults);
  }

  handleQueryUpdate = (q) => {
    let queryUpdate = Object.assign({}, this.state.query);
    for (var key in q) {
      if (q.hasOwnProperty(key)) {
        let value = q[key];
        if (typeof value === "string") {
          value = value.trim();
        }
        if (value && value !== '') {
          queryUpdate[key] = value;
        } else {
          delete queryUpdate[key];
        }
      }
    }
    let enableSearch = Object.keys(queryUpdate).length > 0;
    this.setState({query: queryUpdate, searchEnabled: enableSearch});
  }

  handleSubmit = (e) => {
    e.preventDefault();
    if (Object.keys(this.state.query).length > 0) {
      SearchActions.search(this.state.query);
    }
  }

  handleResultsNavClick = (e) => {
    if (e.target.value) {
      SearchActions.loadResults(e.target.value);
    }
  }

  onSearchResults = (data) => {
    var { count, results, next, previous, errorMessage } = data;
    this.setState({count, results, nextURL: next, previousURL: previous, errorMessage});
    this.refs.searchForm.collapse();
  }

  render() {
    searchBoxStyle.maxHeight = this.props.maxHeight;
    return (
      <div className="searchBox">
        <div className="searchWidget">
          <form onSubmit={this.handleSubmit}>
          <Section ref='searchForm' header={
            <SearchBar
            label="Project" name="name__icontains"
            value={this.state.projectTitle}
            onSearchInput={this.handleQueryUpdate}
            searchEnabled={this.state.searchEnabled}
            />
          }>
            <div className="section-row">
              <InfrastructureTypeSelectContainer onSelect={this.handleQueryUpdate} />
            </div>
            <div className="section-row">
              <StatusSelectContainer onSelect={this.handleQueryUpdate} />
            </div>
            <Section header={
              <SearchBar label="Initiative" name="initiatives__name__icontains"
              onSearchInput={this.handleQueryUpdate}
              searchEnabled={this.state.searchEnabled}
              />
            }>
            <div className="section-row">
              <PrincipalAgentSelectContainer onSelect={this.handleQueryUpdate} />
            </div>
            <div className="section-row">
              <RegionSelectContainer onSelect={this.handleQueryUpdate} />
            </div>
            </Section>
            <Section header={
              <SearchBar label="Funder" name="funding__sources__name__icontains"
              onSearchInput={this.handleQueryUpdate}
              searchEnabled={this.state.searchEnabled}
              />
            }>
            <div className="section-row">
              <CurrencyAmountSelectContainer onSelect={this.handleQueryUpdate} />
            </div>
            <div className="section-row">
              <CountrySelectContainer onSelect={this.handleQueryUpdate} />
            </div>
            </Section>
          </Section>
          </form>
        </div>
        <div className="resultsNav">
          <Button
            enabled={this.state.previousURL !== null}
            onClick={this.handleResultsNavClick}
            value={this.state.previousURL}
          >Previous</Button>
          <Button
            enabled={this.state.nextURL !== null}
            onClick={this.handleResultsNavClick}
            value={this.state.nextURL}
          >Next</Button>
        </div>
        <div className="scrollWrap">
          <div className="scrollContent">
            <ResultsBox results={this.state.results} />
          </div>
        </div>
        <Style
          scopeSelector=".searchBox"
          rules={searchBoxStyle}
        />
      </div>
    );
  }
}
