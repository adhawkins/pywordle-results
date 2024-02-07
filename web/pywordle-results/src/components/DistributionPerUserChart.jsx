import React, { useState, useEffect } from 'react';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import ReactDOM from 'react-dom/client';
import { AgChartsReact } from 'ag-charts-react';
import PropTypes from 'prop-types';

const DistributionPerUserChart = (props) => {
  const [apiData, setAPIData] = useState({})
  const [chartOptions, setChartOptions] = useState({})

  function updateChart() {
    const data = [];

    const totals = {}
    const userTotals = {};

    apiData.data.forEach((value) => {
      if (!userTotals.hasOwnProperty(value.user)) {
        userTotals[value.user] = 0;
      }

      userTotals[value.user]++;

      if (!totals.hasOwnProperty(value['userdetails.username'])) {
        totals[value['userdetails.username']] = {
          fullname: value['userdetails.fullname'],
          userid: value['user'],
          1: 0,
          2: 0,
          3: 0,
          4: 0,
          5: 0,
          6: 0,
          fail: 0
        }
      }

      if (value.success) {
        totals[value['userdetails.username']][value['guesses']]++;
      } else {
        totals[value['userdetails.username']].fail++;
      }
    })

    for (const [key, value] of Object.entries(totals)) {
      data.push({
        user: key,
        userName: value.fullname,
        userID: value.userid,
        1: value["1"] * 100 / userTotals[value.userid],
        2: value["2"] * 100 / userTotals[value.userid],
        3: value["3"] * 100 / userTotals[value.userid],
        4: value["4"] * 100 / userTotals[value.userid],
        5: value["5"] * 100 / userTotals[value.userid],
        6: value["6"] * 100 / userTotals[value.userid],
        fail: value.fail * 100 / userTotals[value.userid],
      });
    };

    data.sort((a, b) => { return a.userID - b.userID; });

    setChartOptions({
      title: {
        text: "Guess Distribution per user",
      },
      data: data,
      series: [
        { type: 'bar', xKey: 'userName', xName: 'userName', yKey: '1', yName: '1' },
        { type: 'bar', xKey: 'userName', xName: 'userName', yKey: '2', yName: '2' },
        { type: 'bar', xKey: 'userName', xName: 'userName', yKey: '3', yName: '3' },
        { type: 'bar', xKey: 'userName', xName: 'userName', yKey: '4', yName: '4' },
        { type: 'bar', xKey: 'userName', xName: 'userName', yKey: '5', yName: '5' },
        { type: 'bar', xKey: 'userName', xName: 'userName', yKey: '6', yName: '6' },
        { type: 'bar', xKey: 'userName', yKey: 'fail', yName: 'Fail' },
      ],
      axes: [
        {
          type: "category",
          position: "bottom",
          title: {
            text: "User",
            enabled: false,
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
            data: data.results
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
  );
}

DistributionPerUserChart.propTypes = {
  fetchOptions: PropTypes.shape({
    headers: PropTypes.shape({
      'Authorization': PropTypes.string,
    }),
    method: PropTypes.string,
  })
}

export default DistributionPerUserChart
