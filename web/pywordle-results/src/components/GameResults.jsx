import React, { useState, useEffect } from 'react';

import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import GameResult from './GameResult.jsx';

function GameResults(props) {
	const [apiData, setAPIData] = useState({});
	const [resultList, setResultList] = useState([]);

	useEffect(() => {
		if (apiData.hasOwnProperty('data')) {
			setResultList(apiData.data.map((item, key) =>
				<Row className="mb-3" key={item.id}>
					<Col>
						<GameResult result={item} fetchOptions={props.fetchOptions} displayGuess={props.displayGuess} />
					</Col>
				</Row>
			));
		}
	}, [apiData, props.displayGuess]);

	useEffect(() => {
		async function fetchData() {
			const url = `https://wordle-api.gently.org.uk:7001/wordle-results/api/v1/games/${props.selectedGame}/results`;
			fetch(url, props.fetchOptions)
				.then(res => res.json())
				.then((data) => {
					setAPIData({
						time: new Date().toLocaleTimeString(),
						data: data.gameresults
					})
				})
		}

		if (props.selectedGame != -1) {
			fetchData();
		}
	}, [props.selectedGame]);

	return (
		<div>
			{resultList}
		</div>
	)
}

export default GameResults;
