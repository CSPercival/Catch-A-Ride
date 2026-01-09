import { map } from './state_handler.js';
import { updateInvalidAddress } from '../form/input_handler.js';

map.on('click', function(e) {
    updateInvalidAddress(e.latlng);
});