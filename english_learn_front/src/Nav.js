import { Component } from "react";
import { Link } from 'react-router-dom';
import './Nav.scss';

class Nav extends Component {
    constructor() {
        super();
    }

    render() {
        return (
            <nav className='nav'>
                <ul className='nav__links'>
                    <Link to='/'>
                        <li className='nav__link'>Home</li>
                    </Link>
                    <Link to='/quick_round'>
                        <li className='nav__link'>Quick</li>
                    </Link>
                    <Link to='/test_multi'>
                        <li className='nav__link'>Multi test</li>
                    </Link>
                </ul>
            </nav>
        )
    }


}

export default Nav;