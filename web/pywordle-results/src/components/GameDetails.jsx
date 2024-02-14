import React, { useState, useEffect } from 'react';

import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';
import CopyToClipboard from 'react-copy-to-clipboard'

import GameResults from './GameResults.jsx'

function GameDetails(props) {
	const [gameInfo, setGameInfo] = useState({});
	const [apiData, setAPIData] = useState({});
	const [clipboardString, setClipboardString] = useState("");

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

	function onClipboardInfoChanged(clipboardInfo) {
		let newClipboardString = "";

		clipboardInfo.sort((a, b) => { return a.userID - b.userID });

		clipboardInfo.forEach((info) => {
			if (info.data.length) {
				newClipboardString += `${info.user}\n\n`;
				newClipboardString += `Wordle ${gameInfo.id} ${info.data.length <= 6 ? info.data.length : 'x'}/6\n\n`;

				let line = 0;

				info.data.forEach((data) => {
					if (props.displayGuess) {
						newClipboardString += `\`${data.guessNumber.toString().padStart(2, '0')}\`  - ${data.data}`

						if (data.numWords > 0 && data.guess != "") {
							newClipboardString += `- ||\`${data.guess}\`|| - ${data.numWords}`;
						}

						newClipboardString += "\n";

						line++;
						if (line == 6 && info.data.length > 6) {
							newClipboardString += "`===================================`\n";
						}
					} else {
						newClipboardString += `${data.guessNumber.toString().padStart(2, '0')}  - ${data.data}`
						if (data.numWords != 0) {
							newClipboardString += ` - ${data.numWords}`;
						}

						newClipboardString += "\n";

						line++;
						if (line == 6 && info.data.length > 6) {
							newClipboardString += "===================\n";
						}
					}
				})

				newClipboardString += "\n";
			}
		});

		setClipboardString(newClipboardString);
	}

	return (
		<Row>
			<Col sm={3}>
				<p>Game details for {props.selectedGame}</p>
				<p>ID: {gameInfo.id}</p>
				<p>Date: {gameInfo.date}</p>
				{props.displayGuess && <p>Solution: {gameInfo.solution}</p>}
				<CopyToClipboard text={clipboardString}>
					<Button>Copy</Button>
				</CopyToClipboard>
			</Col>
			<Col>
				<GameResults fetchOptions={props.fetchOptions} selectedGame={props.selectedGame} displayGuess={props.displayGuess} onClipboardInfoChanged={onClipboardInfoChanged} />
			</Col>
		</Row>
	)
}

GameDetails.defaultProps = {
	displayGuess: false,
}

export default GameDetails;
