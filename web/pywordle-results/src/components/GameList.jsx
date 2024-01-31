import { useEffect, useState } from 'react';
import Form from 'react-bootstrap/Form';

function GameList(props) {
	const [apiData, setAPIData] = useState({});
	const [items, setItems] = useState([]);
	const [selectedGame, setSelectedGame] = useState(-1);

	useEffect(() => {
		props.onSelectionChanged(selectedGame);
	}, [selectedGame]);

	useEffect(() => {
		if (apiData.hasOwnProperty('data') && apiData.data.length) {
			const newItems = apiData.data.reverse().map((item, key) =>
				<option key={item["id"]} value={item["id"]}>{item["id"]} - {item["date"]}</option>
			);

			setItems(newItems);

			if (props.selectedGame == -1) {
				setSelectedGame(newItems[0].key)
			} else {
				setSelectedGame(props.selectedGame)
			}
		}
	}, [apiData]);

	useEffect(() => {
		async function fetchData() {
			fetch("https://wordle-api.gently.org.uk:7001/wordle-results/api/v1/games", props.fetchOptions)
				.then(res => res.json())
				.then((data) => {
					setAPIData({
						time: new Date().toLocaleTimeString(),
						data: data.games
					})
				})
		}

		fetchData();

	}, []);

	function handleChange(e) {
		setSelectedGame(parseInt(e.target.value));
	}

	return (
		<Form.Group>
			<Form.Label>Games:</Form.Label>
			<Form.Control as="select"
				onChange={handleChange}
				value={selectedGame}>
				{items}
			</Form.Control>
		</Form.Group>
	)
}

export default GameList
