import React, { useState } from 'react';
import ReactDOM from 'react-dom/client';
import { Link, Outlet } from "react-router-dom";

function Layout() {
	return (
		<div className="row">
			<div className="column-left">
				<nav>
					<ul>
						<li>
							<Link to="/">Home</Link>
						</li>
						<li>
							<Link to="/per-user">Per-user</Link>
						</li>
						<li>
							<Link to="/per-guesses">Per-guesses</Link>
						</li>
					</ul>
				</nav>
			</div>
			<div className="column-right">
				<Outlet />
			</div>
		</div>
	)
}

export default Layout;
