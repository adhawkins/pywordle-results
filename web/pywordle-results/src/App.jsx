import './App.css'
import { BrowserRouter, Routes, Route } from "react-router-dom"

import Layout from './components/Layout.jsx'
import Home from './components/Home.jsx'
import DistributionPerUserChart from './components/DistributionPerUserChart.jsx'
import DistributionPerNumGuessesChart from './components/DistributionPerNumGuessesChart.jsx'
import GameInfo from './components/GameInfo.jsx'
import NoMatch from './components/NoMatch.jsx'

function App() {
  const fetchOptions = {
    headers: {
      'Authorization': 'Basic ' + btoa('andy:testing'),
    },
    method: 'GET',
  };

  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />} >
            <Route index element={<Home />} />
            <Route path="per-user" element={<DistributionPerUserChart fetchOptions={fetchOptions} />} />
            <Route path="per-guesses" element={<DistributionPerNumGuessesChart fetchOptions={fetchOptions} />} />
            <Route path="game-info" element={<GameInfo fetchOptions={fetchOptions} />} />
            <Route path="*" element={<NoMatch />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </>
  )
}

export default App
