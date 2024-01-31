import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

function Guess(props) {
	const squares = ["⬜", "🟨", "🟩"];

	return (
		<Row>
			<Col>
				{props.guess.guess_num}&nbsp;-&nbsp;
				{squares[props.guess.result1]}
				{squares[props.guess.result2]}
				{squares[props.guess.result3]}
				{squares[props.guess.result4]}
				{squares[props.guess.result5]}
				{props.displayGuess && ` - ${props.guess.guess}`}
			</Col>
		</Row>
	)
}

Guess.defaultProps = {
	displayGuess: false,
}

export default Guess;
