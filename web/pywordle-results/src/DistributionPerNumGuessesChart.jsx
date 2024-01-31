import React, { useEffect, useState } from 'react';
import ReactDOM from 'react-dom/client';
import { AgChartsReact } from 'ag-charts-react';
import PropTypes from 'prop-types';

const DistributionPerNumGuessesChart = (props) => {
  const [apiData, setAPIData] = useState({})
  const [chartOptions, setChartOptions] = useState({})

  function updateChart() {
    const data = [];
    const series = [];
    const userTotals = {};

    const totals = {}
    const users = {}

    apiData.data.forEach((value) => {
      if (!userTotals.hasOwnProperty(value.user)) {
        userTotals[value.user] = 0;
      }

      userTotals[value.user]++;
      if (!users.hasOwnProperty(value.user)) {
        users[value.user] = {
          userName: value['userdetails.username'],
          fullname: value['userdetails.fullname'],
        };
      }
    })

    apiData.data.forEach((value) => {
      let groupName = "failure";

      if (value.success) {
        groupName = value.guesses;
      }

      if (!totals.hasOwnProperty(groupName)) {
        totals[groupName] = {};

        for (const [key, value] of Object.entries(users)) {
          totals[groupName][key] = 0;
        }
      }

      totals[groupName][value.user]++;
    })

    for (const [key, value] of Object.entries(totals)) {
      const percentageValue = {}

      for (const [percentKey, percentValue] of Object.entries(value)) {
        percentageValue[percentKey] = percentValue * 100 / userTotals[percentKey];
      }

      data.push(Object.assign({
        result: key
      },
        percentageValue));
    };

    for (const [key, value] of Object.entries(users)) {
      series.push({
        type: 'bar',
        xKey: 'result',
        xName: 'result',
        yKey: key,
        yName: value.fullname,
      })
    };

    setChartOptions({
      title: {
        text: "Guess Distribution per number of guesses",
      },
      data: data,
      series: series,
      axes: [
        {
          type: "category",
          position: "bottom",
          title: {
            text: "Num Guesses",
            enabled: true,
          },
        },
        {
          type: "number",
          position: "left",
          title: {
            text: "Frequency (%)",
            enabled: true,
          },
          label: {
            formatter: (params) => {
              return params.value + "%";
            },
          },
        },
      ],
    });
  }

  useEffect(() => {
    if (apiData.hasOwnProperty('data') && apiData.data.length) {
      updateChart()
    }
  }, [apiData]);

  useEffect(() => {
    async function fetchData() {
      fetch("https://wordle-api.gently.org.uk:7001/wordle-results/api/v1/results", props.fetchOptions)
        .then(res => res.json())
        .then((data) => {
          setAPIData({
            time: new Date().toLocaleTimeString(),
            data: data.results
          })
        })
    }

    fetchData();
  }, []);

  return (
    <AgChartsReact options={chartOptions} />
  );
}

DistributionPerNumGuessesChart.propTypes = {
  fetchOptions: PropTypes.shape({
    headers: PropTypes.shape({
      'Authorization': PropTypes.string,
    }),
    method: PropTypes.string,
  })
}

export default DistributionPerNumGuessesChart
