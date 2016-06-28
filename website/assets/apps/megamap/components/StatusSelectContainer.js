import {createSelectContainer} from './containers';
import Option from '../models/Option';
import StatusStore from '../stores/StatusStore';
import StatusActions from '../actions/StatusActions';

var StatusSelectContainer = createSelectContainer(
  StatusStore, StatusActions,
  'status', 'Status',
  function(data) {
    return data.results.map((obj) => new Option(obj.name, obj.id));
  }
);

export default StatusSelectContainer;