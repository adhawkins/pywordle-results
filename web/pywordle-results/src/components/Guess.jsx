import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

function Guess(props) {
	const squares = ["⬜", "🟨", "🟩"];

	return (
		<Row>
			<Col className="col-1 text-end">
				{props.guess.guess_num}
			</Col>
			<Col className="col-3">
				{squares[props.guess.result1]}
				{squares[props.guess.result2]}
				{squares[props.guess.result3]}
				{squares[props.guess.result4]}
				{squares[props.guess.result5]}
			</Col>
			<Col className="col-2">
				{props.guess.num_words}
			</Col>
			{props.displayGuess && <Col className="col-1">{props.guess.guess}</Col>}
		</Row >
	)
}

Guess.defaultProps = {
	displayGuess: false,
}

export default Guess;
