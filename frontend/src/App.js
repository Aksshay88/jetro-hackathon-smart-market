import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);


function App() {
    const [produce, setProduce] = useState([]);
    const [selectedProduce, setSelectedProduce] = useState('');
    const [prediction, setPrediction] = useState(null);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        axios.get('http://localhost:8001/produce')
            .then(response => {
                setProduce(response.data.produce);
                if (response.data.produce.length > 0) {
                    setSelectedProduce(response.data.produce[0]);
                }
                setLoading(false);
            })
            .catch(error => {
                console.error('Error fetching produce list:', error);
                setError('Error fetching produce list. Please make sure the backend is running.');
                setLoading(false);
            });
    }, []);

    useEffect(() => {
        if (selectedProduce) {
            axios.get(`http://localhost:8001/predict/${selectedProduce}`)
                .then(response => {
                    setPrediction(response.data);
                })
                .catch(error => {
                    console.error(`Error fetching prediction for ${selectedProduce}:`, error);
                    setError(`Error fetching prediction for ${selectedProduce}.`);
                });
        }
    }, [selectedProduce]);

    const chartData = {
        labels: prediction?.historical_data.map(d => new Date(d.date).toLocaleDateString()),
        datasets: [
            {
                label: 'Historical Prices',
                data: prediction?.historical_data.map(d => d.price),
                fill: false,
                backgroundColor: 'rgb(75, 192, 192)',
                borderColor: 'rgba(75, 192, 192, 0.2)',
            },
        ],
    };

    if (loading) {
        return <div className="container mt-5"><h1 className="mb-4 text-center">Loading...</h1></div>;
    }

    return (
        <div className="container mt-5">
            <h1 className="mb-4 text-center">Smart Markets for Smart Produce</h1>
            {error && <div className="alert alert-danger">{error}</div>}
            <div className="row mb-4">
                <div className="col-md-6 offset-md-3">
                    <select 
                        className="form-select"
                        value={selectedProduce}
                        onChange={e => setSelectedProduce(e.target.value)}
                    >
                        {produce.map(p => (
                            <option key={p} value={p}>{p}</option>
                        ))}
                    </select>
                </div>
            </div>

            {prediction && (
                <div className="row">
                    <div className="col-md-8 offset-md-2">
                        <div className="card">
                            <div className="card-body">
                                <h5 className="card-title">Prediction for {prediction.produce_name}</h5>
                                <p className="card-text">Predicted Price for next week: <strong>{prediction.prediction.toFixed(2)}</strong></p>
                                <p className="card-text"><strong>Actionable Insight:</strong> {prediction.insight}</p>
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {prediction && (
                <div className="row mt-4">
                    <div className="col-md-8 offset-md-2">
                        <Line data={chartData} />
                    </div>
                </div>
            )}
        </div>
    );
}

export default App;