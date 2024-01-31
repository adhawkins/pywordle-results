import React, { useState } from 'react';
import ReactDOM from 'react-dom/client';
import { Link, Outlet } from "react-router-dom";
import Navbar from 'react-bootstrap/Navbar';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';

function Layout() {
	return (
		<div className="App">
			<Navbar>
				<Navbar.Brand>Wordle Results Database</Navbar.Brand>
			</Navbar>
			<Container fluid className="vh-100 vw-100">
				<Form>
					<Row className="p-1">
						<Col sm={2}>
							<nav>
								<ul>
									<li>
										<Link to="/">Home</Link>
									</li>
									<li>
										<Link to="/per-user">Graph by User</Link>
									</li>
									<li>
										<Link to="/per-guesses">Graph by Number of Guesses</Link>
									</li>
									<li>
										<Link to="/game-info">Game Info</Link>
									</li>
								</ul>
							</nav>
						</Col>
						<Col>
							<Outlet />
						</Col>
					</Row>
				</Form>
			</Container>
		</div>
	)
}

export default Layout;
