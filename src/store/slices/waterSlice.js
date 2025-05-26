import { createSlice } from '@reduxjs/toolkit';

const initialState = {
    waterData: null,
    predictions: null,
    waterQualityClass: null,
    plot: null,
    loading: false,
    error: null
};

const waterSlice = createSlice({
    name: 'water',
    initialState,
    reducers: {
        setWaterData: (state, action) => {
            state.waterData = action.payload;
        },
        setPredictions: (state, action) => {
            state.predictions = action.payload;
        },
        setWaterQualityClass: (state, action) => {
            state.waterQualityClass = action.payload;
        },
        setPlot: (state, action) => {
            state.plot = action.payload;
        },
        setLoading: (state, action) => {
            state.loading = action.payload;
        },
        setError: (state, action) => {
            state.error = action.payload;
        },
        resetState: (state) => {
            return initialState;
        }
    }
});

export const {
    setWaterData,
    setPredictions,
    setWaterQualityClass,
    setPlot,
    setLoading,
    setError,
    resetState
} = waterSlice.actions;

export default waterSlice.reducer; 