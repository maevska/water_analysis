import { useDispatch, useSelector } from 'react-redux';
import { waterApi } from '../api/water.api';
import {
    setWaterData,
    setPredictions,
    setWaterQualityClass,
    setPlot,
    setLoading,
    setError
} from '../store/slices/waterSlice';

export const useWaterData = () => {
    const dispatch = useDispatch();
    const {
        waterData,
        predictions,
        waterQualityClass,
        plot,
        loading,
        error
    } = useSelector((state) => state.water);

    const getPredictions = async (data) => {
        try {
            dispatch(setLoading(true));
            dispatch(setError(null));

            const response = await waterApi.predict(data);

            dispatch(setWaterData(data));
            dispatch(setPredictions(response.predictions));
            dispatch(setWaterQualityClass(response.waterQualityClass));
            dispatch(setPlot(response.plot));

            return response;
        } catch (error) {
            dispatch(setError(error.message));
            throw error;
        } finally {
            dispatch(setLoading(false));
        }
    };

    const generateReport = async (data) => {
        try {
            dispatch(setLoading(true));
            dispatch(setError(null));

            const response = await waterApi.generateReport(data);

            const url = window.URL.createObjectURL(new Blob([response]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `water-quality-report-${data.waterName}.pdf`);
            document.body.appendChild(link);
            link.click();
            link.remove();

            return response;
        } catch (error) {
            dispatch(setError(error.message));
            throw error;
        } finally {
            dispatch(setLoading(false));
        }
    };

    return {
        waterData,
        predictions,
        waterQualityClass,
        plot,
        loading,
        error,
        getPredictions,
        generateReport
    };
}; 