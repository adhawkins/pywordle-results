import React, { useState, useEffect } from 'react';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import { AgChartsReact } from 'ag-charts-react';

function StreakChart(props) {
	const [userData, setUserData] = useState([]);
	const [apiData, setAPIData] = useState({});
	const [chartOptions, setChartOptions] = useState({});

	function updateChart() {
		const streakData = {};
		const maxGame = apiData.data[0].game;

		userData.data.forEach((user) => {
			user.maxStreak = 0;
			user.currentStreak = 0;

			streakData[user.id] = {
				fullName: user.fullname,
				streakData: [],
			}
		});

		for (let game = 0; game <= maxGame; game++) {
			userData.data.forEach((user) => {
				const gameData = apiData.data.find((entry) => entry.game == game && entry.user == user.id);
				const currentData = streakData[user.id];

				if (gameData && gameData.success) {
					user.currentStreak++;
					currentData.streakData[game] = user.currentStreak;
					if (user.currentStreak > user.maxStreak) {
						user.maxStreak = user.currentStreak;
					}
				} else {
					currentData.streakData[game] = 0;
					user.currentStreak = 0;
				}
			})
		}

		const chartData = [];

		for (let game = 0; game < maxGame; game++) {
			const newData = {
				game: game,
			};

			userData.data.forEach((user) => {
				newData[user.username] = streakData[user.id].streakData[game];
			})

			chartData.push(newData);
		}

		const chartSeries = []

		userData.data.forEach((user) => {
			chartSeries.push({
				type: 'line',
				xKey: 'game',
				xName: 'game',
				yKey: user.username,
				yName: `${user.fullname} - longest: ${user.maxStreak}, current: ${user.currentStreak}`,
				marker: {
					size: 1,
				}
			})
		});

		setChartOptions({
			title: {
				text: "Streak history",
			},
			data: chartData,
			series: chartSeries,
			axes: [
				{
					type: "category",
					position: "bottom",
					label: {
						enabled: false,
					}
				},
				{
					type: "number",
					position: "left",
				}
			]
		})
	}

	useEffect(() => {
		if (apiData.hasOwnProperty('data') && apiData.data.length) {
			updateChart();
		}
	}, [apiData]);

	useEffect(() => {
		async function fetchData() {
			fetch("https://wordle-api.gently.org.uk:7001/wordle-results/api/v1/results", props.fetchOptions)
				.then(res => res.json())
				.then((data) => {
					setAPIData({
						time: new Date().toLocaleTimeString(),
						data: data.results.sort((a, b) => { return b.game - a.game; }),
					})
				})
		}

		fetchData();
	}, [userData]);

	useEffect(() => {
		async function fetchData() {
			fetch("https://wordle-api.gently.org.uk:7001/wordle-results/api/v1/users", props.fetchOptions)
				.then(res => res.json())
				.then((data) => {
					setUserData({
						time: new Date().toLocaleTimeString(),
						data: data.users.sort((a, b) => { return a.id - b.id; }),
					})
				})
		}

		fetchData();
	}, []);

	return (
		<>
			<Row>
				<Col>
					<AgChartsReact options={chartOptions} />
				</Col>
			</Row>
		</>
	)
}

export default StreakChart;
