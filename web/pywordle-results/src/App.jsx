import './App.css'
import { BrowserRouter, Routes, Route } from "react-router-dom"
import Container from 'react-bootstrap/Container';

import Header from './components/Header.jsx'
import Home from './components/Home.jsx'
import DistributionPerUserChart from './components/DistributionPerUserChart.jsx'
import DistributionPerNumGuessesChart from './components/DistributionPerNumGuessesChart.jsx'
import GameInfo from './components/GameInfo.jsx'
import StreakChart from './components/StreakChart.jsx'
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
      <Container fluid className="vh-100 vw-100">
        <BrowserRouter>
          <Header />
          <Routes>
            <Route exact path="/" element={<Home />} />
            <Route path="per-user" element={<DistributionPerUserChart fetchOptions={fetchOptions} />} />
            <Route path="per-guesses" element={<DistributionPerNumGuessesChart fetchOptions={fetchOptions} />} />
            <Route path="game-info" element={<GameInfo fetchOptions={fetchOptions} />} />
            <Route path="streak" element={<StreakChart fetchOptions={fetchOptions} />} />
            <Route path="*" element={<NoMatch />} />
          </Routes>
        </BrowserRouter>
      </Container>
    </>
  )
}

export default App
