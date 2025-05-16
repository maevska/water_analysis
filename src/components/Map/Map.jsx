import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';
import './Map.css';


let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41]
});
L.Marker.prototype.options.icon = DefaultIcon;


const ChangeView = ({ center }) => {
    const map = useMap();
    useEffect(() => {
        map.setView(center);
    }, [center, map]);
    return null;
};

const Map = ({ waterName, coordinates }) => {
    if (!coordinates || !coordinates.lat || !coordinates.lng) {
        return null;
    }

    return (
        <div className="map-container">
            <MapContainer
                center={[coordinates.lat, coordinates.lng]}
                zoom={13}
                style={{ height: '400px', width: '100%' }}
            >
                <ChangeView center={[coordinates.lat, coordinates.lng]} />
                <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                />
                <Marker position={[coordinates.lat, coordinates.lng]}>
                    <Popup>{waterName}</Popup>
                </Marker>
            </MapContainer>
        </div>
    );
};

export default Map;