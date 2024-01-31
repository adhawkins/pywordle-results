import './App.css'
import { BrowserRouter, Routes, Route } from "react-router-dom"

import Layout from './Layout.jsx'
import Home from './Home.jsx'
import DistributionPerUserChart from './DistributionPerUserChart.jsx'
import DistributionPerNumGuessesChart from './DistributionPerNumGuessesChart.jsx'
import NoMatch from './NoMatch.jsx'

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
            <Route path="*" element={<NoMatch />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </>
  )
}

export default App
