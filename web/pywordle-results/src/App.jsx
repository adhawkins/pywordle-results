import React, { useState, useEffect } from 'react'
import './App.css'
import { BrowserRouter, Routes, Route } from "react-router-dom"

import DistributionPerUserChart from './DistributionPerUserChart.jsx'
import DistributionPerNumGuessesChart from './DistributionPerNumGuessesChart.jsx'
import Layout from './Layout.jsx'
import Home from './Home.jsx'
import NoMatch from './NoMatch.jsx'

function App() {
  const [count, setCount] = useState(0)
  const [result, setResult] = useState({
    time: "invalid",
    data: [],
  })

  const fetchOptions = {
    headers: {
      'Authorization': 'Basic ' + btoa('andy:testing'),
    },
    method: 'GET',
  };

  // useInterval(() => {
  // 	fetch("https://wordle-api.gently.org.uk:7001/wordle-results/api/v1/results")
  //     .then(res => res.json())
  //     .then((data) => {
  //       setResult({
  //         time: new Date().toLocaleTimeString(),
  //         data: data
  //       })
  //     })
  // }, 5000);

  useEffect(() => {
    async function fetchData() {
      fetch("https://wordle-api.gently.org.uk:7001/wordle-results/api/v1/results", fetchOptions)
        .then(res => res.json())
        .then((data) => {
          setResult({
            time: new Date().toLocaleTimeString(),
            data: data
          })
        })
    }

    fetchData();
  }, [])

  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />} >
            <Route index element={<Home />} />
            <Route path="per-user" element={<DistributionPerUserChart data={result.data.results} />} />
            <Route path="per-guesses" element={<DistributionPerNumGuessesChart data={result.data.results} />} />
            <Route path="*" element={<NoMatch />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </>
  )
}

export default App
