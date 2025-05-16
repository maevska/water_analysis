import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import './Map.css';

const Map = ({ waterName, coordinates }) => {
return (
    <div className="map-container">
    <MapContainer
        center={[coordinates.lat, coordinates.lng]}
        zoom={13}
        style={{ height: '400px', width: '100%' }}
    >
        <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <Marker position={[coordinates.lat, coordinates.lng]}>
        <Popup>{waterName}</Popup>
        </Marker>
    </MapContainer>
    </div>
);
};

export default Map;