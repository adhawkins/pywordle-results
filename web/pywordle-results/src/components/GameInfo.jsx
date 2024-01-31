import React, { useState } from 'react';

import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import GameList from './GameList.jsx'
import GameDetails from './GameDetails.jsx'

function GameInfo(props) {
	const [selectedGame, setSelectedGame] = useState(-1);
	const [displayGuess, setDisplayGuess] = useState(false);

	function onGameChanged(game) {
		setSelectedGame(game);
	}

	function onDisplayGuessChanged(e) {
		setDisplayGuess(e.target.checked);
	}

	return (
		<Row>
			<Col sm={2}>
				<Row>
					<Col>
						<GameList fetchOptions={props.fetchOptions} selectedGame={selectedGame} onSelectionChanged={onGameChanged} />
					</Col>
				</Row>
				<Row>
					<Col>
						<Form.Check label='Show guesses' checked={displayGuess} onChange={onDisplayGuessChanged} />
					</Col>
				</Row>
			</Col>
			<Col>
				<GameDetails fetchOptions={props.fetchOptions} selectedGame={selectedGame} displayGuess={displayGuess} />
			</Col>
		</Row>
	);
}

export default GameInfo;
