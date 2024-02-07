import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import { LinkContainer } from 'react-router-bootstrap'

function Header(props) {
	return (
		<Navbar bg="light" expand="true" static="top">
			<LinkContainer to="/">
				<Navbar.Brand>Wordle Results Database</Navbar.Brand>
			</LinkContainer>
			<Navbar.Toggle aria-controls="basic-navbar-nav" />
			<Navbar.Collapse id="basic-navbar-nav">
				<Nav className="mr-auto">
					<LinkContainer to="/">
						<Nav.Link>Home</Nav.Link>
					</LinkContainer>
					<LinkContainer to="/per-user">
						<Nav.Link>Graph by User</Nav.Link>
					</LinkContainer>
					<LinkContainer to="/per-guesses">
						<Nav.Link>Graph by Number of Guesses</Nav.Link>
					</LinkContainer>
					<LinkContainer to="/streak">
						<Nav.Link>Streak History</Nav.Link>
					</LinkContainer>
					<LinkContainer to="/game-info">
						<Nav.Link>Game Info</Nav.Link>
					</LinkContainer>
				</Nav>
			</Navbar.Collapse>
		</Navbar>
	)
}

export default Header;
