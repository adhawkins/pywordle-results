import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import { useEffect } from 'react';

function Guess(props) {
	const squares = ["⬜", "🟨", "🟩"];

	useEffect(() => {
		props.onClipboardInfoChanged({
			guessNumber: props.guess.guess_num,
			guess: props.guess.guess,
			numWords: props.guess.num_words,
			data: `${squares[props.guess.result1]}${squares[props.guess.result2]}${squares[props.guess.result3]}${squares[props.guess.result4]}${squares[props.guess.result5]}`,
		});
	});

	return (
		<Row>
			<Col className="text-end" sm={1}>
				{props.guess.guess_num}
			</Col>
			<Col sm={5} className="text-nowrap">
				{squares[props.guess.result1]}
				{squares[props.guess.result2]}
				{squares[props.guess.result3]}
				{squares[props.guess.result4]}
				{squares[props.guess.result5]}
			</Col>
			<Col sm={1}>
				{props.guess.num_words != 0 && props.guess.num_words}
			</Col>
			{props.displayGuess && <Col>{props.guess.guess}</Col>}
		</Row >
	)
}

Guess.defaultProps = {
	displayGuess: false,
}

export default Guess;
