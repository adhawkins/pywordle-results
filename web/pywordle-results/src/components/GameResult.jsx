import { useEffect, useState } from "react";

import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import Guess from './Guess.jsx';

function GameResult(props) {
	const [apiData, setAPIData] = useState({});
	const [displayResult, setDisplayResult] = useState("");
	const [guesses, setGuesses] = useState([]);

	useEffect(() => {
		if (apiData.hasOwnProperty('data') && apiData.data.length) {
			const newGuesses = apiData.data.map((element, key) =>
				<Guess key={element.guess_num} guess={element} displayGuess={props.displayGuess} />
			);

			setGuesses(newGuesses);
		}
	}, [apiData, props.displayGuess]);

	useEffect(() => {
		async function fetchData() {
			const url = `https://wordle-api.gently.org.uk:7001/wordle-results/api/v1/games/${props.result.game}/results/${props.result.id}/guesses`;
			fetch(url, props.fetchOptions)
				.then(res => res.json())
				.then((data) => {
					setAPIData({
						time: new Date().toLocaleTimeString(),
						data: data.guesses
					})
				})
		}

		if (props.result.hasOwnProperty('id')) {
			fetchData();
		}
	}, [props.result]);

	useEffect(() => {
		let result = `${props.result['userdetails.fullname']} = ${props.result.success ? 'won' : 'lost'}`;
		if (props.result.guesses) {
			result += ` (${props.result.guesses} guesses)`;
		}

		setDisplayResult(result);
	}, [props.result]);

	return (
		<Row>
			<Col>
				{displayResult}
			</Col>
			<Col>
				{guesses}
			</Col>
		</Row>
	)
}

GameResult.defaultProps = {
	displayGuess: false,
}


export default GameResult
