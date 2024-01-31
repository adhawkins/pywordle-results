import React, { useState, useEffect } from 'react';

import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import GameResults from './GameResults.jsx'

function GameDetails(props) {
	const [gameInfo, setGameInfo] = useState({});
	const [apiData, setAPIData] = useState({});

	useEffect(() => {
		if (apiData.hasOwnProperty('data')) {
			setGameInfo({
				'id': apiData.data.id,
				'date': apiData.data.date,
				'solution': apiData.data.solution,
			})
		}
	}, [apiData]);

	useEffect(() => {
		async function fetchData() {
			const url = `https://wordle-api.gently.org.uk:7001/wordle-results/api/v1/games/${props.selectedGame}`;
			fetch(url, props.fetchOptions)
				.then(res => res.json())
				.then((data) => {
					setAPIData({
						time: new Date().toLocaleTimeString(),
						data: data.game
					})
				})
		}

		if (props.selectedGame != -1) {
			fetchData();
		}
	}, [props.selectedGame]);

	return (
		<Row>
			<Col sm={2}>
				<p>Game details for {props.selectedGame}</p>
				<p>ID: {gameInfo.id}</p>
				<p>Date: {gameInfo.date}</p>
				{props.displayGuess && <p>Solution: {gameInfo.solution}</p>}
			</Col>
			<Col>
				<GameResults fetchOptions={props.fetchOptions} selectedGame={props.selectedGame} displayGuess={props.displayGuess} />
			</Col>
		</Row>
	)
}

GameDetails.defaultProps = {
	displayGuess: false,
}

export default GameDetails;
