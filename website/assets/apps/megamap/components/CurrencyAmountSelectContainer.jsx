import React, { Component, PropTypes } from 'react';
import Select from 'react-select';
import CurrencyStore from '../stores/CurrencyStore';
import CurrencyActions from '../actions/CurrencyActions';
import Option from '../models/Option';

class CurrencyAmountSelectContainer extends Component {

  static get labelName() { return 'Cost'; }

  constructor(props) {
    super(props);
    this.state = {
      isLoading: true,
      options: [],
      value: '',
      lookups: {},
      error: null,
    };
    this.updateOptions = this.updateOptions.bind(this);
    this.onChange = this.onChange.bind(this);
  }

  componentDidMount() {
    CurrencyStore.listen(this.updateOptions);
    CurrencyActions.fetch();
  }

  onChange(option) {
    const value = option ? option.value : '';
    this.setState({ value });
    if (this.props.onSelect) {
      this.props.onSelect(this.state.lookups[value]);
    }
  }

  updateOptions(data) {
    this.setState({
      lookups: data.lookups,
      options: Object.keys(data.lookups).map(key => new Option(key, key)),
      error: data.error,
      isLoading: false,
    });
  }

  render() {
    return (
      <Select
        value={this.state.value}
        name="cost"
        placeholder={this.labelName}
        options={this.state.options}
        onChange={this.onChange}
        isLoading={this.state.isLoading}
      />
    );
  }

}

CurrencyAmountSelectContainer.propTypes = {
  onSelect: PropTypes.func,
};

export default CurrencyAmountSelectContainer;
