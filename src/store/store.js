import { configureStore } from '@reduxjs/toolkit';
import waterReducer from './slices/waterSlice';

export const store = configureStore({
    reducer: {
        water: waterReducer
    },
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware({
            serializableCheck: false
        })
}); 