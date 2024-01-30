import React, { useState } from 'react';
import ReactDOM from 'react-dom/client';
import { AgChartsReact } from 'ag-charts-react';
import PropTypes from 'prop-types';

const DistributionPerNumGuessesChart = (props) => {
  const data = [];
  const series = [];
  const userTotals = {};

  if (props.hasOwnProperty('data') && props.data.length) {
    const totals = {}
    const users = {}

    props.data.forEach((value) => {
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

    props.data.forEach((value) => {
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
  }

  const chartOptions = {
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
  }

  return (
    <AgChartsReact options={chartOptions} />
  );
}

DistributionPerNumGuessesChart.propTypes = {
  data: PropTypes.arrayOf(PropTypes.shape({
    id: PropTypes.number,
    user: PropTypes.number,
    'userdetails.username': PropTypes.string,
    'userdetails.fullname': PropTypes.string,
    game: PropTypes.number,
    'gamedetails.date': PropTypes.string,
    'gamedetails.solution': PropTypes.string,
    guesses: PropTypes.number,
    success: PropTypes.number,
    uri: PropTypes.string,
  }))
}

DistributionPerNumGuessesChart.defaultProps = {
  data: []
}

export default DistributionPerNumGuessesChart
