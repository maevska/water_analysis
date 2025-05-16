import React from 'react';
import { PDFDownloadLink, Document, Page, Text, View } from '@react-pdf/renderer';
import './PDFReport.css';

const styles = {
  section: {
    margin: 10,
    padding: 10,
  },
  title: {
    fontSize: 24,
    marginBottom: 10,
  },
  waterName: {
    fontSize: 18,
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 16,
    marginTop: 10,
    marginBottom: 5,
  },
  results: {
    marginTop: 20,
  }
};

const PDFDocument = ({ data }) => (
<Document>
    <Page>
    <View style={styles.section}>
        <Text style={styles.title}>Отчет по качеству воды</Text>
        <Text style={styles.waterName}>Водоем: {data.waterName}</Text>
        
        <View style={styles.results}>
        <Text style={styles.subtitle}>Класс качества воды:</Text>
        <Text>{data.results.waterQualityClass}</Text>
        <Text style={styles.subtitle}>Прогнозируемые параметры:</Text>
        {Object.entries(data.results.predictedParams).map(([param, value]) => (
            <Text key={param}>{param}: {value.toFixed(2)}</Text>
        ))}
        </View>
    </View>
    </Page>
</Document>
);

const PDFReport = ({ data }) => {
return (
    <div className="pdf-container">
    <PDFDownloadLink
        document={<PDFDocument data={data} />}
        fileName={`water-quality-report-${data.waterName}.pdf`}
    >
        {({ loading }) => 
        loading ? 'Создание отчета...' : 'Скачать отчет (PDF)'
        }
    </PDFDownloadLink>
    </div>
);
};

export default PDFReport;