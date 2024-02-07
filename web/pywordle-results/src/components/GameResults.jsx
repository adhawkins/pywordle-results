import React, { useState, useEffect } from 'react';

import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import GameResult from './GameResult.jsx';

function GameResults(props) {
	const [apiData, setAPIData] = useState({});
	const [resultList, setResultList] = useState([]);
	const [clipboardInfo, setClipboardInfo] = useState([]);

	useEffect(() => {
		if (apiData.hasOwnProperty('data')) {
			setResultList(apiData.data.map((item, key) =>
				<Row key={item.id}>
					<Col>
						<GameResult result={item} fetchOptions={props.fetchOptions} displayGuess={props.displayGuess} onClipboardInfoChanged={onClipboardInfoChanged} />
					</Col>
				</Row >
			));
		} else {
			setResultList(
				<Row>
					<Col>
						&nbsp;
					</Col>
				</Row>
			);
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
						data: data.gameresults.sort((a, b) => { return a.user - b.user }),
					})
				})
		}

		setClipboardInfo([]);

		if (props.selectedGame != -1) {
			fetchData();
		}
	}, [props.selectedGame]);

	function onClipboardInfoChanged(newClipboardInfo) {
		const currentClipboardInfo = clipboardInfo;
		const thisInfo = currentClipboardInfo.find((value) => {
			return value.result == newClipboardInfo.result;
		});

		if (thisInfo) {
			thisInfo.user = newClipboardInfo.user;
			thisInfo.data = newClipboardInfo.data;
		} else {
			currentClipboardInfo.push(newClipboardInfo);
		}

		setClipboardInfo(currentClipboardInfo);

		props.onClipboardInfoChanged(clipboardInfo);
	}

	return (
		<div>
			{resultList}
		</div>
	)
}

export default GameResults;
