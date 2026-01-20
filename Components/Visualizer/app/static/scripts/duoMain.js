import { FormComponent } from './form/FormComponent.js';
import { MapComponent } from './map/MapComponent.js';
import { MainController } from './controllers/DuoMainController.js';

// const formEl = document.querySelector('#location-form');

const mapInstance = L.map('map').setView([51.109603609969334, 17.032424849065997], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(mapInstance);

const form = new FormComponent();
const map = new MapComponent(mapInstance);

new MainController(form, map);